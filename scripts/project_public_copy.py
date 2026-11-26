#!/usr/bin/env python3
"""Make a review candidate from the pinned pre-remediation public assets.

This is a structural projection, NOT editorial or publication clearance. It never
opens or writes a workbook. Inputs must be a separate, unchanged source checkout.
Remaining reader-language candidates are intentionally left for contextual review.
"""
import argparse
import base64
import copy
import gzip
import hashlib
import json
import re
from pathlib import Path

from check_project import Page, expand_payload, stable_bytes

EDITIONS = ('primary', 'young-explorers')
PROFILE_FIELDS = frozenset('name form category etymology_status county code municipal_code municipality_id current_origin current_origin_label source_ids urls'.split())
EVENT_FIELDS = frozenset('id municipality date year precision before after type actor action significance sources urls municipality_ids version date_review'.split())
SOURCE_FIELDS = frozenset('id author title publication url'.split())
# Exact reviewed label approvals contain hashes, never private before text.
REVIEWED_JOURNEY_LABELS = {
    ('editorial','0810','journey',0,'names',0):
        ('1adcf6732cab0e465f15d22a2af586d85cea0b650552aa76044948b9541cb49c',
         'Manteskÿl (reported form, provisional)'),
}



def digest(value):
    return hashlib.sha256(stable_bytes(value)).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def pack(value):
    raw = compact(value).encode()
    return {'encoding': 'gzip-base64', 'sha256': hashlib.sha256(raw).hexdigest(),
            'payload': base64.b64encode(gzip.compress(raw, mtime=0)).decode()}


def unpack(wrapper):
    raw = gzip.decompress(base64.b64decode(wrapper['payload'], validate=True))
    if hashlib.sha256(raw).hexdigest() != wrapper['sha256']:
        raise ValueError('Source packed identity mismatch')
    return expand_payload(json.loads(raw))


def literal(html, name):
    match = re.search(r'\bconst ' + re.escape(name) + r'\s*=\s*', html)
    if not match:
        raise ValueError('Missing literal: ' + name)
    value, size = json.JSONDecoder().raw_decode(html[match.end():])
    return value, match.end(), match.end() + size


def replace_literal(html, name, value):
    _, start, end = literal(html, name)
    return html[:start] + compact(value) + html[end:]


def reader_copy(editorial):
    """Exclude ONLY guard bindings, retaining every C57 reader text and metadata."""
    result = copy.deepcopy(editorial)
    for record in result.values():
        record.pop('expected_data')
        record['sidebar'].pop('expected_data')
    return result


def project_payload(original):
    projected = copy.deepcopy(original)
    projected['public_projection'] = 'publication-boundary-v1'
    projected['source_field_guards'] = {}
    for code, view in original['views'].items():
        # Hashes retain source comparison bindings without shipping raw wording.
        projected['source_field_guards'][code] = {
            field: digest(value) for field, value in view['profile'].items()
        }
        profile = {key: value for key, value in view['profile'].items() if key in PROFILE_FIELDS}
        # These are exact existing C57 reader strings, not new interpretations.
        profile['referent'] = original['editorial'][code]['preview']
        profile['earlier'] = '; '.join(dict.fromkeys(
            name for frame in original['editorial'][code]['journey'] for name in frame['names']))
        events = []
        for event in view['events']:
            public = {key: copy.deepcopy(value) for key, value in event.items() if key in EVENT_FIELDS}
            review = public.get('date_review')
            if review:
                # Preserve displayed date, held status, kind and every retained
                # expected field; private note/grade fields leave both sides.
                review['expected_fields'] = {
                    key: value for key, value in review['expected_fields'].items()
                    if key in EVENT_FIELDS and key != 'date_review'
                }
            events.append(public)
        sources = {sid: {key: value for key, value in source.items() if key in SOURCE_FIELDS}
                   for sid, source in view['sources'].items()}
        public_view = {'profile': profile, 'events': events, 'sources': sources}
        projected['views'][code] = public_view
        guard = stable_bytes(public_view).decode()
        projected['view_guards'][code] = guard
        projected['editorial'][code]['expected_data'] = guard
        projected['editorial'][code]['sidebar']['expected_data'] = guard
    if reader_copy(projected['editorial']) != reader_copy(original['editorial']):
        raise ValueError('C57 reader text changed during structural projection')
    return projected


