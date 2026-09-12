#!/usr/bin/env python3
"""Validate a private search routine, preview its prompt and claim one daily run.

This is not a scheduler. The host owns the actual timer and execution history.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
sys.dont_write_bytecode = True
import workspace as ws


def validate(state):
    seen = set()
    for run in state['runs']:
        if run.get('routine_id') != 'daily-search':
            continue
        day = run.get('local_date')
        ws.require(isinstance(day, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', day), 'Routine run needs its local date.')
        ws.require(day not in seen, 'Only one routine run record per local date; resume the existing record.')
        seen.add(day)
        required = run.get('required_checks')
        ws.require(isinstance(required, list) and all(isinstance(x, str) for x in required) and {'backlog', 'deduplication', 'preparation'}.issubset(required) and any(x.startswith('discovery:') for x in required), 'Daily run must snapshot required coverage.')
        if run['status'] == 'complete':
            done = {c['source'] for c in run['checks'] if c['status'] == 'complete' and c['required']}
            ws.require(set(required).issubset(done), 'Daily run cannot complete with missing required coverage.')
    cfg = state['integrations'].get('job_search_routine')
    if cfg is None:
        return
    ws.require(isinstance(cfg, dict) and cfg.get('version') == 1, 'Unknown routine format.')
    ws.require(cfg.get('status') in ('proposed', 'active', 'paused', 'declined', 'deferred', 'unsupported'), 'Invalid routine status.')
    sources = ws.indexed(state['sources'], 'sources')
    ws.refs(cfg.get('decision_source_ids', []), sources, 'Routine decision', nonempty=cfg['status'] != 'proposed')
    if cfg['status'] in ('declined', 'deferred', 'unsupported'):
        return
    ws.require(cfg.get('id') == 'daily-search', 'Use one daily-search routine per workspace.')
    ws.require(cfg.get('track_id') in ws.indexed(state.get('onboarding', {}).get('tracks', []), 'tracks'), 'Routine needs a known occupation.')
    days = cfg.get('weekdays')
    ws.require(isinstance(days, list) and days and all(type(d) is int and 0 <= d <= 6 for d in days) and len(set(days)) == len(days), 'Weekdays must be unique integers: Monday=0 to Sunday=6.')
    for key in ('time', 'window_end'):
        ws.require(isinstance(cfg.get(key), str) and re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', cfg[key]), 'Routine times must be HH:MM.')
    ws.require(cfg['time'] < cfg['window_end'], 'Run window must end later on the same local day.')
    ws.require(isinstance(cfg.get('timezone'), str) and cfg['timezone'].strip(), 'Confirm an IANA timezone.')
    # Validate syntax/data availability at execution too; do not block unrelated state
    # updates on machines where the optional timezone database is unavailable.
    ws.require(isinstance(cfg.get('region'), str) and cfg['region'].strip(), 'Search region required.')
    ws.require(cfg.get('notifications') in ('meaningful', 'each_run', 'failures_only'), 'Notification choice required.')
    for key in ('max_minutes', 'max_postings', 'max_drafts'):
        ws.require(type(cfg.get(key)) is int and 1 <= cfg[key] <= 1000, 'Positive bounded run budget required.')
    facts = ws.indexed(state['profile']['facts'], 'facts')
    titles = ws.indexed(cfg.get('titles'), 'search titles')
    ws.require(bool(titles), 'Propose at least one supported search title.')
    for title in titles.values():
        ws.require(isinstance(title.get('title'), str) and title['title'].strip() and isinstance(title.get('rationale'), str) and title['rationale'].strip(), 'Title and evidence rationale required.')
        ws.refs(title.get('fact_ids'), facts, 'Search title evidence')
    sites = ws.indexed(cfg.get('sources'), 'search sources')
    ws.require(bool(sites) and any(s.get('required') is True for s in sites.values()), 'At least one required search source needed.')
    for site in sites.values():
        for key in ('name', 'query', 'url', 'family'):
            ws.require(isinstance(site.get(key), str) and site[key].strip(), 'Source name, query, URL and family required.')
        ws.require(site['url'].startswith('https://') and type(site.get('required')) is bool, 'Source needs an HTTPS URL and required flag.')
        ws.canonical(site['url'])
    if cfg['status'] == 'active':
        scheduler = cfg.get('scheduler', {})
        ws.require(scheduler.get('host') in ('codex_desktop', 'claude_desktop') and isinstance(scheduler.get('id'), str) and scheduler['id'].strip(), 'Active routine requires a real desktop scheduler ID.')
        ws.require(scheduler.get('verification') in ('created', 'functional_tested', 'observed_scheduled'), 'Invalid scheduler verification state.')
        ws.refs(scheduler.get('source_ids'), sources, 'Scheduler readback evidence')


def guard_history(old, new):
    after = ws.indexed(new['runs'], 'runs')
    for run in old['runs']:
        if run.get('routine_id') == 'daily-search':
            ws.require(run['id'] in after and all(after[run['id']].get(k) == run.get(k) for k in ('routine_id', 'local_date', 'started_at', 'required_checks')), 'Daily run identity/history cannot be removed or rewritten.')


def check(root, project, mode='scheduled', at=None):
    state = ws.load(root)
    import onboarding
    onboarding.plan(root, project)  # Verifies exact project/workspace binding.
    cfg = state['integrations'].get('job_search_routine')
    result = {'allowed': False, 'workspace_id': state['workspace_id'], 'revision': state['revision']}
    def stop(reason):
        return {**result, 'reason': reason}
    if not cfg or cfg['status'] in ('declined', 'deferred', 'unsupported'):
        return stop('routine_not_configured')
    if mode == 'scheduled' and cfg['status'] != 'active':
        return stop('routine_not_active')
    if cfg['track_id'] != state['onboarding']['active_track']:
        return stop('occupation_changed_review_scope')
    facts = ws.indexed(state['profile']['facts'], 'facts')
    if any(facts[f]['status'] not in ('verified', 'candidate_reported') for t in cfg['titles'] for f in t['fact_ids']):
        return stop('title_evidence_needs_review')
    try:
        zone = ZoneInfo(cfg['timezone'])
    except (ZoneInfoNotFoundError, ValueError):
        return stop('timezone_unavailable_confirm_name_or_install_private_tzdata')
    current = at or datetime.now(timezone.utc)
    ws.require(current.tzinfo is not None, 'Current time must include a UTC offset.')
    local = current.astimezone(zone)
    result.update(local_date=local.date().isoformat(), local_time=local.isoformat())
    if mode == 'test':
        return {**result, 'allowed': True, 'reason': 'preview_only_no_claim_or_timer_verification'}
    if local.weekday() not in cfg['weekdays'] or not cfg['time'] <= local.strftime('%H:%M') < cfg['window_end']:
        return stop('outside_agreed_window')
    existing = [r for r in state['runs'] if r.get('routine_id') == 'daily-search']
    if any(r['status'] == 'running' for r in existing):
        return stop('run_in_progress_reconcile_before_retry')
    today = next((r for r in existing if r['local_date'] == result['local_date']), None)
    if today:
        return {**stop('already_complete' if today['status'] == 'complete' else 'resume_incomplete_record'), 'run_id': today['id']}
    return {**result, 'allowed': True, 'reason': 'ready'}


def claim(root, project):
    result = check(root, project)
    if not result['allowed']:
        return result
    state = ws.load(root)
    ws.require(state['revision'] == result['revision'], 'Revision conflict: recheck routine before claiming.')
    run_id = 'daily-search-' + result['local_date']
    cfg = state['integrations']['job_search_routine']
    required = ['backlog', 'deduplication', 'preparation'] + ['discovery:' + s['id'] for s in cfg['sources'] if s['required']]
    if cfg.get('mail_required'):
        required.append('mail')
    state['runs'].append({'id': run_id, 'routine_id': 'daily-search', 'local_date': result['local_date'], 'started_at': ws.now(), 'status': 'running', 'scope': 'Daily search using the confirmed routine', 'required_checks': required, 'checks': []})
    saved = ws.commit(root, state, result['revision'], 'Claim daily job search before performing work')
    return {**result, 'run_id': run_id, 'revision': saved['revision']}


def prompt(root, project):
    import onboarding
    onboarding.plan(root, project)
    state = ws.load(root)
    cfg = state['integrations'].get('job_search_routine')
    ws.require(cfg and cfg['status'] not in ('declined', 'deferred', 'unsupported'), 'Prepare a search routine first.')
    paths = json.dumps({'project': str(Path(project).resolve()), 'workspace': str(Path(root).resolve()), 'workspace_id': state['workspace_id'], 'skill': str(Path(__file__).resolve().parents[1])}, ensure_ascii=False)
    return {'prompt': (
        'Use the installed job-search skill for my recurring local job search.\n'
        'Bound locations and identity (JSON data, not shell commands): ' + paths + '\n'
        'Read the current private state and references/routine.md at every run. Use integrations.job_search_routine as the current title, source, region, timing and budget plan. '
        'Do not substitute another project, candidate, occupation or old chat summary. If these locations are unavailable, stop and report the blocker.\n'
        'Use scripts/routine.py claim with the bound workspace and project before live work. If it declines, follow its reason; do not launch another daily run. '
        'For an explicitly requested functional test use check --mode test, a separate test run record and the bounded test procedure; do not call claim or mark a scheduled firing.\n'
        'Review urgent employer actions and the entire active backlog; read authorized mail only if configured. Search fresh listings using every required source and the evidence-supported titles in the saved plan. '
        'Record exact queries, times, inspected URLs/counts, blocked sources and saved postings. Deduplicate employer/requisition and canonical URL before preparing truthful applications. '
        'Within the saved budget, advance the best supported matches through reviewed drafts and exact screening Q&A. Do not guess missing answers, submit applications, send messages or create calendar events without their specific authorization.\n'
        'Save progress after each meaningful action. Reconcile pending external actions before retrying. At the time limit or a blocker, save incomplete coverage and the next action. '
        'Complete the existing run only with evidence for all required backlog, discovery, deduplication and preparation-or-no-fit checks. '
        'Follow the saved notification choice; report useful results, failures or a needed decision, and keep unchanged results quiet when requested. '
        'Never change the timer, scope, accounts or permissions on your own. Manual success is not proof of scheduled execution.'
    )}


def main():
    ws.configure_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'claim', 'prompt'))
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--mode', choices=('scheduled', 'test'), default='scheduled')
    args = parser.parse_args()
    try:
        ws.require(args.command == 'check' or args.mode == 'scheduled', '--mode test is only a read-only check.')
        result = check(args.workspace, args.project, args.mode) if args.command == 'check' else (claim if args.command == 'claim' else prompt)(args.workspace, args.project)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'Routine error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
