"""Reject stale, duplicate or protected edits in explicit copy proposal application."""
import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from project_public_copy import apply_copy_corrections,digest

class CopyCorrectionTests(unittest.TestCase):
 def setUp(self):
  self.payload={'views':{'0001':{'profile':{'earlier':'Old Name'},'events':[{'id':'T1','year':1928,'date':'1928-03-12 (reported; original uninspected)','action':'Synthetic source-process wording','sources':'S1','date_review':{'display':'1928-03-12 (reported; original uninspected)','expected_fields':{'action':'Synthetic source-process wording','date':'1928-03-12 (reported; original uninspected)'}}}],'sources':{}}},'editorial':{'0001':{'sidebar':{},'paragraphs':['Original story']}},'view_guards':{}}
 def proposal(self,path,before,after):return {'towns':['0001'],'changes':[{'edition':'primary','code':'0001','path':path,'expected_sha256':digest(before),'replacement':after}]}
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

if __name__=='__main__':unittest.main()
