#!/usr/bin/env python3
"""Check and retain evidence of saved application-form completeness; no browser access."""
import argparse
import hashlib
import json
import sys
from datetime import datetime
import workspace as ws

CHECKS = ('identity_contact', 'work_history', 'education', 'profile_links_skills',
          'answers_dates', 'attachments', 'saved_final_review', 'consent')
HISTORY = ('work_history', 'education')
EXCLUDED_APP_FIELDS = {'form_review', 'stage', 'outcome', 'outcome_source_ids',
                       'posting_status', 'posting_source_ids', 'next_action',
                       'milestones', 'submission'}


class StaleFormReview(ws.WorkspaceError):
    """An otherwise valid saved review no longer matches its candidate context."""


def application(state, aid):
    return ws.indexed(state['applications'], 'applications').get(aid)


def context_hash(state, app):
    value = {'workspace_id': state['workspace_id'], 'profile': state['profile'],
             'experiences': state.get('onboarding', {}).get('experiences', []),
             'application': {k: v for k, v in app.items() if k not in EXCLUDED_APP_FIELDS}}
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()


def text(value, label):
    ws.require(isinstance(value, str) and value.strip(), label + ': nonempty text required.')


def labels(value, label):
    ws.require(isinstance(value, list), label + ': list required.')
    for item in value:
        text(item, label)
    ws.require(len(set(value)) == len(value), label + ': duplicate entry.')
    return set(value)


def validate_record(record, state, root, app, current=True):
    ws.require(isinstance(record, dict) and record.get('schema_version') == 1,
               'Form review schema_version must be 1.')
    ws.require(record.get('application') == app['id'], 'Form review belongs to another application.')
    ws.require(record.get('workspace_id') == state['workspace_id'], 'Form review belongs to another workspace.')
    ws.stamp(record.get('reviewed_at'), 'reviewed_at')
    ws.require(datetime.fromisoformat(record['reviewed_at'].replace('Z', '+00:00')) <=
               datetime.fromisoformat(ws.now()), 'Review cannot be in the future.')
    text(record.get('review_url'), 'review_url'); ws.canonical(record['review_url'])
    text(record.get('context_sha256'), 'context_sha256')
    sources = ws.indexed(state['sources'], 'sources')
    ws.refs(record.get('inventory_source_ids'), sources, 'Independent expected inventory')
    evidence = record.get('evidence_files')
    ws.require(isinstance(evidence, list) and evidence, 'Retained live saved-form evidence required.')
    for ref in evidence:
        ws.file_ref(root, ref, 'Saved-form evidence')
    checks = record.get('checks')
    ws.require(isinstance(checks, dict) and set(checks) == set(CHECKS), 'All eight form checks required.')
    for name, item in checks.items():
        ws.require(isinstance(item, dict), name + ': check object required.')
        ws.require(item.get('status') in ('verified', 'not_applicable'), name + ': unresolved check.')
        text(item.get('evidence'), name + ' observed evidence')
        if item['status'] == 'not_applicable':
            ws.require(name not in ('identity_contact', 'saved_final_review'), name + ': cannot be skipped.')
            text(item.get('reason'), name + ' limitation')
            ws.require(item.get('candidate_disclosed') is True, name + ': limitation must be disclosed.')

    exclusions = record.get('exclusions', [])
    ws.require(isinstance(exclusions, list), 'exclusions must be a list.')
    excluded = {name: set() for name in HISTORY}
    for item in exclusions:
        ws.require(isinstance(item, dict) and item.get('section') in HISTORY, 'Invalid inventory exclusion.')
        text(item.get('id'), 'Excluded entry'); text(item.get('reason'), 'Exclusion reason')
        ws.refs(item.get('source_ids'), sources, 'Employer/candidate exclusion instruction')
        ws.require(item.get('candidate_disclosed') is True, 'Inventory exclusions must be disclosed.')
        group = excluded[item['section']]
        ws.require(item['id'] not in group, 'Duplicate inventory exclusion.'); group.add(item['id'])
    for name in HISTORY:
        expected = labels(record.get('expected_' + name), 'Expected ' + name)
        observed = labels(record.get('observed_' + name), 'Observed ' + name)
        ws.require(excluded[name] <= expected, 'Excluded entry not present in expected inventory.')
        ws.require(expected - excluded[name] == observed, name + ': expected/saved entries differ.')
        status = checks[name]['status']
        ws.require(bool(observed) == (status == 'verified'),
                   name + ': empty/absent section needs an explained not_applicable check; populated sections must be verified.')

    fields = record.get('fields')
    ws.require(isinstance(fields, list) and fields, 'Field-by-field saved-value review required.')
    ids = set()
    for field in fields:
        ws.require(isinstance(field, dict), 'Invalid field review.')
        text(field.get('id'), 'Field ID'); text(field.get('label'), 'Field label')
        ws.require(field['id'] not in ids, 'Duplicate field ID.'); ids.add(field['id'])
        ws.require(field.get('section') in CHECKS, 'Unknown field section.')
        ws.require(field.get('requirement') in ('required', 'recommended', 'optional'), 'Invalid field requirement.')
        ws.require(isinstance(field.get('supported'), bool), 'Field supported must be boolean.')
        ws.require(field.get('status') in ('verified', 'omitted', 'not_applicable'), 'Field is unresolved.')
        text(field.get('evidence'), 'Field saved-value observation')
        if field['status'] == 'verified':
            ws.require(field['supported'], 'A verified field needs a truthful supported answer.')
            text(field.get('expected_value'), 'Expected field value')
            text(field.get('saved_value'), 'Saved field value')
            ws.require(field['expected_value'] == field['saved_value'], 'Expected/saved field values differ: ' + field['label'])
        else:
            text(field.get('reason'), 'Field omission reason')
            ws.require(field['requirement'] != 'required' or field['status'] == 'not_applicable',
                       'A required field cannot be left unanswered.')
            if field['supported'] or field['requirement'] != 'optional':
                ws.refs(field.get('source_ids'), sources, 'Field exclusion/limitation evidence')
                ws.require(field.get('candidate_disclosed') is True, 'Supported/recommended field omission must be disclosed.')
    for name in CHECKS:
        if checks[name]['status'] == 'verified':
            ws.require(any(f['section'] == name for f in fields), name + ': missing field observations.')
    if current and record['context_sha256'] != context_hash(state, app):
        raise StaleFormReview('Application ' + app['id'] + ': form review is stale. '
            'Keep it preparing until the saved form is re-inspected and a fresh review is saved.')
    return record