def apply_copy_corrections(payload, edition, corrections):
    """Apply individually recorded proposals; refuse stale or out-of-scope fields."""
    count=0
    seen=set()
    allowed_event={'date','precision','type','before','after','actor','action','significance'}
    for row in corrections.get('changes',[]):
        if row['edition']!=edition:continue
        path=row['path']; code=row['code']
        if code not in corrections['towns'] or path[1]!=code:
            raise ValueError('Copy correction outside the explicit town scope')
        key=tuple(path)
        if key in seen:raise ValueError('Duplicate copy correction')
        seen.add(key)
        allowed=path[0]=='editorial' and (
            (len(path)==3 and path[2]=='preview') or
            (len(path)==4 and path[2]=='paragraphs' and type(path[3]) is int) or
            (len(path)==5 and path[2]=='journey' and path[-1] in {'date','label','detail'}) or
            (len(path)==6 and path[2:4]==['sidebar','fields'] and path[-1] in {'label','text'}))
        # General journey names remain protected. A reviewed qualifier may
        # change only at its exact target, original hash and approved wording.
        approved_label=REVIEWED_JOURNEY_LABELS.get(tuple(path))
        if approved_label:
            allowed=(row['expected_sha256'],row['replacement'])==approved_label
        if path[0]=='views':
            allowed=(path[2]=='events' and (path[-1] in allowed_event or path[-2:]==['date_review','display'])) or (path[2]=='sources' and path[-1] in {'author','title','publication'}) or (len(path)==4 and path[2]=='profile' and path[-1] in {'earlier','referent'})
        if not allowed:raise ValueError('Protected field in copy correction')
        parent=payload
        for part in path[:-1]:parent=parent[part]
        before=parent[path[-1]];after=row['replacement']
        if not isinstance(before,str) or not isinstance(after,str) or digest(before)!=row['expected_sha256']:
            raise ValueError('Stale copy correction: '+edition+' '+str(path))
        if path==['views',code,'profile','referent'] and after!=payload['editorial'][code].get('preview'):
            raise ValueError('Public profile summary must match the reviewed editorial preview')
        if path[0]=='views' and path[2]=='events' and path[-1]=='date':
            if re.findall(r'\d+',before)!=re.findall(r'\d+',after):
                raise ValueError('Historical date digits changed by copy correction')
        parent[path[-1]]=after;count+=1
        if path[0]=='views' and path[2]=='events' and len(path)==5:
            review=parent.get('date_review')
            if review and path[-1] in review['expected_fields']:
                if review['expected_fields'][path[-1]]!=before:raise ValueError('Stale date-context binding')
                review['expected_fields'][path[-1]]=after
    for code,view in payload['views'].items():
        payload['view_guards'][code]=stable_bytes(view).decode()
        payload['editorial'][code]['expected_data']=payload['view_guards'][code]
        payload['editorial'][code]['sidebar']['expected_data']=payload['view_guards'][code]
    return count


def apply_auxiliary_copy_corrections(bundle, owner, edition, corrections):
    """Guard reader text in discovery cards and Young activities separately."""
    seen = set()
    changed_lessons = set()
    count = 0
    for row in corrections.get('auxiliary_changes', []):
        if row.get('owner') not in {'discovery', 'youngContent'}:
            raise ValueError('Unknown auxiliary copy owner')
        if row['edition'] != edition or row['owner'] != owner:
            continue
        path, code = row['path'], row['code']
        if code not in corrections['towns']:
            raise ValueError('Auxiliary copy outside town scope')
        key = tuple(path)
        if key in seen:
            raise ValueError('Duplicate auxiliary copy correction')
        seen.add(key)
        allowed = False
        if owner == 'discovery':
            if len(path) == 5 and path[0] == 'tours' and path[2] == 'stops' and path[-1] == 'text':
                allowed = bundle['tours'][path[1]]['stops'][path[3]]['code'] == code
            elif len(path) == 3 and path[0] == 'connections' and path[-1] == 'text':
                item = bundle['connections'][path[1]]
                allowed = code in (item['a'], item['b'])
        elif owner == 'youngContent' and len(path) >= 3 and path[:2] == ['stories', code]:
            allowed = ((len(path) == 3 and path[2] in {'intro', 'evidence', 'uncertain'}) or
                       (len(path) == 5 and path[2] == 'moments' and type(path[3]) is int and path[4] == 2))
        if not allowed:
            raise ValueError('Protected field in auxiliary copy correction')
        if owner == 'youngContent' and code not in changed_lessons:
            lesson = bundle['stories'][code]
            public = {k: v for k, v in lesson.items() if k not in {'guard', 'version'}}
            if lesson['guard']['expected_lesson'] != stable_bytes(public).decode():
                raise ValueError('Stale Young activity content binding')
            changed_lessons.add(code)
        parent = bundle
        for part in path[:-1]:
            parent = parent[part]
        before, after = parent[path[-1]], row['replacement']
        if not isinstance(before, str) or not isinstance(after, str) or digest(before) != row['expected_sha256']:
            raise ValueError('Stale auxiliary copy correction')
        parent[path[-1]] = after
        count += 1
    for code in changed_lessons:
        lesson = bundle['stories'][code]
        lesson['guard']['expected_lesson'] = stable_bytes({k: v for k, v in lesson.items() if k not in {'guard', 'version'}}).decode()
    return count


