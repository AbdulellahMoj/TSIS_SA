# TSIS_SA — Technical Students Internship Strategist (Saudi Arabia)
![TSIS_SA header](assets/tsis_header.svg)

A lot of computer science and technical students in Saudi struggle to find internships.
Not because they're not capable — but because the hiring ecosystem is noisy and opaque:
companies post inconsistently, ATS filters block qualified applicants, cold outreach is ignored,
and many opportunities live behind networks and local processes.

TSIS_SA packages an AI-powered internship strategist that guides students through the
entire pipeline — from profile building and CV tailoring, to searching, ATS prep,
automated form-filling (where available), outreach, and tracking.

What this repo helps you do (quick overview):
1. Build a full Work History Document from your CV and projects
2. Tailor CV bullets and generate a LaTeX PDF
3. Score and rank opportunities (Fit Scoring)
4. Search jobs across boards and company career pages
5. Produce ATS answer-sheets and optionally auto-fill forms with Playwright
6. Draft personalised outreach and cover letters
7. Track applications, reminders, and follow-ups
8. Export or sync data to Notion or CSV

---

## Two Options — pick what suits you

Option A — claude.ai (Quick, no local setup)
- Install the Claude skill and run the strategist directly in claude.ai (free or Pro).
- Best for students who want immediate interactive help without installing anything.

Quick steps:
1. Open `claude-ai/student-internship-strategist-SA.md`
2. In claude.ai: Settings → Skills → Install from file
3. Start a conversation and upload or paste your CV

Option B — Claude Code (Full power, local)
- Full multi-agent system with per-task agents, local scripts, Playwright ATS automation, and a pipeline tracker.
- Best when you want batch job scanning, automated ATS filling, LaTeX generation, or to run everything locally.

Quickstart (Claude Code):
```bash
git clone https://github.com/<your-username>/TSIS_SA
cd TSIS_SA/claude-code
bash scripts/setup.sh
claude
```

Then type `/onboarding` to begin and upload your CV when prompted.

---

## How the UI/colors are used
The repository header uses two visual themes to hint at the two usage modes:
- Saudi green/white: quick, regional-focused workflows and datasets
- LinkedIn blue/white: the external search/outreach and network-mapping flows

These are purely visual cues in the header SVG and don't affect functionality.

---

## What It Does (short)

- `claude-ai/` — single-file skill for use inside claude.ai
- `claude-code/` — full multi-agent code, scripts, references and templates
- `scripts/` — tooling: `job_search.py`, `cv_parser.py`, `ats_fill.py`, `tracker.py`
- `references/` — company lists, ATS patterns, question bank
- `templates/` — cover letters, cold message templates, LaTeX CV base
- `config/` — example config files (copy by `scripts/setup.sh`)
- `data/` — gitignored personal data and application tracker

---

## Saudi Context
This project is built with Saudi students in mind: it includes Saudi/GCC career
sources, Tamheer/Taqat patterns, and curated company lists (see `references/`).

---

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md) — contributions welcome: company URLs,
working cold messages (anonymised), ATS patterns, script improvements, and
question-bank additions.

---

## License
MIT — see `LICENSE`.
