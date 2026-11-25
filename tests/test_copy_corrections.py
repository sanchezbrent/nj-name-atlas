"""Reject stale, duplicate or protected edits in explicit copy proposal application."""
import copy,sys,unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from project_public_copy import apply_copy_corrections,digest,REVIEWED_JOURNEY_LABELS

class CopyCorrectionTests(unittest.TestCase):
 def setUp(self):
  self.payload={'views':{'0001':{'profile':{'earlier':'Old Name'},'events':[{'id':'T1','year':1928,'date':'1928-03-12 (reported; original uninspected)','action':'Synthetic source-process wording','sources':'S1','date_review':{'display':'1928-03-12 (reported; original uninspected)','expected_fields':{'action':'Synthetic source-process wording','date':'1928-03-12 (reported; original uninspected)'}}}],'sources':{}}},'editorial':{'0001':{'sidebar':{},'paragraphs':['Original story']}},'view_guards':{}}
 def proposal(self,path,before,after):return {'towns':['0001'],'changes':[{'edition':'primary','code':'0001','path':path,'expected_sha256':digest(before),'replacement':after}]}
 def test_profile_summary_follows_reviewed_preview(self):
  self.payload['views']['0001']['profile'].update(referent='Old process summary',source_ids='S1')
  self.payload['editorial']['0001']['preview']='A reported naming account.'
  row=self.proposal(['views','0001','profile','referent'],'Old process summary','A reported naming account.')
  stale=copy.deepcopy(row);stale['changes'][0]['expected_sha256']=digest('A different summary')
  with self.assertRaisesRegex(ValueError,'Stale'):apply_copy_corrections(copy.deepcopy(self.payload),'primary',stale)
  apply_copy_corrections(self.payload,'primary',row)
  self.assertEqual(self.payload['views']['0001']['profile']['referent'],self.payload['editorial']['0001']['preview'])
  self.assertEqual(self.payload['views']['0001']['profile']['source_ids'],'S1')
 def test_profile_projection_remains_restricted(self):
  self.payload['views']['0001']['profile'].update(referent='Old summary',source_ids='S1')
  self.payload['editorial']['0001']['preview']='Reviewed summary'
  for field,before,after,message in [('referent','Old summary','Unrelated summary','must match'),('source_ids','S1','S2','Protected')]:
   with self.subTest(field=field):
    row=self.proposal(['views','0001','profile',field],before,after)
    with self.assertRaisesRegex(ValueError,message):apply_copy_corrections(copy.deepcopy(self.payload),'primary',row)
 def test_exact_proposal_rebinds_date_context(self):
  row=self.proposal(['views','0001','events',0,'action'],'Synthetic source-process wording','A reported naming account.')
  apply_copy_corrections(self.payload,'primary',row)
  event=self.payload['views']['0001']['events'][0]
  self.assertEqual(event['date_review']['expected_fields']['action'],event['action'])
  self.assertEqual((event['id'],event['year'],event['sources']),('T1',1928,'S1'))
 def test_stale_source_rejected(self):
  row=self.proposal(['editorial','0001','paragraphs',0],'Wrong old story','New story')
  with self.assertRaisesRegex(ValueError,'Stale'):apply_copy_corrections(self.payload,'primary',row)
 def test_protected_year_rejected(self):
  row=self.proposal(['views','0001','events',0,'year'],1928,'1929')
  with self.assertRaisesRegex(ValueError,'Protected'):apply_copy_corrections(self.payload,'primary',row)
 def test_editorial_guard_edit_rejected(self):
  row=self.proposal(['editorial','0001','sidebar','expected_data'],'old','new')
  with self.assertRaisesRegex(ValueError,'Protected'):apply_copy_corrections(self.payload,'primary',row)
 def test_date_digits_cannot_change(self):
  row=self.proposal(['views','0001','events',0,'date'],'1928-03-12 (reported; original uninspected)','1929-03-12 (reported)')
  with self.assertRaisesRegex(ValueError,'date digits'):apply_copy_corrections(self.payload,'primary',row)
 def test_duplicate_target_rejected(self):
  row=self.proposal(['editorial','0001','paragraphs',0],'Original story','New story');row['changes']*=2
  with self.assertRaisesRegex(ValueError,'Duplicate'):apply_copy_corrections(self.payload,'primary',row)
 def test_unscoped_town_rejected(self):
  row=self.proposal(['editorial','0001','paragraphs',0],'Original story','New story');row['towns']=[]
  with self.assertRaisesRegex(ValueError,'scope'):apply_copy_corrections(self.payload,'primary',row)
 def test_other_edition_not_changed(self):
  row=self.proposal(['editorial','0001','paragraphs',0],'Original story','New story')
  apply_copy_corrections(self.payload,'young-explorers',row)
  self.assertEqual(self.payload['editorial']['0001']['paragraphs'],['Original story'])
 def test_reviewed_journey_qualifier_preserves_historical_name_and_context(self):
  path=['editorial','0810','journey',0,'names',0]
  before='Synthetic Name (process qualifier)';after='Synthetic Name (reported, provisional)'
  approval={tuple(path):(digest(before),after)}
  for edition in ['primary','young-explorers']:
   with self.subTest(edition=edition),patch.dict(REVIEWED_JOURNEY_LABELS,approval,clear=True):
    payload=copy.deepcopy(self.payload)
    payload['views']['0810']=payload['views'].pop('0001')
    payload['editorial']['0810']=payload['editorial'].pop('0001')
    payload['editorial']['0810']['journey']=[{'names':[before,'Another name'],'date':'1655 (reported)'}]
    protected=copy.deepcopy(payload['views']['0810'])
    corrections={'towns':['0810'],'changes':[{'edition':edition,'code':'0810','path':path,'expected_sha256':digest(before),'replacement':after}]}
    apply_copy_corrections(payload,edition,corrections)
    self.assertEqual(payload['editorial']['0810']['journey'],[{'names':[after,'Another name'],'date':'1655 (reported)'}])
    self.assertEqual(payload['views']['0810'],protected)
 def test_journey_name_exception_rejects_identity_scope_and_stale_changes(self):
  path=['editorial','0810','journey',0,'names',0]
  expected,after=REVIEWED_JOURNEY_LABELS[tuple(path)]
  base={'edition':'primary','code':'0810','path':path,'expected_sha256':expected,'replacement':after}
  variants=[dict(base,replacement='Another historical name'),dict(base,expected_sha256=digest('A different original')),dict(base,path=['editorial','0810','journey',0,'names',1]),dict(base,code='0001',path=['editorial','0001','journey',0,'names',0])]
  for row in variants:
   with self.subTest(row=row):
    with self.assertRaisesRegex(ValueError,'Protected'):apply_copy_corrections(copy.deepcopy(self.payload),'primary',{'towns':['0810','0001'],'changes':[row]})
  payload=copy.deepcopy(self.payload)
  payload['views']['0810']=payload['views'].pop('0001')
  payload['editorial']['0810']=payload['editorial'].pop('0001')
  payload['editorial']['0810']['journey']=[{'names':['An unrelated actual original']}]
  with self.assertRaisesRegex(ValueError,'Stale'):apply_copy_corrections(payload,'primary',{'towns':['0810'],'changes':[base]})

if __name__=='__main__':unittest.main()
