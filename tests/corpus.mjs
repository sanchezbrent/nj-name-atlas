import fs from 'node:fs';
import vm from 'node:vm';
import zlib from 'node:zlib';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

const baseline=JSON.parse(fs.readFileSync(new URL('../project/content-baseline.json',import.meta.url)));
let assertions=0;
const check=(value,label)=>{assert.ok(value,label);assertions++;};
const canonical=value=>Array.isArray(value)?value.map(canonical):value&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])])):value;
const hash=value=>createHash('sha256').update(JSON.stringify(canonical(value))).digest('hex');
let primaryEditorial;
for(const edition of ['primary','young-explorers']){
  const html=fs.readFileSync(new URL(`../docs/${edition}/index.html`,import.meta.url),'utf8');
  const packed=JSON.parse(html.match(/<script id="atlas-pilot-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  const decoderCode=html.slice(html.indexOf('async function decodeAtlasPacked('),html.indexOf('\n  let data;'));
  const decode=vm.runInNewContext(decoderCode+';decodeAtlasPacked;',{Uint8Array,atob,Response,Blob,DecompressionStream,TextDecoder,TextEncoder,crypto:globalThis.crypto});
  const payload=await decode(packed.payload,packed.sha256);
  check(createHash('sha256').update(JSON.stringify(payload)).digest('hex')===baseline.editions[edition].expanded_payload_sha256,'lossless original payload identity '+edition);
  await assert.rejects(decode(packed.payload,'wrong'),/identity/);assertions++;
  for(const invalid of [{$atlas_ref:-1},{$atlas_ref:0,extra:true}]){
    const wrapper=JSON.parse(zlib.gunzipSync(Buffer.from(packed.payload,'base64')));wrapper.value=invalid;
    const raw=Buffer.from(JSON.stringify(wrapper));
    await assert.rejects(decode(zlib.gzipSync(raw).toString('base64'),createHash('sha256').update(raw).digest('hex')),/reference/);assertions++;
  }
  const coreCode=html.slice(html.indexOf('function createAtlasPilotCore('),html.indexOf('\n  const packedPayload='));
  const makeCore=vm.runInNewContext(coreCode+';createAtlasPilotCore;');
  const core=makeCore(payload,{});
  const overlayPacked=JSON.parse(html.split('  const packedCategoryOverlay=')[1].split(';\n')[0]);
  const overlay=await decode(overlayPacked.payload,overlayPacked.sha256);
  check(createHash('sha256').update(JSON.stringify(overlay)).digest('hex')===baseline.overlay_sha256,'lossless category overlay identity '+edition);
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
  else check(Object.keys(payload.editorial).every(c=>JSON.stringify(payload.editorial[c].paragraphs)!==JSON.stringify(primaryEditorial[c].paragraphs)),'every Young story retains its separate adaptation');
}
console.log(JSON.stringify({status:'PASS',assertions,profiles_per_edition:564,mappings:179,scope:'Actual runtime story/category guards with isolated data; no browser notes accessed.'}));
