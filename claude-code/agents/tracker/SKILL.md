---
name: tracker
description: Application pipeline tracker. Log applications, update status, check follow-ups, generate summaries. Manages data/tracker.tsv. Run /tracker or /status.
---

# Tracker Agent

Manages the application pipeline.
All data stored in `data/tracker.tsv`.
Syncs to Notion if the connector is active.

---

## tracker.tsv Structure

```
company  role  applied_date  status  follow_up_date  notes  link
```

Status values: `applied` | `followed_up` | `interview_scheduled` | `interview_done` | `offer` | `rejected` | `ghosted` | `withdrawn`

---

## Commands

### Log a new application

```bash
python scripts/tracker.py --add \
  --company "SDAIA" \
  --role "AI Research Intern" \
  --date "2026-06-01" \
  --link "https://sdaia.gov.sa/careers/job/123" \
  --notes "Applied via careers page, no connection found"
```

Or in conversation: *"Log that I applied to SDAIA for the AI intern role today"*

### Update status

```bash
python scripts/tracker.py --update --company "SDAIA" --status "interview_scheduled" \
  --notes "Interview on June 10, technical + HR"
```

### Show pipeline

```bash
python scripts/tracker.py --list
```

### Show follow-ups due

```bash
python scripts/tracker.py --followups
```

---

## Follow-Up Schedule

Default schedule after applying:
- **+7 days:** First follow-up (if no reply)
- **+14 days:** Second follow-up (if still no reply)
- **+21 days:** Mark as ghosted, move on

When logging an application, automatically set:
`follow_up_date = applied_date + 7 days`

When follow-up is sent, update:
`follow_up_date = today + 7 days`

---

## `/status` Output

```
## Pipeline Status — [date]

Total applications: [N]
Active: [N] (applied, followed up, interview stages)
Closed: [N] (offer, rejected, withdrawn, ghosted)

Follow-ups due today or overdue:
- [Company] — [Role] — applied [date] — [N] days since last contact

This week's priority:
- Follow up: [Company A] — sent [date]
- Apply to: [Company B] — shortlisted, not applied yet
- Prepare for: [Company C] — interview on [date]

At risk of going cold (no contact in 14+ days):
- [Company] — consider moving to ghosted
```

---

## `/tracker` Full View

```
## Full Pipeline

| Company | Role | Applied | Status | Follow-up | Notes |
|---|---|---|---|---|---|
| SDAIA | AI Intern | 2026-06-01 | applied | 2026-06-08 | Via careers page |
| STC | SW Eng Intern | 2026-06-03 | interview_scheduled | 2026-06-10 | Interview June 10 |
| Lean | Backend Intern | 2026-05-28 | followed_up | 2026-06-04 | No reply yet |
| KAUST | Research Intern | 2026-05-20 | ghosted | — | No reply in 3 weeks |
```

---

## Notion Sync

If the Notion connector is active:

```
sync to Notion → Internship Pipeline database
Fields: Company, Role, Applied Date, Status, Follow-up Date, Notes, Link
```

Sync runs automatically when `--sync` flag is passed to tracker.py,
or manually triggered with: *"Sync my pipeline to Notion"*

---

## Application Folder Structure

Each application gets its own folder in `data/applications/`:

```
data/applications/sdaia-ai-intern/
├── cv_tailored.md          ← Tailored CV for this role
├── cv_tailored.tex         ← LaTeX version (compile locally)
├── cover_letter.md         ← Cover letter
├── ats_answers.md          ← ATS answer sheet
├── outreach_recruiter.md   ← Cold message to recruiter
└── research_brief.md       ← Company research brief
```

Create folder when starting an application:
```bash
mkdir -p data/applications/[company-slug]
```
