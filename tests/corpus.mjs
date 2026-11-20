import fs from 'node:fs';
import vm from 'node:vm';
import zlib from 'node:zlib';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

const baseline=JSON.parse(fs.readFileSync(new URL('../project/content-baseline.json',import.meta.url)));
const publication=JSON.parse(fs.readFileSync(new URL('../project/public-copy-baseline.json',import.meta.url)));
let assertions=0;
const check=(value,label)=>{assert.ok(value,label);assertions++;};
const canonical=value=>Array.isArray(value)?value.map(canonical):value&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])])):value;
const hash=value=>createHash('sha256').update(JSON.stringify(canonical(value))).digest('hex');
// Preserve lexical key order even for municipality codes that JS treats as integer keys.
const canonicalJSON=value=>Array.isArray(value)?'['+value.map(canonicalJSON).join(',')+']':value&&typeof value==='object'?'{'+Object.keys(value).sort().map(key=>JSON.stringify(key)+':'+canonicalJSON(value[key])).join(',')+'}':JSON.stringify(value);
const projectionHash=value=>createHash('sha256').update(canonicalJSON(value)).digest('hex');
let primaryEditorial;
for(const edition of ['primary','young-explorers']){
  const html=fs.readFileSync(new URL(`../docs/${edition}/index.html`,import.meta.url),'utf8');
  const packed=JSON.parse(html.match(/<script id="atlas-pilot-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  const decoderCode=html.slice(html.indexOf('async function decodeAtlasPacked('),html.indexOf('\n  let data;'));
  const decode=vm.runInNewContext(decoderCode+';decodeAtlasPacked;',{Uint8Array,atob,Response,Blob,DecompressionStream,TextDecoder,TextEncoder,crypto:globalThis.crypto});
  const payload=await decode(packed.payload,packed.sha256);
  const approved=publication.editions[edition];
  check(projectionHash(payload)===approved.expanded_canonical_sha256,'reviewed public projection identity '+edition);
  await assert.rejects(decode(packed.payload,'wrong'),/identity/);assertions++;
  for(const invalid of [{$atlas_ref:-1},{$atlas_ref:0,extra:true}]){
    const wrapper={atlas_string_dictionary:1,strings:[],value:invalid};
    const raw=Buffer.from(JSON.stringify(wrapper));
    await assert.rejects(decode(zlib.gzipSync(raw).toString('base64'),createHash('sha256').update(raw).digest('hex')),/reference/);assertions++;
  }
  const coreCode=html.slice(html.indexOf('function createAtlasPilotCore('),html.indexOf('\n  const packedPayload='));
  const makeCore=vm.runInNewContext(coreCode+';createAtlasPilotCore;');
  const core=makeCore(payload,{});
  const overlayPacked=JSON.parse(html.split('  const packedCategoryOverlay=')[1].split(';\n')[0]);
  const overlay=await decode(overlayPacked.payload,overlayPacked.sha256);
  check(hash(overlay)===approved.overlay_sha256,'reviewed category overlay binding '+edition);
  const semantics=overlay.rows.map(({expected_data,...row})=>row);
  check(hash(semantics)===approved.overlay_semantics_sha256,'all Review27 decisions unchanged '+edition);
  const readerCopy=structuredClone(payload.editorial);
  for(const record of Object.values(readerCopy)){delete record.expected_data;delete record.sidebar.expected_data;}
  check(projectionHash(readerCopy)===approved.reader_copy_sha256,'reader fields match C57 plus explicit copy proposals '+edition);
  check(approved.before_editorial_sha256===baseline.editions[edition].editorial_sha256,'frozen C57 source identity '+edition);
  const helper=html.slice(html.indexOf('function applyReviewedCategoryOverlay('),html.indexOf('\n\n  const packedCategoryOverlay='));
  const apply=vm.runInNewContext(helper+';applyReviewedCategoryOverlay;');
  const themes=vm.runInNewContext(html.match(/const themes=\[[\s\S]*?\n  \];/)[0]+';themes;');
  const labels=Object.fromEntries(themes.map(t=>[t.id,t.label]));
  const source=Object.fromEntries(Object.keys(payload.views).map(code=>[code,core.profileFor(code)]));
  const original=JSON.stringify(source);
  const profiles=apply(source,core,payload,overlay,labels);
  check(Object.keys(profiles).length===564,'564 runtime profiles '+edition);
  check(overlay.rows.length===baseline.mappings,'all reviewed category mappings '+edition);
  const counts={};
  for(const code of Object.keys(profiles)){
    const editorial=core.editorialFor(code);
    check(!!editorial,'actual story guard accepts '+edition+code);
    check(core.previewFor(code,edition)===editorial.preview,'actual summary selects rewritten text '+edition+code);
    check(core.journeyFor(code).length===editorial.journey.length,'actual journey selects rewritten frames '+edition+code);
    counts[profiles[code].current_origin]=(counts[profiles[code].current_origin]||0)+1;
  }
  check(hash(counts)===hash(baseline.category_counts),'all seven category counts '+edition);
  const sample=Object.keys(payload.editorial)[0];
  const retained=payload.editorial[sample];
  for(const [field,value] of Object.entries({expected_data:'stale',source_manifest_sha256:'wrong',source_workbook_sha256:'wrong',version:'C15'})){
    payload.editorial[sample]={...retained,[field]:value};
    check(core.editorialFor(sample)===null,'stale narrative rejected '+edition+field);
  }
  payload.editorial[sample]=retained;
  check(core.editorialFor(sample)===retained,'valid narrative restored '+edition);
  const view=payload.views[sample],name=view.profile.name;
  view.profile.name='Synthetic stale public view';
  check(core.editorialFor(sample)===null,'changed projected context rejects story '+edition);
  view.profile.name=name;
  check(core.editorialFor(sample)===retained,'restored projected context accepts story '+edition);
  const dated=view.events.find(event=>event.date_review);
  if(dated){
    const action=dated.action;
    check(core.dateFor(dated)===dated.date_review.display+(dated.date_review.held?' · unverified lead':''),'qualified display date preserved '+edition);
    dated.action='Synthetic stale date context';
    check(core.dateFor(dated)===String(dated.date||'Date not established'),'stale public date context rejected '+edition);
    dated.action=action;
  }
  for(const row of overlay.rows)check(profiles[row.code].current_origin===row.group,'reviewed category applied '+edition+row.code);
  // Exercise rejection against the actual guarded helper with isolated source records.
  const guarded={...core,validView:code=>!!payload.view_guards[code]};
  for(const row of overlay.rows){
    for(const [field,value] of Object.entries({municipality_id:'wrong',expected_category:'wrong',expected_data:'stale',expected_origin:(row.expected_origin??'other')==='other'?'people':'other',group:'__proto__'})){
      const changed={...overlay,rows:[{...row,[field]:value}]};
      check(apply(source,guarded,payload,changed,labels)[row.code]===source[row.code],'stale category rejected '+edition+row.code+field);
    }
    check(apply(source,guarded,payload,{...overlay,rows:[row,row]},labels)[row.code]===source[row.code],'duplicate category rejected '+edition+row.code);
  }
  check(JSON.stringify(source)===original,'source records unchanged '+edition);
  const code=Object.keys(payload.editorial)[0];
  const stale={...payload,editorial:{...payload.editorial,[code]:{...payload.editorial[code],expected_data:'stale'}}};
  check(makeCore(stale,{}).editorialFor(code)===null,'stale narrative rejected '+edition);
  if(edition==='primary')primaryEditorial=payload.editorial;
  else {
    check(Object.keys(payload.editorial).every(c=>JSON.stringify(payload.editorial[c].paragraphs)!==JSON.stringify(primaryEditorial[c].paragraphs)),'every Young story retains its separate adaptation');
    const youngContent=JSON.parse(html.split('  const youngContent = ')[1].split('\n/* Pure guards')[0].trim().replace(/;$/,''));
    const resolverCode=html.slice(html.indexOf('function createYoungLessonResolver('),html.indexOf('\n\n  const youngLessons='));
    const resolver=vm.runInNewContext(resolverCode+';createYoungLessonResolver;')(youngContent,payload,core);
    for(const [code,lesson] of Object.entries(youngContent.stories)){
      check(resolver.lessonFor(code)===lesson,'original Young activity retained '+code);
      const expected=lesson.guard.expected_data;
      lesson.guard.expected_data='stale';
      check(resolver.lessonFor(code)===null,'stale Young binding rejected '+code);
      lesson.guard.expected_data=expected;
    }
  }
}
console.log(JSON.stringify({status:'PASS',assertions,profiles_per_edition:564,mappings:179,scope:'Actual runtime story/category guards with isolated data; no browser notes accessed.'}));
