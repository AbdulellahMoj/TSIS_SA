# Agents

Nine agents. Each handles one part of the pipeline.
They are designed to chain: output from one feeds into the next.

---

## onboarding

**File:** `agents/onboarding/SKILL.md`
**Trigger:** `/onboarding` or first-time user
**Inputs:** Nothing required upfront
**Outputs:** Candidate told what to prepare; session initialised

Greets the candidate, explains the full process and what Claude can do.
Checks which connectors are active (Indeed, Notion, Google Drive).
Asks for CV, LinkedIn URL, GitHub, LinkedIn connections CSV.
Does NOT ask discovery questions — that is the questions agent's job.
Ends by reading the CV and sharing 2–3 first impressions.

---

## questions

**File:** `agents/questions/SKILL.md`
**Trigger:** `/questions` or after onboarding
**Inputs:** CV already read; basic profile exists
**Outputs:** Complete candidate profile saved to `data/profile.md`

Runs deep adaptive questioning — up to 100 questions across all areas of
the candidate's background. Never asks about things already in the CV.
Pushes back on vague answers. Builds and saves the Work History Document
to `data/work_history.md`. Does not stop until the profile is fully detailed.

---

## cv

**File:** `agents/cv/SKILL.md`
**Trigger:** `/cv` or any CV-related request
**Inputs:** CV file or text; Work History Document preferred
**Outputs:** CV analysis, tailored CV per role, LaTeX .tex file

Three modes:
1. **Analyse** — reads CV, flags strengths, weaknesses, missing metrics
2. **Tailor** — rewrites bullets for a specific role using Work History Document
3. **Generate** — produces ATS-safe LaTeX `.tex` file from candidate profile

Runs ATS keyword extraction before any tailoring.
Checks prerequisites before generating documents.

---

## search

**File:** `agents/search/SKILL.md`
**Trigger:** `/search [role] [location]` or job-finding requests
**Inputs:** Candidate profile; optional role/location filters
**Outputs:** Ranked shortlist of opportunities with fit scores

Searches in this order:
1. Indeed MCP (if connected)
2. ZipRecruiter MCP (if connected)
3. Direct Greenhouse / Lever / Ashby JSON API endpoints
4. Saudi company careers pages via `scripts/job_search.py`
5. Web search fallback

Runs a fit score on every result before presenting.
Only shows opportunities scoring 12/30 or above.

---

## scraping

**File:** `agents/scraping/SKILL.md`
**Trigger:** `/scrape [target]` or research requests
**Inputs:** Company name, person name, or LinkedIn URL
**Outputs:** Research brief in structured format

Two modes:
1. **Company research** — fetches careers page, blog, GitHub, press releases,
   funding data, key people to contact, recent news
2. **Person research** — reads LinkedIn profile, Twitter/X, papers,
   extracts background, current role, shared context, message tone

Strict rules on what NOT to scrape (gated content, CAPTCHA pages, private profiles).

---

## review

**File:** `agents/review/SKILL.md`
**Trigger:** `/review` or when opportunities need evaluation
**Inputs:** One or more job listings or opportunity descriptions
**Outputs:** Fit scores, strategy map, ranked shortlist

Two modes:
1. **Single opportunity** — runs 6-dimension fit score, gives verdict
2. **Multi-offer comparison** — scores all options, produces comparison table,
   recommends investment priority

Also produces the Strategy Map: tier 1/2/3 targets, gaps to address, first move.

---

## outreach

**File:** `agents/outreach/SKILL.md`
**Trigger:** `/outreach [company]` or message/letter requests
**Inputs:** Company research brief; candidate profile; target person details
**Outputs:** Cold message or cover letter, ready to send

Always asks 5 clarifying questions before writing:
who is the recipient, have they applied, is there an open listing,
what is the purpose, what tone is appropriate.

Templates for: CEO/Founder, Senior Engineer, Employee/Intern, Consulting person.
Cover letter: research-first, role-specific, reads like a person wrote it.

---

## ats

**File:** `agents/ats/SKILL.md`
**Trigger:** `/ats [url]` or application requests
**Inputs:** ATS URL; tailored CV; company research brief
**Outputs:** Complete answer sheet; optionally auto-filled form via Playwright

Step 1: Identify ATS platform from URL pattern.
Step 2: Run prerequisites check (CV, research brief, form field prompts).
Step 3: Generate filled answer sheet for every field.
Step 4 (Claude Code + Playwright only): Navigate and fill the form automatically.

⚠️ Auto-fill requires Playwright. If it fails, the answer sheet is always the fallback.

---

## tracker

**File:** `agents/tracker/SKILL.md`
**Trigger:** `/tracker` or `/status` or tracking requests
**Inputs:** Application details; status updates
**Outputs:** Updated `data/tracker.tsv`; Notion sync if connected

Manages the full application pipeline:
- Log new application
- Update status (applied / interview / offer / rejected / ghosted)
- List all applications with current status
- Show follow-up due today or overdue
- Generate summary report

Follow-up schedule: +7 days after applying, +14 days if no reply.
