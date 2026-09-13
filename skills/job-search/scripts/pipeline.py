#!/usr/bin/env python3
"""Observed milestones and confirmed-submission cohort summaries."""
import argparse
import json
from datetime import datetime
import workspace as ws

MILESTONES={'discovered_at','qualified_at','materials_ready_at','submitted_at'}


def moment(value):
    ws.stamp(value,'observation');return datetime.fromisoformat(value.replace('Z','+00:00'))


def validate(state):
    sources=ws.indexed(state['sources'],'sources')
    for app in state['applications']:
        milestones=app.get('milestones',{})
        ws.require(isinstance(milestones,dict) and set(milestones).issubset(MILESTONES),'Unknown milestone fields.')
        for name,record in milestones.items():
            ws.require(isinstance(record,dict),'Milestone needs an observation record.')
            when=moment(record.get('at'));ws.require(when<=moment(ws.now()),'A milestone cannot be observed in the future.')
            ws.refs(record.get('source_ids'),sources,'Milestone observation')
            if name=='submitted_at':
                receipt=app.get('submission')
                ws.require(receipt and moment(receipt['confirmed_at'])==when and set(record['source_ids']).issubset(receipt['source_ids']),'Submitted milestone requires the matching employer-confirmed receipt and its sources.')
        for label in ('discovery_source','application_channel'):
            if label in app:ws.require(isinstance(app[label],str) and app[label].strip(),'Channel labels must be nonempty strings when known.')


def guard_history(old,new):
    applications={a['id']:a for a in new['applications']}
    for app in old['applications']:
        for key,value in app.get('milestones',{}).items():
            ws.require(app['id'] in applications and applications[app['id']].get('milestones',{}).get(key)==value,'Observed milestones are immutable; preserve history and add a sourced correction note.')


def observe(value,application_id,milestone,source_id,observed_at=None):
    state=ws.load(value);app=next((a for a in state['applications'] if a['id']==application_id),None)
    ws.require(app is not None and milestone in MILESTONES,'Known application and milestone required.')
    if milestone=='submitted_at' and observed_at is None:
        ws.require(app.get('submission'),'No confirmed submission receipt.');observed_at=app['submission']['confirmed_at']
    record={'at':observed_at or ws.now(),'source_ids':[source_id]}
    existing=app.setdefault('milestones',{}).get(milestone)
    if existing:
        ws.require(existing==record or (observed_at is None and existing['source_ids']==[source_id]),'Milestone already observed; preserve it.');return {'observation':existing,'revision':state['revision']}
    app['milestones'][milestone]=record
    saved=ws.commit(value,state,state['revision'],'Recorded sourced observation: '+milestone)
    return {'observation':record,'revision':saved['revision'],'limitation':'Source references establish traceability; the helper cannot prove that a prose source describes the claimed event.'}


def metrics(value,start,end):
    state=ws.load(value);lo,hi=moment(start),moment(end);ws.require(lo<hi,'Cohort end must follow start.')
    cohort=[a for a in state['applications'] if a.get('submission') and lo<=moment(a['submission']['confirmed_at'])<hi]
    n=len(cohort);counts={outcome:sum(a['outcome']==outcome for a in cohort) for outcome in sorted(ws.OUTCOMES)}
    return {'cohort':{'from_inclusive':start,'to_exclusive':end,'basis':'employer-confirmed submission time'},'confirmed_submissions':n,
            'application_ids':[a['id'] for a in cohort],'current_outcomes':counts,'current_outcome_rates':{k:v/n if n else None for k,v in counts.items()},
            'small_sample':n<20,'small_sample_definition':'Fewer than 20 confirmed submissions; descriptive label, not a significance test.',
            'limitation':'Current outcome snapshot, not transition history, hiring probability or causal evidence. Missing/unverified submissions are excluded.'}


def main():
    ws.configure_output();p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('observe');a.add_argument('--workspace',required=True);a.add_argument('--application',required=True);a.add_argument('--milestone',choices=sorted(MILESTONES),required=True);a.add_argument('--source-id',required=True);a.add_argument('--observed-at')
    a=sub.add_parser('metrics');a.add_argument('--workspace',required=True);a.add_argument('--from',dest='start',required=True);a.add_argument('--to',dest='end',required=True)
    a=p.parse_args()
    try:
        result=observe(a.workspace,a.application,a.milestone,a.source_id,a.observed_at) if a.command=='observe' else metrics(a.workspace,a.start,a.end)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ws.WorkspaceError,OSError,ValueError,KeyError,TypeError) as e:print('Pipeline operation refused: '+str(e));return 2

if __name__=='__main__':raise SystemExit(main())
