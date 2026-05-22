---
name: review
description: Fit scoring and opportunity comparison. Score any job listing against the candidate profile. Run /review to evaluate current opportunities or compare multiple options. Read references/fit_scoring.md.
---

# Review Agent

Evaluates opportunities. Two modes: single score and multi-offer comparison.
Never present an opportunity to the candidate without a fit score.

---

## Fit Scoring — 6 Dimensions

Score each from 1 (poor fit) to 5 (strong fit).
Load the candidate profile from `data/profile.md` before scoring.

**1. Technical fit**
Does the required stack match what the candidate has actually used in real projects?
5 = used 80%+ of listed tools in real work
3 = used about half, knows the rest conceptually
1 = almost no overlap, significant ramp-up required

**2. Seniority match**
Is this role calibrated to the candidate's current level?
5 = right level, small stretch at most
3 = slightly senior but possible with strong application
1 = too junior (wasted effort) or too senior (not credible)

**3. Location and logistics**
Is the location, remote policy, and timing compatible with the candidate's constraints?
5 = perfect match, no friction
3 = workable with some adjustment
1 = requires relocation, sponsorship, or timing they've ruled out

**4. Growth potential**
Will this role improve the candidate's profile in 12 months?
5 = strong brand, real technical ownership, mentorship, high network value
3 = decent experience, moderate network, not transformational
1 = low learning, weak brand, filler role on the CV

**5. Reachability**
How realistic is an interview given the candidate's current profile?
5 = strong match, not oversubscribed, candidate is competitive
3 = possible with a strong application
1 = very unlikely — overqualified applicants, no connection, top-tier requirement

**6. Strategic value**
Does this role add long-term leverage?
5 = opens doors to next-tier roles, key network, target domain
3 = solid stepping stone, not transformational
1 = no strategic upside in the candidate's target field

---

## Single Opportunity Score Output

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
Recommendation: [one sentence — what to do next]
```

**Thresholds:**
- 25–30: Strong — full tailored application (LaTeX CV, cover letter, ATS sheet)
- 18–24: Moderate — worth applying, standard tailoring
- 12–17: Weak — flag concerns before the candidate invests time
- Below 12: Tell them explicitly why this is not worth their time right now

---

## Multi-Offer Comparison

When the candidate has 3+ options:

```
## Opportunity Comparison

|                   | [Company A] | [Company B] | [Company C] |
|---|---|---|---|
| Technical fit     |      4      |      3      |      5      |
| Seniority match   |      5      |      4      |      3      |
| Location          |      5      |      5      |      2      |
| Growth potential  |      4      |      5      |      3      |
| Reachability      |      3      |      4      |      5      |
| Strategic value   |      5      |      3      |      4      |
| Total /30         |     26      |     24      |     22      |

Priority:
1. [Company A] — full tailored materials
2. [Company B] — strong growth, apply second
3. [Company C] — easier to get but lower fit, apply if time allows
```

---

## Strategy Map

After scoring all opportunities, produce the Strategy Map:

```
## Candidate Strategy Map

Strongest positioning:
[2-3 sentences on what this candidate can credibly claim]

Target tiers:

Tier 1 (stretch — worth trying):
- [Company/role type] — because [specific reason from profile]

Tier 2 (strong fit):
- [Company/role type] — because [specific reason]

Tier 3 (safety — high probability):
- [Company/role type] — because [specific reason]

Gaps to address before applying:
- [Gap] — how to mitigate: [action]

Recommended first move:
[Single most important action]
```
