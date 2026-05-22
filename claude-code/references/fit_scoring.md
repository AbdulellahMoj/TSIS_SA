# Fit Scoring — Canonical Reference

The 6-dimension rubric used to evaluate every opportunity.
Used by the review agent, the search agent, and the strategy mapping step.

---

## The 6 Dimensions

Score each from 1 (poor fit) to 5 (strong fit).

---

### 1. Technical Fit

Does the required stack match what the candidate has actually used in real projects?
Not heard of. Not learned in a course. Actually used.

| Score | Meaning |
|---|---|
| 5 | Used 80%+ of listed tools in real projects |
| 4 | Used most tools, one or two gaps |
| 3 | Used about half, knows the rest conceptually |
| 2 | Some overlap but significant gaps |
| 1 | Almost no overlap — major ramp-up required |

---

### 2. Seniority Match

Is this role calibrated to the candidate's current level?

| Score | Meaning |
|---|---|
| 5 | Exactly right level — small stretch at most |
| 4 | Slightly senior but achievable with a strong application |
| 3 | Moderate stretch — possible but will be competitive |
| 2 | Too senior (not credible) OR too junior (wasted effort) |
| 1 | Clearly out of range in either direction |

---

### 3. Location and Logistics

Is the role's location, remote policy, and start date compatible with the candidate's constraints?

| Score | Meaning |
|---|---|
| 5 | Perfect match — no friction |
| 4 | Minor adjustment needed |
| 3 | Workable with some flexibility |
| 2 | Significant logistical hurdle |
| 1 | Requires relocation, sponsorship, or timing the candidate has ruled out |

---

### 4. Growth Potential

Will this role measurably improve the candidate's profile in 12 months?

| Score | Meaning |
|---|---|
| 5 | Strong brand, real ownership, mentorship signals, high network value |
| 4 | Good experience, solid network access |
| 3 | Decent experience, moderate network, not transformational |
| 2 | Limited learning or weak brand signal |
| 1 | Filler role — no strategic upside, weak brand in target field |

---

### 5. Reachability

How realistic is getting an interview given the candidate's current profile?

| Score | Meaning |
|---|---|
| 5 | Strong match, not oversubscribed — very likely to get a reply |
| 4 | Competitive but possible with a polished application |
| 3 | Possible — needs strong application and possibly outreach |
| 2 | Unlikely without a referral or connection |
| 1 | Very unlikely — overqualified applicants or top-tier requirement |

---

### 6. Strategic Value

Does this role add long-term leverage beyond the immediate role?

| Score | Meaning |
|---|---|
| 5 | Opens doors to next-tier roles, key network access, exact target domain |
| 4 | Strong stepping stone in the right direction |
| 3 | Solid but not transformational |
| 2 | Limited strategic upside |
| 1 | No meaningful leverage in the candidate's target field |

---

## Score Output Template

```
## Fit Score: [Role] at [Company]

Technical fit:    [X/5] — [one sentence reason]
Seniority match:  [X/5] — [one sentence reason]
Location:         [X/5] — [one sentence reason]
Growth potential: [X/5] — [one sentence reason]
Reachability:     [X/5] — [one sentence reason]
Strategic value:  [X/5] — [one sentence reason]

Total: [X/30]
Verdict: [Strong Match / Moderate Match / Weak Match / Skip]
Recommendation: [what to do next — one sentence]
```

---

## Thresholds

| Score | Verdict | Action |
|---|---|---|
| 25–30 | Strong Match | Full tailored materials: LaTeX CV + cover letter + ATS answer sheet |
| 18–24 | Moderate Match | Worth applying with standard tailoring |
| 12–17 | Weak Match | Flag concerns before candidate invests time |
| Below 12 | Skip | Tell candidate explicitly why this is not worth their time |

---

## Multi-Offer Comparison Template

When comparing 3+ opportunities, use this table:

```
## Opportunity Comparison

|                   | [Company A] | [Company B] | [Company C] |
|---|---|---|---|
| Technical fit     |      X      |      X      |      X      |
| Seniority match   |      X      |      X      |      X      |
| Location          |      X      |      X      |      X      |
| Growth potential  |      X      |      X      |      X      |
| Reachability      |      X      |      X      |      X      |
| Strategic value   |      X      |      X      |      X      |
| Total /30         |     XX      |     XX      |     XX      |

Priority:
1. [Company A] (XX/30) — full tailored materials
2. [Company B] (XX/30) — standard tailoring
3. [Company C] (XX/30) — apply only if time allows
```

Only invest full tailored documents (LaTeX CV, cover letter, ATS sheet)
for roles scoring 18/30 or above.

For anything below 18/30, tell the candidate the specific reason before they apply.
