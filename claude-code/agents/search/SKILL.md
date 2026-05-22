---
name: search
description: Job search agent. Searches Indeed, ZipRecruiter, direct Greenhouse/Lever/Ashby API endpoints, and Saudi company careers pages. Run /search [role] [location] or trigger when candidate asks to find opportunities.
---

# Search Agent

Finds live opportunities across multiple sources.
Always runs a fit score on every result before presenting anything.
Only shows results scoring 12/30 or above.

---

## Search Sequence

Run in this order. Stop when enough results are found (aim for 10–20 raw results
to filter down to 5–10 scored opportunities).

### 1. Indeed (if connector active)

```python
# Via MCP connector
search_jobs(
    search="[role]",
    location="[city, country]",
    country_code="SA",
    job_type="internship"
)
```

Good search patterns for Saudi roles:
- `"software engineering intern"` + location: Riyadh, SA
- `"AI intern machine learning"` + location: Jeddah, SA
- `"data science internship"` + location: remote
- `"computer science intern"` + country_code: SA

After results: call `get_job_details` on top 3–5 matches.

### 2. ZipRecruiter (if connector active)

Use for:
- Remote roles at international companies
- Multinational companies with Saudi offices
- Backup when Indeed returns thin results

### 3. Direct JSON API Endpoints

For companies the candidate has named, try their ATS API directly.
This returns complete, structured data and finds roles that never appear on job boards.

> Works in Claude Code via `scripts/job_search.py`.
> Also works in claude.ai via web_fetch — no Claude Code needed for this step.

```
Greenhouse:  boards-api.greenhouse.io/v1/boards/[slug]/jobs
Lever:       api.lever.co/v0/postings/[slug]?mode=json
Ashby:       api.ashbyhq.com/posting-api/job-board/[slug]
Workable:    [company].workable.com/api/v3/jobs
```

To find the slug: check the URL of any job listing from that company.

Filter results for: intern, junior, entry-level, summer, trainee, graduate.

### 4. Saudi Company Careers Pages (Direct Fetch)

Load `references/saudi_companies.md` for the full URL list.
Fetch the key targets directly:

```python
# Via scripts/job_search.py
python scripts/job_search.py --company sdaia
python scripts/job_search.py --company kaust
python scripts/job_search.py --company stc
python scripts/job_search.py --all  # scans all configured companies
```

### 5. Web Search Fallback

Use web_search when:
- Company is not in the Saudi reference list
- ATS endpoint returns nothing
- Candidate wants to find companies, not just listings

Good search patterns:
- `site:linkedin.com/jobs "[role] intern" Riyadh 2026`
- `"[company]" internship apply 2026`
- `"[sector]" intern saudi arabia summer 2026`

---

## Output Per Opportunity

For each result, produce this before presenting to the candidate:

```
## [Company Name] — [Role Title]

Source: [Indeed / Lever API / Careers page / Web]
Link: [apply URL]
Location: [city / remote]
Team: [team or department if known]
Posted: [date if available]
Deadline: [if listed]

Fit Score: [X/30] — [Strong / Moderate / Weak]
Technical fit:    [X/5]
Seniority match:  [X/5]
Location:         [X/5]
Growth potential: [X/5]
Reachability:     [X/5]
Strategic value:  [X/5]

Why it fits: [1-2 sentences]
Watch out for: [1 sentence on any concern]
```

---

## Shortlist Output

After scoring all results:

```
## Opportunity Shortlist

Showing [N] results scored 18+ out of 30.

| Rank | Company | Role | Score | Action |
|---|---|---|---|---|
| 1 | [Company] | [Role] | 26/30 | Full tailored application |
| 2 | [Company] | [Role] | 23/30 | Standard application |
| 3 | [Company] | [Role] | 20/30 | Apply if time allows |

Run /review to compare these in detail.
Run /outreach [company] to start the application process.
```

---

## Running Locally

```bash
# Search a specific company's Greenhouse board
python scripts/job_search.py --company stripe --platform greenhouse

# Search all Saudi companies in the reference list
python scripts/job_search.py --all --filter intern

# Search by role across all configured platforms
python scripts/job_search.py --role "AI engineer" --location riyadh
```

Results are saved to `data/search_results.tsv` for reference.
