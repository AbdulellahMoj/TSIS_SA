---
name: scraping
description: Company and person research agent. Deep research on any target. Use /scrape [company or person name] or trigger when candidate asks to research a company or find who to contact.
---

# Scraping Agent

Two modes: company research and person research.
Always research before writing outreach. Never send a message without reading this first.

---

## What to Scrape

### Company Research Sources

| Source | What to extract |
|---|---|
| `[company].com/about` | Mission, founding story, team size, leadership names |
| `[company].com/blog` | Recent product updates, tech stack mentions, culture signals |
| `[company].com/careers` | Open roles, team names, required skills, seniority signals |
| Crunchbase | Funding stage, investors, headcount, founding year, recent rounds |
| GitHub (`github.com/[company]`) | Languages used, repo activity, open source work, team size signals |
| LinkedIn company page | Employee count, recent posts, job listings, who works there |
| Twitter/X (`@[company]`) | Recent announcements, tone, community activity |
| Press releases | Funding, partnerships, new products, expansions |
| ATS listing pages | Full job description, team name, required vs preferred skills |

### Person Research Sources

| Source | What to extract |
|---|---|
| LinkedIn profile | Current role, previous companies, education, recent activity |
| Twitter/X | Recent posts, tone, what they care about, community engagement |
| Published papers or talks | Research areas, technical depth, public positions |
| Personal website or blog | Personality, writing style, areas of interest |

---

## What NOT to Scrape

- LinkedIn content behind login (gated profiles, connection lists, InMail)
- Pages behind authentication or CAPTCHA — stop after one attempt
- Paid databases (Hunter.io, Apollo, etc.) — outside scope
- Any page returning persistent errors — move on

---

## Company Research Output

```
## [Company Name] — Research Brief

What they do:
[2-3 sentences: product, client type, industry, scale]

Recent news / projects:
- [Most recent significant thing — funding, product, announcement]
- [Second item if relevant]

Tech stack:
[Languages, frameworks, tools — extracted from job listings, GitHub, blog]

Culture signals:
[How they describe themselves, what they value, team size vibe]

People to contact:
- [Name], [Title] — [LinkedIn URL] — [Why relevant to candidate]
- [Name], [Title] — [LinkedIn URL] — [Why relevant]

Current/past interns found:
- [Name] — [LinkedIn URL] — [Year]

Connection points with candidate:
- [Specific overlap between candidate's background and company's work]
- [Shared context: KAUST, AI field, Saudi ecosystem, university, etc.]

Open listings: [Yes/No] — [Link if yes]
ATS platform: [Greenhouse / Lever / Workday / Ashby / Custom]
How to apply: [Direct link, recruiter name, referral path]
```

---

## Person Research Output

```
## [Person Name] — Profile Brief

Role: [Title at Company]
Background: [Where they studied, what they did before]
What they work on: [Day-to-day focus based on posts and activity]
Recent activity: [Most recent relevant post or announcement — last 30 days if possible]
Shared context with candidate: [Any overlap — program, university, domain, Saudi ecosystem]
Recommended message tone: [Formal / Technical peer / Community / Casual]
Recommended hook: [The one specific thing to reference in the first line]
```

---

## Glassdoor — Saudi Context

Glassdoor exists but has very limited coverage of Saudi and GCC companies.

Use Glassdoor for:
- Major companies with Saudi offices: Aramco, STC, Deloitte, McKinsey, EY
- Getting a rough culture signal for multinationals
- Salary estimates for well-known companies (rough ballpark only)

Do NOT rely on Glassdoor for:
- Saudi startups — almost no coverage
- Government entities — almost none listed
- PIF portfolio companies — most too new

For Saudi-specific culture signals, better sources are:
- LinkedIn posts by current employees
- Twitter/X accounts of the company and leadership
- Direct outreach to people currently working there

---

## Local Execution

```bash
# Research a company
python scripts/job_search.py --research "SDAIA"

# Parse a LinkedIn profile (paste the profile text, Claude reads it)
# No automated LinkedIn scraping — paste the profile text into the session
```
