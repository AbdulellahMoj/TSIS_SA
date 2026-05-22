# Claude Code — Student Internship Strategist

Full multi-agent system for power users.
One focused agent per task. Local scripts. Playwright ATS automation.

---

## Requirements

- **Claude Code** — [install guide](https://docs.anthropic.com/en/docs/claude-code)
- **Python 3.10+**
- **Node.js 18+** (for Playwright — optional, ATS automation only)
- A terminal

---

## Setup

```bash
git clone https://github.com/[your-username]/student-internship-strategist
cd student-internship-strategist/claude-code
bash scripts/setup.sh
```

Then:
1. Edit `config/profile.yml` with your details
2. Edit `config/targets.yml` with your target companies
3. Run `claude` to start Claude Code

Note: Running `bash scripts/setup.sh` will copy the example config files
(`config/profile.example.yml` and `config/targets.example.yml`) to
`config/profile.yml` and `config/targets.yml` if those files do not already exist.
This creates the editable config files the scripts expect.

---

## Starting a Session

```bash
claude
```

Type `/onboarding` to begin.
Upload your CV as a PDF when prompted.
Export your LinkedIn connections and upload the CSV file for network mapping.

---

## Slash Commands

| Command | What it does |
|---|---|
| `/onboarding` | Start here — setup, intro, collect your CV |
| `/questions` | Deep discovery — 20–100 questions about your background |
| `/cv` | Analyse, tailor, or generate LaTeX CV |
| `/search [role] [city]` | Search jobs across all configured sources |
| `/scrape [company]` | Deep research on a company or person |
| `/review` | Score opportunities, compare multiple options |
| `/outreach [company]` | Draft cold message or cover letter |
| `/ats [url]` | Prepare ATS answer sheet; optionally auto-fill |
| `/tracker` | Show full pipeline |
| `/status` | Quick summary and follow-ups due |

---

## Scripts (run directly)

```bash
# Parse your CV
python scripts/cv_parser.py --file path/to/cv.pdf

# Search a specific company's job board
python scripts/job_search.py --company sdaia
python scripts/job_search.py --company stripe --platform greenhouse

# Scan all Saudi companies for intern roles
python scripts/job_search.py --all --filter intern

# Score a job listing
python scripts/fit_score.py --job path/to/job.txt

# Compare multiple opportunities
python scripts/fit_score.py --compare job_a.txt job_b.txt job_c.txt

# Map LinkedIn connections against targets
python scripts/linkedin_csv.py --file data/connections.csv

# Application tracker
python scripts/tracker.py --list
python scripts/tracker.py --followups
python scripts/tracker.py --add --company "SDAIA" --role "AI Intern" --date "2026-06-01"
python scripts/tracker.py --update --company "SDAIA" --status "interview_scheduled"

# ATS form auto-fill (Playwright required)
python scripts/ats_fill.py --url "https://boards.greenhouse.io/..." --application data/applications/company/
```

---

## Data Structure

```
data/                          ← gitignored — your private data
├── profile.md                 ← Candidate profile (built during /onboarding)
├── work_history.md            ← Full Work History Document
├── connections.csv            ← LinkedIn connections export
├── tracker.tsv                ← Application pipeline
└── applications/
    └── [company-slug]/
        ├── research_brief.md  ← Company research
        ├── cv_tailored.md     ← Tailored CV for this role
        ├── cv.tex             ← LaTeX CV
        ├── cover_letter.md    ← Cover letter
        ├── ats_answers.md     ← ATS answer sheet
        └── outreach_*.md      ← Cold messages
```

---

## What Needs Claude Code vs What Works in claude.ai

| Feature | claude.ai | Claude Code |
|---|---|---|
| Deep questioning | ✅ | ✅ |
| CV analysis | ✅ | ✅ |
| Job search (API) | ✅ web_fetch | ✅ job_search.py |
| Fit scoring | ✅ | ✅ fit_score.py |
| CV tailoring | ✅ | ✅ |
| LaTeX generation | ✅ (.tex file) | ✅ (compile locally) |
| Cold messages | ✅ | ✅ |
| ATS answer sheet | ✅ | ✅ |
| **ATS auto-fill** | ❌ | ✅ ats_fill.py + Playwright |
| **Batch job scan** | ❌ | ✅ job_search.py --all |
| **LinkedIn CSV** | ✅ (upload file) | ✅ linkedin_csv.py |
| **Notion sync** | ✅ connector | ✅ tracker.py --sync |

---

## Agents

See `AGENTS.md` for a full description of every agent.
Each agent has its own `agents/[name]/SKILL.md`.

---

## References

| File | Contents |
|---|---|
| `references/saudi_companies.md` | 50+ Saudi/GCC careers URLs by category |
| `references/ats_patterns.md` | ATS identification + field names per platform |
| `references/fit_scoring.md` | The 6-dimension scoring rubric |
| `references/question_bank.md` | 100 discovery questions by phase |

---

## License

MIT