def project_html(html, edition=None, corrections=None):
    page = Page()
    page.feed(html)
    original = unpack(json.loads(next(s['text'] for s in page.scripts
                                     if s['attrs'].get('id') == 'atlas-pilot-data')))
    projected = project_payload(original)
    structural_reader_hash=digest(reader_copy(projected['editorial']))
    correction_count=apply_copy_corrections(projected,edition,corrections) if corrections else 0
    old_wrapper = next(s['text'] for s in page.scripts if s['attrs'].get('id') == 'atlas-pilot-data')
    html = html.replace(old_wrapper, compact(pack(projected)), 1)

    # The legacy dataset is overwritten for all 564 towns. Only map geometry,
    # county counts and retrieval date still have active consumers.
    pattern = r'data=await decodeAtlasPacked\(("[^"]+"),"([a-f0-9]+)"\)'
    match = re.search(pattern, html)
    if not match:
        raise ValueError('Missing legacy map payload')
    legacy = unpack({'payload': json.loads(match[1]), 'sha256': match[2]})
    map_data = {key: legacy[key] for key in ('geography', 'counties', 'context', 'counts', 'boundary_retrieved')}
    map_data.update(profiles={}, events=[])
    packed_map = pack(map_data)
    html = html[:match.start()] + ('data=await decodeAtlasPacked(' + compact(packed_map['payload']) +
                                  ',' + compact(packed_map['sha256']) + ')') + html[match.end():]

    overlay, _, _ = literal(html, 'packedCategoryOverlay')
    overlay = unpack(overlay)
    old_overlay_semantics = [{key: value for key, value in row.items() if key != 'expected_data'} for row in overlay['rows']]
    for row in overlay['rows']:
        if row['expected_data'] != original['view_guards'][row['code']]:
            raise ValueError('Source Review27 guard mismatch')
        row['expected_data'] = projected['view_guards'][row['code']]
    html = replace_literal(html, 'packedCategoryOverlay', pack(overlay))

    # These three fallback stores are unreachable for every current municipality.
    # Do not ship their older research wording merely to support dead branches.
    for name, empty in [('presentationEdits', {}), ('curated', {}), ('storyHookData', {'hooks': []})]:
        html = replace_literal(html, name, empty)
    # readerText/readerNote have been identity functions since statewide C57.
    html, count = re.subn(r'  const readerEdits=new Map\(\[[\s\S]*?\n  function readerText', '  function readerText', html, count=1)
    if count != 1:
        raise ValueError('Missing retired reader/note replacement dictionaries')

    discovery, _, _ = literal(html, 'discovery')
    auxiliary_count = 0
    for item in discovery['connections'] + [stop for tour in discovery['tours'] for stop in tour['stops']]:
        for binding in item.get('basis', []):
            binding['value_guard'] = digest(binding.pop('value'))
        code=item.get('code',item.get('a'))
        if corrections and code in corrections['towns'] and item.get('event') and item.get('eventAction'):
            source_event=next((e for e in original['views'][code]['events'] if e['id']==item['event']),None)
            public_event=next((e for e in projected['views'][code]['events'] if e['id']==item['event']),None)
            if source_event and public_event and item['eventAction']==source_event['action']:
                item['eventAction']=public_event['action']
    if corrections:
        auxiliary_count += apply_auxiliary_copy_corrections(discovery, 'discovery', edition, corrections)
    html = replace_literal(html, 'discovery', discovery)
    before = "profiles[b.code]?.[b.field]===b.value"
    after = "typeof b.value_guard==='string'&&pilotPayload.source_field_guards?.[b.code]?.[b.field]===b.value_guard"
    if html.count(before) != 1:
        raise ValueError('Unexpected discovery guard owner')
    html = html.replace(before, after, 1)

    # Remove the public disclosure and its private content owner, not just CSS.
    html, count = re.subn(r"    if\(sidebar\)\{\n      const originals=el\('details',[\s\S]*?\n    \}\n    const sourceBody=", '    const sourceBody=', html, count=1)
    if count != 1:
        raise ValueError('Unexpected original-wording disclosure owner')
    html = html.replace("sidebar?'More about '+p.name+'’s name and history.':'Research wording is retained below, including earlier statements and later qualifications. The shorter story above is shown only where its current evidence check passes.'", "'More about '+p.name+'’s name and history.'")

    if 'const youngContent = ' in html:
        young, _, _ = literal(html, 'youngContent')
        young['researchEdition'] = 'Stories and activities for young explorers'
        for code, lesson in young['stories'].items():
            if lesson['guard']['expected_data'] != original['view_guards'][code]:
                raise ValueError('Source Young lesson guard mismatch')
            lesson['guard']['expected_data'] = projected['view_guards'][code]
        if corrections:
            auxiliary_count += apply_auxiliary_copy_corrections(young, 'youngContent', edition, corrections)
        html = replace_literal(html, 'youngContent', young)

    return html, {
        'expanded_canonical_sha256': digest(projected),
        'payload_sha256': pack(projected)['sha256'],
        'editorial_sha256': digest(projected['editorial']),
        'reader_copy_sha256': digest(reader_copy(projected['editorial'])),
        'frozen_reader_copy_sha256': structural_reader_hash,
        'before_editorial_sha256': digest(original['editorial']),
        'overlay_sha256': digest(overlay),
        'overlay_semantics_sha256': digest(old_overlay_semantics),
        'municipalities': {c: e['municipality_id'] for c, e in projected['editorial'].items()},
        'events': sum(len(view['events']) for view in projected['views'].values()),
        'sources': sum(len(view['sources']) for view in projected['views'].values()),
        'source_input_writes': 0,
        'copy_correction_fields': correction_count,
        'auxiliary_copy_correction_fields': auxiliary_count,
        'exact_C57_reader_records':sum(reader_copy({c:original['editorial'][c]})==reader_copy({c:projected['editorial'][c]}) for c in original['editorial']),
        'contextual_review_complete': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    parser.add_argument('--corrections',type=Path)
    args = parser.parse_args()
    source, output = args.source_root.resolve(), args.output_root.resolve()
    if source == output:
        parser.error('Use a separate immutable input checkout')
    baseline = json.loads((source / 'project/asset-baseline.json').read_text())
    approved = {row['path']: row for row in baseline['assets']}
    corrections=json.loads(args.corrections.read_text()) if args.corrections else None
    report = {'stage': 'STRUCTURAL_CANDIDATE_ONLY', 'release_status': 'BLOCKED', 'editions': {}}
    if corrections:
        report.update(stage=corrections['checkpoint'].replace('PUBLIC_COPY_','COPY_PROPOSALS_CHECKPOINT_',1),corrections_sha256=digest(corrections),owner_approval=False)
    for edition in EDITIONS:
        rel = edition + '/index.html'
        raw = (source / 'docs' / rel).read_bytes()
        if hashlib.sha256(raw).hexdigest() != approved[rel]['sha256']:
            raise ValueError('Source asset is not the pinned pre-remediation edition')
        html, details = project_html(raw.decode(),edition,corrections)
        (output / 'docs' / rel).write_text(html)
        details['before_asset_sha256'] = approved[rel]['sha256']
        details['after_asset_sha256'] = hashlib.sha256(html.encode()).hexdigest()
        details['before_bytes'] = len(raw)
        details['after_bytes'] = len(html.encode())
        report['editions'][edition] = details
    (output / 'project/public-copy-baseline.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'CANDIDATE_WRITTEN', 'publication_cleared': False}))


if __name__ == '__main__':
    main()
