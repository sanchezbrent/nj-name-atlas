#!/usr/bin/env python3
"""Write a PRIVATE pending-review ledger; never treats machine inventory as sign-off."""
import argparse
import json
from collections import Counter
from pathlib import Path

from audit_public_copy import check_edition, find_candidates, strings_with_paths
from check_project import Page
from project_public_copy import unpack, reader_copy


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--private-output',type=Path,required=True)
    parser.add_argument('--review-records',type=Path)
    args=parser.parse_args()
    root=args.root.resolve(); output=args.private_output.resolve()
    if output==root or root in output.parents:
        parser.error('Private review output must be outside the public repository')
    output.mkdir(parents=True,exist_ok=True)
    reviews=json.loads(args.review_records.read_text()) if args.review_records else {}
    records=[]; aggregate={}
    for edition in ('primary','young-explorers'):
        page=Page();page.feed((root/'docs'/edition/'index.html').read_text())
        payload=unpack(json.loads(next(s['text'] for s in page.scripts if s['attrs'].get('id')=='atlas-pilot-data')))
        editorial=reader_copy(payload['editorial'])
        for code, view in payload['views'].items():
            review_view=json.loads(json.dumps(view))
            for event in review_view['events']:
                event.pop('date_review',None)  # Same context already present above, not a separate reader field.
            context={'editorial':editorial[code],'public_view':review_view}
            candidates=[]
            for path,text in strings_with_paths(context,'town.'+code):
                rules=find_candidates(text)
                if rules:
                    candidates.append({'path':path,'rules':rules,'exact_public_candidate':text,
                                       'treatment':'PENDING_CONTEXTUAL_EDITORIAL_REVIEW',
                                       'evidence_checked':False,'resolution':None})
            review=reviews.get(edition,{}).get(code)
            records.append({'edition':edition,'code':code,'municipality_id':view['profile']['municipality_id'],
                            'name':view['profile']['name'],'county':view['profile']['county'],
                            'machine_inventory':'COMPLETE','manual_review':'AGENT_TEXT_REVIEW_COMPLETE; HUMAN_AND_RENDER_REVIEW_PENDING' if review else 'NOT_STARTED',
                            'human_sign_off':False,'citation_verification':'PENDING',
                            'candidate_fields':candidates,'contextual_review_record':review})
        findings=check_edition(root,edition)
        aggregate[edition]={'machine_inventoried':564,'manual_reviewed':0,'signed_off':0,
                            'agent_text_reviewed':len(reviews.get(edition,{})),
                            'heuristic_candidates':len(findings),
                            'by_rule':dict(Counter(row['rule'] for row in findings))}
    checkpoint=json.loads((root/'project/public-copy-corrections.json').read_text())['checkpoint'] if reviews else None
    ledger={'stage':checkpoint.replace('PUBLIC_COPY_','COPY_PROPOSALS_CHECKPOINT_',1) if checkpoint else 'STRUCTURAL_CANDIDATE_ONLY','release':'BLOCKED','records':records,
            'scope_note':'This inventory is not a contextual or human review. Guard repetitions are excluded from per-town excerpts; the complete bundle scan counts them.',
            'aggregate':aggregate}
    (output/'Pending_Review_Ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    (output/'Aggregate_Review_Status.json').write_text(json.dumps({'release':'BLOCKED','editions':aggregate},indent=2)+'\n')
    print(json.dumps({'town_edition_records':len(records),'manual_sign_offs':0,'editions':aggregate}))


if __name__=='__main__':
    main()
