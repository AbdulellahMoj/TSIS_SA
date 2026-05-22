---
name: cv
description: CV analysis, Work History Document building, CV tailoring per role, LaTeX CV generation. Use whenever the candidate needs CV work. Read references/fit_scoring.md before tailoring.
---

# CV Agent

Three modes. Always check prerequisites before any output.

---

## Prerequisites Check

Before generating anything:

**Analyse mode:**
- [ ] CV text or PDF available in session

**Tailor mode:**
- [ ] Work History Document exists (`data/work_history.md`) OR CV has been fully read
- [ ] Job description or listing URL available for this specific role
- [ ] Candidate confirmed the company and role
- [ ] Fit score is 18/30 or above (run `/review` first if not done)

**Generate (LaTeX) mode:**
- [ ] Complete candidate profile available
- [ ] Work history document exists
- [ ] Target role confirmed (determines what to emphasise)

If anything is missing: ask for it before writing a single word.

---

## Mode 1 — Analyse

Read the full CV. Output a structured analysis:

```
## CV Analysis

### What's Strong
- [Credential or bullet that is well-written and impactful]
- [Specific metric or achievement that stands out]

### What's Weak
- [Bullet that is vague — no metric, no action verb, no outcome]
- [Section that is missing or thin]

### What's Missing Entirely
- [Skills expected for [target field] that aren't listed]
- [Certifications or projects that would strengthen the profile]

### Recruiter Perception (honest)
[2-3 sentences: what a recruiter looking at this CV for 10 seconds would think]

### Priority Fixes
1. [Most impactful change]
2. [Second most impactful]
3. [Third]
```

---

## Mode 2 — Tailor

When tailoring for a specific role:

### Step 1 — ATS Keyword Extraction

Extract from the job description:
- Required skills (tools, languages, frameworks)
- Preferred skills
- Action verbs used in the role description
- Degree or GPA requirements
- Any specific domain knowledge mentioned

### Step 2 — Gap Analysis

Compare extracted keywords against the candidate's CV and Work History Document.

Output:
```
## ATS Keyword Gap Report — [Role at Company]

| Keyword | In CV? | Action |
|---|---|---|
| [Tool] | YES | Keep |
| [Framework] | PARTIAL | Strengthen in [role] bullet |
| [Skill] | NO | Add to Skills section if known |
```

### Step 3 — Bullet Rewrites

For each bullet being rewritten, follow this formula:
**[Metric or impact] + [action verb] + [what] + [context/scale]**

Example:
- Before: "Worked on computer vision pipeline for drone project"
- After: "Built real-time object detection pipeline (YOLOv8, OpenCV) processing 30fps video for autonomous UAV competing in SUAS 2026"

### Step 4 — Section Reordering

Move the most relevant experience to the top of each section.
Less relevant entries move down — nothing disappears.

### Step 5 — Output

Produce the tailored CV as a markdown file.
Save to `data/applications/[company-slug]/cv_tailored.md`.

---

## Mode 3 — Generate LaTeX

> ⚠️ Compiling the .tex file to PDF requires a local LaTeX installation
> (TeX Live or MiKTeX). Claude generates the .tex file — you compile it.
> If you don't have LaTeX installed, ask for a DOCX version instead.

Load `templates/cv_base.tex` and populate it with the candidate's data.

### ATS-Safe Rules

1. Single column — no side-by-side layout
2. No tables for main content
3. Selectable text only — no rasterized text
4. Standard section names: Experience, Education, Projects, Skills
5. Black body text — color only for section headings
6. Standard fonts: lmodern or helvet
7. No icons in the main body

### Section Order (default)

1. Header (name, contact, links)
2. Education
3. Experience
4. Projects
5. Skills
6. Certifications & Awards

Adjust order based on the role: if the role is research-focused, put Education
and Projects before Experience.

### Output

Save to `data/applications/[company-slug]/cv.tex` (or `data/cv_base.tex` for general use).
Print compile command: `pdflatex cv.tex` (run twice).

---

## Notes on Work History Document

The Work History Document (`data/work_history.md`) is the source of truth.
It contains the full unedited context, numbers, and proof points behind
every item on the CV — the things that got cut for space.

When tailoring, always pull from the Work History Document first.
If it doesn't exist yet, run `/questions` to build it before tailoring.
