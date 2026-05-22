"""
job_search.py
Search for jobs via direct Greenhouse/Lever/Ashby JSON APIs and Saudi careers pages.
No login required. All endpoints are public.

Usage:
    python scripts/job_search.py --company sdaia
    python scripts/job_search.py --company stripe --platform greenhouse
    python scripts/job_search.py --all --filter intern
    python scripts/job_search.py --role "AI engineer" --location riyadh
    python scripts/job_search.py --research "SDAIA"
"""

import argparse
import json
import sys
import csv
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

# ── Saudi and GCC company careers URLs ──────────────────────────────────────
# Format: slug -> {name, url, platform}
# platform: greenhouse | lever | ashby | custom
SAUDI_COMPANIES = {
    "sdaia":        {"name": "SDAIA",            "url": "https://sdaia.gov.sa/careers",                "platform": "custom"},
    "mcit":         {"name": "MCIT",             "url": "https://mcit.gov.sa/careers",                 "platform": "custom"},
    "kaust":        {"name": "KAUST",            "url": "https://kaust.edu.sa/en/study/careers",       "platform": "custom"},
    "elm":          {"name": "Elm",              "url": "https://elm.sa/careers",                      "platform": "custom"},
    "stc":          {"name": "STC",              "url": "https://stc.com.sa/eng/careers",              "platform": "custom"},
    "aramco":       {"name": "Saudi Aramco",     "url": "https://aramco.com/en/careers",               "platform": "custom"},
    "neom":         {"name": "NEOM",             "url": "https://neom.com/en-gb/careers",              "platform": "custom"},
    "humain":       {"name": "HUMAIN",           "url": "https://humain.ai/careers",                   "platform": "custom"},
    "alat":         {"name": "ALAT",             "url": "https://alat.com.sa/careers",                 "platform": "custom"},
    "pif":          {"name": "PIF",              "url": "https://pif.gov.sa/careers",                  "platform": "custom"},
    "misk":         {"name": "Misk Foundation",  "url": "https://misk.org.sa/en/programs",             "platform": "custom"},
    "sda":          {"name": "Saudi Digital Academy", "url": "https://sda.edu.sa",                    "platform": "custom"},
    "taqat":        {"name": "Taqat",            "url": "https://taqat.sa",                            "platform": "custom"},
    "tamheer":      {"name": "Tamheer",          "url": "https://tamheer.hrsd.gov.sa",                 "platform": "custom"},
    "sary":         {"name": "Sary",             "url": "https://sary.com/careers",                   "platform": "custom"},
    "lean":         {"name": "Lean",             "url": "https://lean.sa/careers",                    "platform": "custom"},
    "tamara":       {"name": "Tamara",           "url": "https://tamara.co/careers",                  "platform": "custom"},
    "foodics":      {"name": "Foodics",          "url": "https://foodics.com/careers",                "platform": "greenhouse"},
    "unifonic":     {"name": "Unifonic",         "url": "https://unifonic.com/careers",               "platform": "custom"},
    "mckinsey-sa":  {"name": "McKinsey Saudi",   "url": "https://mckinsey.com/sa/careers",            "platform": "custom"},
    "bcg-riyadh":   {"name": "BCG Riyadh",       "url": "https://bcg.com/offices/riyadh",             "platform": "custom"},
    "deloitte-sa":  {"name": "Deloitte Saudi",   "url": "https://deloitte.com/sa/careers",            "platform": "custom"},
    "ey-sa":        {"name": "EY Saudi",         "url": "https://ey.com/en_sa/careers",               "platform": "custom"},
}

INTERN_KEYWORDS = ["intern", "internship", "trainee", "graduate", "junior", "entry", "summer"]