def check_state(state, root, app):
    pointer = app.get('form_review')
    ws.require(isinstance(pointer, dict), 'Saved-form completeness review missing; keep the application preparing.')
    source = ws.indexed(state['sources'], 'sources').get(pointer.get('source_id'))
    ws.require(source and source['kind'] == 'document' and
               all(pointer.get(k) == source[k] for k in ('file', 'sha256')), 'Form review must match its registered source.')
    ws.file_ref(root, pointer, 'Form completeness review')
    record = json.loads(ws.inside(root, pointer['file']).read_text(encoding='utf-8-sig'))
    return validate_record(record, state, root, app)


def guard_commit(old, new, root):
    old_apps = ws.indexed(old['applications'], 'applications')
    stale = []
    for app in new['applications']:
        previous = old_apps.get(app['id'], {})
        # Old unreviewed records stay readable. New/changed readiness must pass.
        needs_ready = app['stage'] == 'ready' and (app != previous or
            (app.get('form_review') and context_hash(old, previous) != context_hash(new, app)))
        if needs_ready or app.get('form_review') != previous.get('form_review'):
            try:
                check_state(new, root, app)
            except StaleFormReview:
                stale.append(app['id'])
    if stale:
        raise StaleFormReview('Applications ' + ', '.join(stale) + ' have stale form reviews. '
            'Keep your intended edits; move affected ready applications to preparing in the same draft, '
            'then re-inspect their saved forms and save fresh reviews. '
            'Use form_review.py commit-update --workspace W --draft scratch/update.json '
            '--expected-revision N to save the update and move only existing ready applications '
            'with stale reviews to preparing. A changed review pointer itself must be fresh.')


