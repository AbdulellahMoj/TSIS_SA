# Student Internship Strategist — Saudi Tech Edition
A visual header is included below. If your client supports SVG in READMEs, it will render the animated banner.

![TSIS_SA header](assets/tsis_header.svg)

A lot of CS and tech students in Saudi Arabia struggle to find internships.
Not because they're not good enough — but because the system is opaque.
Companies don't always post publicly. Recruiters don't always respond.
Cold messages get ignored. CVs get filtered. The whole process assumes
connections and context most students don't have yet.

This repository is a tool to change that.

It gives you an AI-powered internship strategist that understands the Saudi
tech ecosystem, knows which companies hire interns and how, and walks you
through every step — from fixing your CV to submitting the application.

---

## Two Options

### Option 1 — claude.ai (Free / No Setup)

If you use [claude.ai](https://claude.ai) on the free or Pro plan, install
the `.skill` file and you're done. Claude becomes your internship strategist
in any conversation.

→ [Go to the claude.ai folder](./claude-ai/)

**Works for:** All claude.ai users. Free plan included.
**Requires:** Nothing beyond a claude.ai account.
**Limitations:** No Playwright automation (ATS form-filling is manual paste).
LaTeX CV needs local compile. Everything else works fully.

---

### Option 2 — Claude Code (Full Power)

If you have Claude Code installed, the `claude-code/` folder gives you a
full multi-agent system — one focused agent per task, scripts that run
locally, Playwright-based ATS automation, and a full application tracker.

→ [Go to the Claude Code folder](./claude-code/)

**Works for:** Claude Code users (requires Claude Pro/Max or API access).
**Requires:** Node.js, Python 3.10+, Playwright.
**Unlocks:** Auto-fill ATS forms, batch job scanning, local PDF generation,
full pipeline tracker.

---

## What It Does

Regardless of which option you use, the strategist covers:

- **Profile Building** — reads your CV, asks deep questions, builds a complete
  Work History Document that powers everything else
- **Fit Scoring** — scores every opportunity across 6 dimensions before you
  invest time applying
- **Live Job Search** — searches Indeed, ZipRecruiter, and Saudi company
  careers pages directly
- **CV Tailoring** — rewrites your bullets for each specific role
- **Cover Letters** — writes targeted letters tied to real company research
- **LaTeX CV** — generates a clean, ATS-safe PDF from your profile
- **Cold Outreach** — drafts personalised LinkedIn messages for every target
- **ATS Applications** — prepares every form field answer before you open the form
- **Pipeline Tracking** — logs every application, sets follow-up dates

---

## Quickstart

### claude.ai

1. Go to `claude-ai/`
2. Download `student-internship-strategist-SA.md`
3. In claude.ai: Settings → Skills → Install from file
4. Open a new conversation and type: *"I need help finding a tech internship"*

### Claude Code

```bash
git clone https://github.com/[your-username]/TSIS_SA
cd student-internship-strategist/claude-code
bash scripts/setup.sh
claude
```

Then type `/onboarding` to start.

---

## Saudi Tech Context

This tool is built with the Saudi ecosystem in mind:

- Knows the major Saudi companies and their careers pages
- Understands Tamheer and Taqat internship programs
- Covers PIF portfolio companies, SDAIA, KAUST, STC, Aramco, Elm, and more
- Familiar with the consulting firms hiring in Riyadh (BCG, McKinsey, EY, Deloitte)
- Covers the Saudi startup ecosystem (Sary, Lean, Tamara, Foodics, Unifonic)

---

## Contributing

Found a company that should be on the list? A question that should be in
the question bank? A cold message template that actually worked?

See [CONTRIBUTING.md](./CONTRIBUTING.md).

