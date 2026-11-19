#!/usr/bin/env python3
"""Offline checks for the public atlas; never reads private research or user notes."""
import argparse,base64,gzip,hashlib,json,re,shutil,subprocess,sys,tempfile
from html.parser import HTMLParser
from pathlib import Path

def stable_bytes(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
class CheckError(Exception): pass
def require(value,message):
    if not value:raise CheckError(message)
def expand_payload(parsed):
    if parsed.get('atlas_string_dictionary')!=1:return parsed
    strings=parsed.get('strings')
    require(isinstance(strings,list),'Invalid embedded string dictionary')
    def expand(value):
        if isinstance(value,list):return [expand(item) for item in value]
        if isinstance(value,dict):
            if '$atlas_ref' in value:
                index=value['$atlas_ref']
                require(set(value)=={'$atlas_ref'} and type(index) is int and 0<=index<len(strings) and isinstance(strings[index],str),'Invalid embedded string reference')
                return strings[index]
            return {key:expand(item) for key,item in value.items()}
        return value
    result=expand(parsed['value'])
    require(hashlib.sha256(stable_bytes(result)).hexdigest()==parsed['expanded_canonical_sha256'],'Expanded payload identity changed')
    return result
class Page(HTMLParser):
    def __init__(self):super().__init__();self.scripts=[];self.script=None;self.csp=[];self.assets=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='script':self.script={'attrs':a,'text':''}
        if tag=='meta' and a.get('http-equiv','').lower()=='content-security-policy':self.csp.append(a.get('content',''))
        if tag in ['script','img','iframe','audio','video','source'] and a.get('src'):self.assets.append(a['src'])
        if tag=='link' and a.get('href'):self.assets.append(a['href'])
        if tag=='a' and a.get('href'):self.links.append(a['href'])
    def handle_data(self,data):
        if self.script is not None:self.script['text']+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.script is not None:self.scripts.append(self.script);self.script=None
def tracked_paths(root):
    p=subprocess.run(['git','-C',str(root),'ls-files','--cached','--others','--exclude-standard','-z'],capture_output=True)
    if p.returncode==0:return [Path(x) for x in p.stdout.decode().split('\0') if x]
    return [p.relative_to(root) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts]
def check(root,syntax=True):
    root=Path(root).resolve();site=root/'docs'
    baseline=json.loads((root/'project/asset-baseline.json').read_text())['assets']
    expected={x['path']:x for x in baseline}
    actual={p.relative_to(site).as_posix() for p in site.rglob('*') if p.is_file()}
    require(actual==set(expected),'Website file allowlist changed; review the publishing scope.')
    for rel,row in expected.items():
        p=site/rel;require(not p.is_symlink(),'Website symlink forbidden: '+rel)
        data=p.read_bytes();require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'Reviewed public asset changed: '+rel)
    denied={'.xlsx','.xls','.csv','.tsv','.zip','.pem','.key','.p12'}
    secret_patterns=[re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),re.compile(r'github_pat_[A-Za-z0-9_]{40,}'),re.compile(r'AKIA[0-9A-Z]{16}'),re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
    for rel in tracked_paths(root):
        p=root/rel
        require(not p.is_symlink(),'Tracked symlink requires an explicit portability review: '+str(rel))
        require(p.suffix.lower() not in denied and not p.name.startswith('.env'),'Private/credential/archive file forbidden in public Git: '+str(rel))
        require(not set(rel.parts)&{'authority','private','outputs','work','node_modules'},'Private/generated tree forbidden in public Git: '+str(rel))
        if p.is_file():
            text=p.read_text(errors='replace')
            require(not any(pat.search(text) for pat in secret_patterns),'Credential-like content requires private review: '+str(rel))
    node=shutil.which('node')
    if syntax:require(node is not None,'Node.js 22 or newer is required for syntax checks.')
    corpus=json.loads((root/'project/content-baseline.json').read_text())
    publication=json.loads((root/'project/public-copy-baseline.json').read_text()) if (root/'project/public-copy-baseline.json').exists() else None
    script_count=0
    for edition in ['primary','young-explorers']:
        page=Page();page.feed((site/edition/'index.html').read_text())
        require(len(page.scripts)==4,edition+': unexpected script ownership')
        require(not page.assets,edition+': expected self-contained embedded assets')
        require(any("connect-src 'none'" in v for v in page.csp),edition+': outbound connections are not disabled')
        data=[s for s in page.scripts if s['attrs'].get('id')=='atlas-pilot-data']
        require(len(data)==1,edition+': missing versioned pilot payload')
        packed=json.loads(data[0]['text'])
        approved_corpus=publication['editions'][edition] if publication else corpus['editions'][edition]
        require(packed.get('encoding')=='gzip-base64',edition+': unexpected payload encoding')
        raw=gzip.decompress(base64.b64decode(packed['payload'],validate=True))
        digest=hashlib.sha256(raw).hexdigest()
        require(digest==packed['sha256']==approved_corpus['payload_sha256'],edition+': reviewed payload identity changed')
        payload=expand_payload(json.loads(raw))
        require(hashlib.sha256(stable_bytes(payload)).hexdigest()==approved_corpus['expanded_canonical_sha256'],edition+': reviewed projection identity changed')
        identities=corpus['editions'][edition]['municipalities'];codes=set(identities)
        require(len(codes)==564 and len(set(identities.values()))==564,edition+': incomplete municipality baseline')
        require(set(payload['views'])==set(payload['view_guards'])==set(payload['editorial'])==codes,edition+': statewide town scope changed')
        require({c:e['municipality_id'] for c,e in payload['editorial'].items()}==identities,edition+': municipality identity changed')
        require(hashlib.sha256(stable_bytes(payload['editorial'])).hexdigest()==approved_corpus['editorial_sha256'],edition+': rewritten narratives changed')
        if publication:
            from project_public_copy import reader_copy,PROFILE_FIELDS,EVENT_FIELDS,SOURCE_FIELDS
            require(approved_corpus['before_editorial_sha256']==corpus['editions'][edition]['editorial_sha256'],edition+': frozen C57 binding changed')
            require(hashlib.sha256(stable_bytes(reader_copy(payload['editorial']))).hexdigest()==approved_corpus['reader_copy_sha256'],edition+': C57 reader text changed')
            for code,view in payload['views'].items():
                require(set(view['profile'])<=PROFILE_FIELDS|{'referent','earlier'},edition+': private profile field reintroduced')
                require(payload['view_guards'][code]==stable_bytes(view).decode(),edition+': public view guard mismatch')
                for event in view['events']:
                    require(set(event)<=EVENT_FIELDS,edition+': private event field reintroduced')
                    require(set(event.get('date_review',{}).get('expected_fields',{}))<=EVENT_FIELDS,edition+': private date guard field reintroduced')
                for source in view['sources'].values():
                    require(set(source)<=SOURCE_FIELDS,edition+': private source field reintroduced')
        for code,record in payload['editorial'].items():
            require(bool(record.get('preview','').strip()) and bool(record.get('paragraphs')) and all(p.strip() for p in record['paragraphs']),edition+': missing story or summary '+code)
            require(bool(record.get('journey')) and bool(record.get('sidebar')),edition+': missing journey or sidebar '+code)
        require(payload['source_workbook_sha256']==corpus['source_workbook_sha256'],edition+': workbook authority drift')
        require(payload['source_manifest_sha256']==corpus['source_manifest_sha256'],edition+': source authority drift')
        for s in page.scripts:
            if s['attrs'].get('type')=='application/json':continue
            script_count+=1
            if syntax:
                result=subprocess.run([node,'--check'],input=s['text'],text=True,capture_output=True)
                require(result.returncode==0,edition+': inline script syntax check failed')
    landing=Page();landing.feed((site/'index.html').read_text())
    require(landing.links==['./primary/','./young-explorers/'],'Edition chooser links must retain the project subpath.')
    return {'result':'PASS','public_assets':len(expected),'classic_scripts_checked':script_count,'current_profiles_per_edition':564,'narratives_per_edition':564,'historical_reviews_added':0}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=ap.parse_args()
    try:print(json.dumps(check(args.root)))
    except (CheckError,KeyError,ValueError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