def commit_update(root, draft, expected):
    """Apply an intended state update and explicitly invalidate affected readiness."""
    old = ws.load(root)
    ws.require(old['revision'] == expected, 'Revision conflict: reread current records and merge intended edits.')
    ws.require(draft.startswith('scratch/'), 'Prepare the updated state JSON in workspace scratch.')
    state = json.loads(ws.inside(root, draft).read_text(encoding='utf-8-sig'))
    ws.validate(state, root)
    ws.require(state['revision'] == expected, 'Draft revision must match the state you read.')
    previous = ws.indexed(old['applications'], 'applications'); demoted = []
    for app in state['applications']:
        prior = previous.get(app['id'], {})
        if (app['stage'] == prior.get('stage') == 'ready' and app.get('form_review') and
                app['form_review'] == prior.get('form_review')):
            try:
                check_state(state, root, app)
            except StaleFormReview:
                app['stage'] = 'preparing'
                app['next_action'] = ('Re-inspect the saved form and save a fresh completeness review. '
                                      'Then: ' + app['next_action'])
                demoted.append(app['id'])
    summary = 'Saved intended update; stale form reviews moved to preparing: ' + (', '.join(demoted) or 'none')
    saved = ws.commit(root, state, expected, summary)
    return {'status': 'UPDATED', 'revision': saved['revision'], 'demoted_applications': demoted,
            'next_action': 'Re-inspect these applications and save fresh reviews before readiness.' if demoted else 'Continue the saved next action.'}


def save(root, aid, draft, expected):
    state = ws.load(root); app = application(state, aid)
    ws.require(app is not None, 'Unknown application.')
    ws.require(state['revision'] == expected, 'Revision conflict: reread current records.')
    ws.require(draft.startswith('scratch/'), 'Prepare the review JSON in workspace scratch.')
    path = ws.inside(root, draft)
    record = json.loads(path.read_text(encoding='utf-8-sig'))
    validate_record(record, state, root, app)
    digest = ws.digest(path); sid = 'form-' + digest[:32]
    ref = ws.import_file(root, path, f'applications/{aid}/form-reviews/{digest}.json')
    pointer = dict(ref, source_id=sid)
    if app.get('form_review') == pointer:
        return {'review': pointer, 'revision': expected, 'status': 'PASS'}
    source = {'id': sid, 'kind': 'document', 'recorded_at': ws.now(), **ref}
    if app.get('form_review'):
        source['previous_source_id'] = app['form_review']['source_id']
    ws.require(sid not in ws.indexed(state['sources'], 'sources'), 'Review already registered; create a fresh observation.')
    state['sources'].append(source); app['form_review'] = pointer
    saved = ws.commit(root, state, expected, 'Recorded saved-form completeness review')
    return {'status': 'PASS', 'review': pointer, 'revision': saved['revision']}


def main():
    ws.configure_output()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=('context', 'save', 'check', 'commit-update'))
    p.add_argument('--workspace', required=True); p.add_argument('--application')
    p.add_argument('--draft'); p.add_argument('--expected-revision', type=int)
    a = p.parse_args()
    try:
        root = ws.checked_root(a.workspace); state = ws.load(root)
        if a.command == 'commit-update':
            ws.require(a.application is None, 'commit-update applies a state draft; omit --application.')
            ws.require(a.draft is not None and a.expected_revision is not None, 'commit-update needs --draft and --expected-revision.')
            result = commit_update(root, a.draft, a.expected_revision)
        else:
            ws.require(a.application is not None, a.command + ' needs --application.')
            app = application(state, a.application)
            ws.require(app is not None, 'Unknown application.')
        if a.command == 'context':
            result = {'workspace_id': state['workspace_id'], 'application': app['id'],
                      'context_sha256': context_hash(state, app), 'revision': state['revision']}
        elif a.command == 'save':
            ws.require(a.draft is not None and a.expected_revision is not None, 'save needs --draft and --expected-revision.')
            result = save(root, a.application, a.draft, a.expected_revision)
        elif a.command == 'check':
            check_state(state, root, app)
            result = {'status': 'PASS', 'application': app['id'], 'review': app['form_review']}
        result['limitation'] = 'Checks retained evidence, not the browser itself. Inspect the current saved form; final submission authorization is separate.'
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (ws.WorkspaceError, OSError, ValueError, TypeError, KeyError) as e:
        print(json.dumps({'status': 'FAIL', 'error': str(e)}, ensure_ascii=False), file=sys.stderr); return 2


if __name__ == '__main__':
    raise SystemExit(main())
