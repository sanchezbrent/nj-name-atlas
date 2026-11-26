"""Protect auxiliary identities and content bindings when changing reader prose."""
import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_project import stable_bytes
from project_public_copy import apply_auxiliary_copy_corrections,digest

class AuxiliaryCopyTests(unittest.TestCase):
    def proposal(self,owner,path,before,after,code='0001'):
        return {'towns':['0001'],'auxiliary_changes':[dict(owner=owner,edition='young-explorers',code=code,path=path,expected_sha256=digest(before),replacement=after)]}
    def test_discovery_text_keeps_holds_and_evidence_bindings(self):
        item=dict(code='0001',text='Synthetic process text',event='T1',eventAction='Reported action',basis=[{'value_guard':'retained'}],release_disposition='HELD_PENDING_CURRENT_COPY_REVIEW')
        bundle={'tours':[{'stops':[copy.deepcopy(item)]}]};rows=self.proposal('discovery',['tours',0,'stops',0,'text'],item['text'],'Reported naming account.')
        apply_auxiliary_copy_corrections(bundle,'discovery','young-explorers',rows)
        self.assertEqual(bundle['tours'][0]['stops'][0],dict(item,text='Reported naming account.'))
        for path in [['tours',0,'stops',0,'event'],['tours',0,'stops',0,'release_disposition'],['tours',0,'stops',0,'basis']]:
            with self.subTest(path=path),self.assertRaisesRegex(ValueError,'Protected'):
                apply_auxiliary_copy_corrections(bundle,'discovery','young-explorers',self.proposal('discovery',path,'old','new'))
    def test_stale_duplicate_unknown_owner_and_wrong_identity_rejected(self):
        bundle={'connections':[dict(a='0001',b='0002',text='Original account')]}
        good=self.proposal('discovery',['connections',0,'text'],'Original account','Reported account')
        variants=[]
        stale=copy.deepcopy(good);stale['auxiliary_changes'][0]['expected_sha256']=digest('different');variants.append(stale)
        duplicate=copy.deepcopy(good);duplicate['auxiliary_changes']*=2;variants.append(duplicate)
        unknown=copy.deepcopy(good);unknown['auxiliary_changes'][0]['owner']='other';variants.append(unknown)
        wrong=copy.deepcopy(good);wrong['towns']=['0003'];wrong['auxiliary_changes'][0]['code']='0003';variants.append(wrong)
        for rows in variants:
            with self.subTest(rows=rows),self.assertRaises(ValueError):apply_auxiliary_copy_corrections(copy.deepcopy(bundle),'discovery','young-explorers',rows)
    def test_young_prose_rebinds_only_current_content_and_keeps_protected_fields(self):
        lesson=dict(intro='Synthetic process text',moments=[['1849','Station','Reported account']],event_ids=['T1'],sources=[['S1','Source']],version='C21')
        lesson['guard']=dict(expected_lesson=stable_bytes({k:v for k,v in lesson.items() if k!='version'}).decode(),expected_data='source-binding',source_manifest_sha256='manifest',source_workbook_sha256='workbook')
        original=copy.deepcopy(lesson);bundle={'stories':{'0001':lesson}}
        rows=self.proposal('youngContent',['stories','0001','intro'],lesson['intro'],'Reported naming account.')
        apply_auxiliary_copy_corrections(bundle,'youngContent','young-explorers',rows)
        self.assertEqual(lesson['guard']['expected_lesson'],stable_bytes({k:v for k,v in lesson.items() if k not in {'guard','version'}}).decode())
        self.assertEqual({k:v for k,v in lesson['guard'].items() if k!='expected_lesson'},{k:v for k,v in original['guard'].items() if k!='expected_lesson'})
        for path in [['stories','0001','event_ids'],['stories','0001','sources'],['stories','0001','moments',0,0],['stories','0001','guard','expected_lesson']]:
            with self.subTest(path=path),self.assertRaisesRegex(ValueError,'Protected'):
                apply_auxiliary_copy_corrections(copy.deepcopy(bundle),'youngContent','young-explorers',self.proposal('youngContent',path,'old','new'))
        stale=copy.deepcopy(bundle);stale['stories']['0001']['guard']['expected_lesson']='stale'
        with self.assertRaisesRegex(ValueError,'content binding'):
            apply_auxiliary_copy_corrections(stale,'youngContent','young-explorers',self.proposal('youngContent',['stories','0001','intro'],lesson['intro'],'Other prose'))

if __name__=='__main__':unittest.main()
