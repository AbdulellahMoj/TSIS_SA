---
name: ats
description: ATS application agent. Identifies the ATS platform from a URL, generates a complete answer sheet for every form field, and optionally auto-fills the form using Playwright (Claude Code only). Run /ats [url].
---

# ATS Agent

> ⚠️ **Auto-fill requires Claude Code + Playwright.**
> Running `scripts/ats_fill.py` will not work in claude.ai.
> In claude.ai, this agent still provides full value: it identifies the ATS,
> prepares every answer, and you paste them yourself.
> If Playwright fails or is not installed, use the answer sheet — it's the same output.

---

## Step 1 — Identify the ATS

From the URL:

| Pattern | Platform |
|---|---|
| `boards.greenhouse.io/[company]/jobs/[id]` | Greenhouse |
| `jobs.lever.co/[company]/[id]` | Lever |
| `[company].myworkdayjobs.com/...` | Workday |
| `jobs.ashbyhq.com/[company]/[id]` | Ashby |
| `apply.workable.com/[company]/j/[id]` | Workable |
| `careers.icims.com/...` | iCIMS |
| `[company].taleo.net/...` | Taleo |
| `taqat.sa/...` | Taqat (Saudi) |
| `tamheer.hrsd.gov.sa/...` | Tamheer (Saudi gov) |

---

## Step 2 — Prerequisites Check

- [ ] ATS platform identified
- [ ] Tailored CV available for this role (`data/applications/[slug]/cv_tailored.md`)
- [ ] Company research brief available
- [ ] Job description read
- [ ] Short-answer field prompts known (candidate shares them or Claude fetches the listing)

---

## Step 3 — Generate Answer Sheet

Produce answers for every field before the candidate opens the form.

### Standard Fields (all platforms)

```markdown
## Application Answer Sheet — [Company] / [Role]
Platform: [Greenhouse / Lever / Workday / Ashby]
Date: [date]

### Personal
Full name: [from profile]
Email: [from profile]
Phone: [from profile]
LinkedIn: [from profile]
GitHub / Portfolio: [from profile]
Location: [from profile]
Work authorisation: [Saudi national / iqama holder / requires sponsorship]

### Resume
→ Upload: data/applications/[slug]/cv_tailored.pdf

### Short Answer Fields

Why do you want to work here?
[2-3 sentences — specific to company research, not generic]

Tell us about yourself:
[3-sentence positioning: who, what I build, what I'm looking for]

What's your biggest achievement?
[STAR format — 4-5 sentences: situation, action, result, number]

Technical skills:
[Exact list from Skills section of tailored CV]

Where do you see yourself in 3 years?
[1-2 sentences — honest, relevant to this company's domain]

### Cover Letter (if field exists)
→ Paste from: data/applications/[slug]/cover_letter.md

### Additional Notes (if field exists)
[1 sentence about the most relevant project — optional]
```

---

## Platform-Specific Notes

### Greenhouse
- Multi-step: personal → resume → application questions → demographics (always optional)
- "Additional information" field at end — good place for one relevant note
- Cover letter field often optional — check before preparing one

### Lever
- Single page, cleaner
- Often has a "Why [Company]?" field — use opening paragraph of cover letter
- Has a referral field — if candidate has a connection, name them here

### Workday
- Most complex — multiple pages, heavy on dropdowns
- "Work Experience" section requires manual entry of each role (not just upload)
- Once profile is complete, Workday saves it for future applications at other companies

### Ashby
- Favoured by startups
- Usually shorter
- "Anything else you'd like to share?" at end — use it for one project sentence

---

## Step 4 — Auto-Fill (Claude Code + Playwright Only)

> ⚠️ This step requires Playwright installed via `scripts/setup.sh`.
> It will not run in claude.ai.

```bash
python scripts/ats_fill.py --url "[ATS URL]" --application data/applications/[slug]/
```

The script:
1. Opens the URL in a Playwright browser
2. Identifies form fields by label and input type
3. Fills each field from the answer sheet
4. Pauses before submitting — candidate reviews and confirms
5. Submits only after explicit confirmation

The script never auto-submits. The candidate always reviews and confirms.

If the script encounters a CAPTCHA, unknown field type, or login wall, it stops
and prints what it found. The candidate handles that field manually.

---

## Output

Save answer sheet to:
`data/applications/[company-slug]/ats_answers.md`

Log the application attempt in tracker:
`python scripts/tracker.py --add "[Company]" "[Role]" "[Date]" --status applied`
