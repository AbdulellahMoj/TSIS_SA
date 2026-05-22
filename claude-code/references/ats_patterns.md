# ATS Patterns Reference

Identify the ATS platform from a job listing URL, then use the platform-specific
field names and navigation patterns when filling applications.

---

## Platform Detection

| URL Pattern | ATS Platform |
|---|---|
| `boards.greenhouse.io/[company]/jobs/[id]` | Greenhouse |
| `job-boards.greenhouse.io/[company]/jobs/[id]` | Greenhouse (new) |
| `jobs.lever.co/[company]/[id]` | Lever |
| `[company].myworkdayjobs.com/[path]` | Workday |
| `jobs.ashbyhq.com/[company]/[id]` | Ashby |
| `apply.workable.com/[company]/j/[id]` | Workable |
| `careers.icims.com/jobs/[id]` | iCIMS |
| `[company].taleo.net/careersection` | Taleo |
| `[company].breezy.hr/p/[id]` | Breezy |
| `smartrecruiters.com/[company]/[id]` | SmartRecruiters |
| `taqat.sa/[path]` | Taqat (Saudi) |
| `tamheer.hrsd.gov.sa/[path]` | Tamheer (Saudi Gov) |

To get the company slug: look at any job listing URL from that company.
Example: `boards.greenhouse.io/stripe/jobs/1234` → slug is `stripe`

---

## Greenhouse

### JSON API (public, no login)
```
https://boards-api.greenhouse.io/v1/boards/[slug]/jobs
```
Returns: id, title, location.name, absolute_url, updated_at

### Standard Form Fields

| Field label | Input type | Notes |
|---|---|---|
| First name | text | |
| Last name | text | |
| Email | email | |
| Phone | tel | |
| Location | text | |
| LinkedIn Profile | url | |
| Website | url | Often used for GitHub/portfolio |
| Resume/CV | file | Upload PDF |
| Cover Letter | file or textarea | Often optional |
| How did you hear about us? | select | Safe default: "Company Website" |
| Demographic questions | various | Always optional — can decline |

### Structure
- Multi-step wizard: Personal Info → Resume → Application Questions → Diversity (optional)
- Progress shown at top of page
- "Additional Information" textarea at end — use it for one relevant project note

### Tips
- Cover letter field is often labelled "Cover Letter" as a separate file upload
- "Why are you interested in this role?" is the most common free-text question
- Demographic/EEO section is always optional

---

## Lever

### JSON API (public, no login)
```
https://api.lever.co/v0/postings/[slug]?mode=json
```
Returns: text (title), categories.location, hostedUrl, lists (requirements, description)

### Standard Form Fields

| Field label | Input type | Notes |
|---|---|---|
| Full name | text | |
| Email | email | |
| Phone | tel | Optional |
| Current company | text | Can leave blank if student |
| LinkedIn URL | url | |
| Twitter URL | url | Optional |
| GitHub URL | url | Optional |
| Resume | file | |
| "Why [Company]?" | textarea | Usually present — use cover letter opening |
| Referral source | text | Add connection's name here if you have one |

### Structure
- Usually single-page — cleaner than Greenhouse
- Referral field: enter the name of your connection at the company if applicable
- Less common to require a cover letter — check before preparing one

### Tips
- "Why [Company]?" field is the most important — use your personalised opening paragraph
- The referral field actually matters — companies check this

---

## Workday

### No public JSON API — must fetch careers page HTML

### Standard Form Fields

| Section | Field | Notes |
|---|---|---|
| Personal | First/Last name, email, phone, address | Standard |
| Resume | Upload or manually enter | Manual entry required even if you upload |
| Work Experience | Employer, title, dates, description (per role) | Enter each role separately |
| Education | University, degree, major, GPA, graduation | One entry per degree |
| Skills | Free text or tag selection | |
| Questions | Custom per company | Varies |
| Diversity | EEO, gender, ethnicity | Always optional |

### Structure
- Multi-page — most complex ATS
- "Work Experience" requires manual entry of each role, even if you upload a CV
- Once your Workday profile is complete, it saves across all Workday-powered companies
- URL pattern: `[company].myworkdayjobs.com/...`

### Tips
- Create your Workday profile once and maintain it
- Workday GPA field: enter as X.XX out of 4.0 or 5.0 depending on scale
- Description fields per role: paste the same content as your CV bullets

---

## Ashby

### JSON API (public, no login)
```
https://api.ashbyhq.com/posting-api/job-board/[slug]
```
Returns: jobPostings array with title, employmentType, locationName, publishedDate, jobUrl

### Standard Form Fields

| Field | Notes |
|---|---|
| Name, email, phone | Standard |
| Resume | Upload PDF |
| LinkedIn | URL |
| Cover letter | Usually optional — shorter companies |
| Custom questions | 1-3 role-specific questions |
| "Anything else to share?" | Often present — use for one project sentence |

### Structure
- Favoured by startups and growth-stage companies
- Shorter and simpler than Greenhouse/Workday
- Usually 1-2 pages

---

## Saudi-Specific Platforms

### Taqat (taqat.sa)
- Saudi national employment platform
- Requires Absher account (Saudi national ID linked)
- Upload CV in Arabic or bilingual format
- Most government and PIF-linked roles post here

### Tamheer (tamheer.hrsd.gov.sa)
- Government-managed intern program
- For Saudi nationals only
- Companies post 3-12 month internship slots
- Stipend is subsidised by HRSD
- Apply: create account with national ID, upload CV, select internship

---

## Common Short-Answer Questions (by platform frequency)

These appear on almost every application. Prepare standard answers once and adapt:

1. "Why do you want to work at [Company]?" (Greenhouse, Lever, Ashby)
2. "Tell us about yourself" (all platforms)
3. "What's your greatest achievement?" (all platforms)
4. "Why are you interested in this role?" (Greenhouse, Workday)
5. "What technical skills do you bring?" (Greenhouse, Workday)
6. "Where do you see yourself in 3-5 years?" (all platforms)
7. "What's a challenge you overcame?" (Workday, iCIMS)
8. "Do you have work authorisation?" (all platforms — Saudi nationals: Yes)
9. "How did you hear about this role?" (all platforms — safe: "Company Website")
10. "Are you open to relocation?" (some platforms)
