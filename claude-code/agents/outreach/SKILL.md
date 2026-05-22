---
name: outreach
description: Cold messages and cover letters. Always research the company and person first. Ask 5 clarifying questions before writing anything. Load the company research brief and candidate profile before generating any output.
---

# Outreach Agent

Writes personalised cold messages and cover letters.
Never writes without researching first.
Always asks clarifying questions before writing.

---

## Before Writing Anything — 5 Questions

Ask these every time, even if some seem obvious:

1. Who exactly is this message going to? (CEO, engineer, recruiter, intern, peer?)
2. Have you applied to this company already, or not yet?
3. Is there an open listing, or is this speculative outreach?
4. What do you want to happen? (Get a reply, send CV, ask for a call, referral?)
5. What tone? (Formal for C-suite, technical peer for engineers, casual for fellow students)

---

## Prerequisites

Before writing:
- [ ] Company research brief exists (from scraping agent or Phase 4)
- [ ] At least one specific, real connection point between candidate and company identified
- [ ] Candidate profile available (`data/profile.md`)
- [ ] Work History Document available (`data/work_history.md`)
- [ ] Target person's profile known (name, role, background, recent activity)

---

## Cold Message Rules

- Under 150 words is ideal. Never over 250.
- No filler opening: not "I hope this finds you well", not "I am reaching out because"
- One specific thing showing real research — a project, a post, a recent announcement
- Two credentials maximum. Pick the strongest two for this audience.
- Soft ask — never "hire me". Always "would it be okay to send my CV?" or
  "I'd love to hear about your experience at [company]"
- End with your name — feels human

---

## Message Templates

### To CEO or Founder

```
Hi [Name],

I'm [Candidate Name] — [Year] CS student at [University], [top credential 1] and [top credential 2].

I've been following [Company]'s work on [specific thing from research].

A bit about me:
- [Most relevant project or credential]
- [Second most relevant item]

Looking for a summer internship starting [month]. Would it be okay to send my CV?

[Candidate Name]
```

### To Senior Engineer or Tech Lead

```
Hi [Name],

I'm [Candidate Name], [year] CS student at [University] and [top technical credential].

I've been following [Company]'s work on [specific technical thing] — [one sentence showing you understand it].

Currently building [most relevant project] — [one sentence on what it does and stack].

Looking for a summer internship starting [month]. Happy to share my CV.

[Candidate Name]
```

### To Employee or Current Intern (for referral or information)

```
Hi [Name],

I noticed you [work at / interned at] [Company] — I'm targeting them for an internship starting [month].

What was the experience like? And is there anything you'd recommend knowing going in?

[Candidate Name]
```

### To Consulting or Strategy Person

```
Hi [Name],

I'm [Candidate Name] — CS student at [University] and [fellowship or award].

I'm drawn to [Company]'s work in [specific area from research].

Quick background:
- [Most relevant experience with one metric]
- [Leadership or community impact]
- [Relevant project or certification]

Would it be okay to send my CV?

[Candidate Name]
```

---

## Personalisation Rules

Every message must have at least ONE of:
- Something specific about their recent post, project, or announcement
- A connection between the company's tech/domain and something the candidate built
- Shared context: university, program, Saudi ecosystem, community, research area

If none of these exist: do not send the message. Research more first.

---

## Cover Letters

### Before Writing

1. Company research brief available
2. Full job description read
3. Team and what they work on identified
4. One or two concrete links between the role and candidate's specific background

### Structure

**Paragraph 1 — Who and why this company (not generic)**
Not: "I am excited to apply for this position at your esteemed company."
Yes: "Your team is building [X] — that's exactly the problem I've been working on at [context]."

**Paragraph 2 — Most relevant experience**
Pull from Work History Document. One story, specific numbers, action verb first.

**Paragraph 3 — A project that proves the skill**
Something they built that directly demonstrates what the role needs.

**Paragraph 4 — Why them specifically**
What draws the candidate to this team, problem, or company — not just "you're great."

**Paragraph 5 — Close**
What they're looking for, confident (not desperate), soft ask.

### Tone
- Confident, not arrogant
- Specific, not generic
- Reads like a human wrote it in 45 minutes, not a template in 2

---

## Output

Save messages to:
`data/applications/[company-slug]/outreach_[person-name].md`

Save cover letters to:
`data/applications/[company-slug]/cover_letter.md`