def fetch_greenhouse(slug: str, filter_kw: list = None) -> list:
    """Fetch open roles from Greenhouse JSON API."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        jobs = data.get("jobs", [])
    except requests.HTTPError:
        return []
    except Exception as e:
        print(f"  Greenhouse fetch failed for {slug}: {e}")
        return []

    results = []
    for job in jobs:
        title = job.get("title", "")
        if filter_kw and not any(k in title.lower() for k in filter_kw):
            continue
        results.append({
            "title": title,
            "company": slug,
            "location": job.get("location", {}).get("name", ""),
            "url": job.get("absolute_url", ""),
            "posted": job.get("updated_at", ""),
            "platform": "Greenhouse",
        })
    return results


def fetch_lever(slug: str, filter_kw: list = None) -> list:
    """Fetch open roles from Lever JSON API."""
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        jobs = resp.json()
    except Exception as e:
        print(f"  Lever fetch failed for {slug}: {e}")
        return []

    results = []
    for job in jobs:
        title = job.get("text", "")
        if filter_kw and not any(k in title.lower() for k in filter_kw):
            continue
        cats = job.get("categories", {})
        results.append({
            "title": title,
            "company": slug,
            "location": cats.get("location", ""),
            "url": job.get("hostedUrl", ""),
            "posted": "",
            "platform": "Lever",
        })
    return results


def fetch_ashby(slug: str, filter_kw: list = None) -> list:
    """Fetch open roles from Ashby JSON API."""
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        jobs = data.get("jobPostings", [])
    except Exception as e:
        print(f"  Ashby fetch failed for {slug}: {e}")
        return []

    results = []
    for job in jobs:
        title = job.get("title", "")
        if filter_kw and not any(k in title.lower() for k in filter_kw):
            continue
        results.append({
            "title": title,
            "company": slug,
            "location": job.get("locationName", ""),
            "url": job.get("jobUrl", ""),
            "posted": job.get("publishedDate", ""),
            "platform": "Ashby",
        })
    return results


def fetch_custom_page(company_info: dict, filter_kw: list = None) -> list:
    """
    Fetch a custom careers page.
    Returns a minimal result indicating the page was checked.
    Full parsing requires Claude to read the page content.
    """
    url = company_info["url"]
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        status = resp.status_code
    except Exception as e:
        status = f"error: {e}"

    return [{
        "title": "[Fetch page in Claude for full listing]",
        "company": company_info["name"],
        "location": "Saudi Arabia",
        "url": url,
        "posted": "",
        "platform": f"Custom ({status})",
    }]


def print_results(results: list):
    if not results:
        print("  No matching roles found.")
        return
    for r in results:
        print(f"\n  [{r['platform']}] {r['title']}")
        print(f"  Company:  {r['company']}")
        print(f"  Location: {r['location']}")
        print(f"  Link:     {r['url']}")


def save_results(results: list, path: str = "data/search_results.tsv"):
    """Append results to TSV file."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_header = not out.exists()
    with open(out, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "url", "posted", "platform"], delimiter="\t")
        if write_header:
            writer.writeheader()
        writer.writerows(results)
    print(f"\n✓ Results saved to {path}")


def main():
    parser = argparse.ArgumentParser(description="Search jobs via direct API endpoints")
    parser.add_argument("--company", help="Company slug (e.g. sdaia, stripe, foodics)")
    parser.add_argument("--platform", choices=["greenhouse", "lever", "ashby", "auto"], default="auto")
    parser.add_argument("--all", action="store_true", help="Scan all Saudi companies in reference list")
    parser.add_argument("--filter", default="intern", help="Keyword filter (default: intern)")
    parser.add_argument("--role", help="Role title keyword to search for")
    parser.add_argument("--location", help="Location hint (informational only)")
    parser.add_argument("--research", help="Research mode: fetch and print company info")
    parser.add_argument("--save", action="store_true", help="Save results to data/search_results.tsv")
    args = parser.parse_args()

    filter_kw = [k.lower() for k in (args.filter or "intern").split(",")] if not args.role else [args.role.lower()]

    all_results = []

    if args.research:
        slug = args.research.lower()
        info = SAUDI_COMPANIES.get(slug)
        if info:
            print(f"\nCompany: {info['name']}")
            print(f"Careers URL: {info['url']}")
            print(f"ATS Platform: {info['platform']}")
        else:
            print(f"'{args.research}' not in Saudi reference list.")
            print("Trying Greenhouse/Lever/Ashby anyway...")
            for fn, name in [(fetch_greenhouse, "Greenhouse"), (fetch_lever, "Lever"), (fetch_ashby, "Ashby")]:
                r = fn(slug, filter_kw)
                if r:
                    print(f"Found on {name}:")
                    print_results(r)
                    break
        return

    if args.all:
        print(f"Scanning {len(SAUDI_COMPANIES)} Saudi companies (filter: {filter_kw})...\n")
        for slug, info in SAUDI_COMPANIES.items():
            print(f"→ {info['name']}...")
            platform = info["platform"]
            if platform == "greenhouse":
                results = fetch_greenhouse(slug, filter_kw)
            elif platform == "lever":
                results = fetch_lever(slug, filter_kw)
            elif platform == "ashby":
                results = fetch_ashby(slug, filter_kw)
            else:
                results = fetch_custom_page(info, filter_kw)
            if results:
                print_results(results)
                all_results.extend(results)

    elif args.company:
        slug = args.company.lower()
        print(f"Searching {slug} (filter: {filter_kw})...\n")

        if args.platform == "auto" or args.platform == "greenhouse":
            results = fetch_greenhouse(slug, filter_kw)
            if results:
                print_results(results)
                all_results.extend(results)

        if not all_results and (args.platform in ("auto", "lever")):
            results = fetch_lever(slug, filter_kw)
            if results:
                print_results(results)
                all_results.extend(results)

        if not all_results and (args.platform in ("auto", "ashby")):
            results = fetch_ashby(slug, filter_kw)
            if results:
                print_results(results)
                all_results.extend(results)

        if not all_results:
            info = SAUDI_COMPANIES.get(slug)
            if info:
                results = fetch_custom_page(info, filter_kw)
                print_results(results)
                all_results.extend(results)
            else:
                print(f"No results found for '{slug}' on any platform.")

    else:
        parser.print_help()
        return

    if args.save and all_results:
        save_results(all_results)

    print(f"\n{len(all_results)} total results found.")


if __name__ == "__main__":
    main()
