"""
ats_fill.py
Playwright-based ATS form navigation and filling.
Reads the application answer sheet and fills the form field by field.
Always pauses before submitting — never auto-submits.

⚠️  REQUIRES Claude Code + Playwright installed.
    Run: npm install playwright && npx playwright install chromium
    This script will NOT run in claude.ai.

Usage:
    python scripts/ats_fill.py --url "https://boards.greenhouse.io/..." --application data/applications/company-slug/
    python scripts/ats_fill.py --url "https://jobs.lever.co/..." --application data/applications/company-slug/ --headless
"""

import argparse
import sys
import re
from pathlib import Path

# ── Platform detection ────────────────────────────────────────────────────────

PLATFORM_PATTERNS = {
    "greenhouse": r"boards\.greenhouse\.io",
    "lever":      r"jobs\.lever\.co",
    "workday":    r"\.myworkdayjobs\.com",
    "ashby":      r"jobs\.ashbyhq\.com",
    "workable":   r"apply\.workable\.com",
    "icims":      r"careers\.icims\.com",
    "taleo":      r"\.taleo\.net",
    "taqat":      r"taqat\.sa",
    "tamheer":    r"tamheer\.hrsd\.gov\.sa",
}


def detect_platform(url: str) -> str:
    for name, pattern in PLATFORM_PATTERNS.items():
        if re.search(pattern, url, re.IGNORECASE):
            return name
    return "unknown"


# ── Answer sheet parser ───────────────────────────────────────────────────────

def load_answer_sheet(application_dir: str) -> dict:
    """Read ats_answers.md and return field -> answer mapping."""
    path = Path(application_dir) / "ats_answers.md"
    if not path.exists():
        print(f"ERROR: Answer sheet not found at {path}")
        print("Run /ats in Claude to generate it first.")
        sys.exit(1)

    answers = {}
    current_field = None
    current_lines = []

    for line in path.read_text(encoding="utf-8").splitlines():
        # Field headers look like: "### Field Name" or "**Field:**"
        if line.startswith("### ") or (line.startswith("**") and line.endswith("**")):
            if current_field:
                answers[current_field] = "\n".join(current_lines).strip()
            current_field = line.lstrip("#* ").rstrip(":**").strip().lower()
            current_lines = []
        elif current_field and line and not line.startswith("→"):
            current_lines.append(line)

    if current_field:
        answers[current_field] = "\n".join(current_lines).strip()

    return answers


# ── Playwright form filling ───────────────────────────────────────────────────

def fill_form(url: str, answers: dict, platform: str, headless: bool = False):
    """
    Open the ATS URL in a Playwright browser and fill fields.
    Pauses before submitting for candidate review.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: Playwright not installed.")
        print("Run: npm install playwright && npx playwright install chromium")
        sys.exit(1)

    print(f"\nOpening {platform.upper()} form: {url}")
    print("(Browser will open — do not close it manually)\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle")

        filled = []
        skipped = []

        # ── Generic field filling strategy ─────────────────────────────────
        # Try to match labels to answers by text similarity
        inputs = page.query_selector_all("input, textarea, select")

        for inp in inputs:
            try:
                # Get the label for this field
                input_id = inp.get_attribute("id") or ""
                input_name = inp.get_attribute("name") or ""
                input_type = inp.get_attribute("type") or "text"
                placeholder = inp.get_attribute("placeholder") or ""

                if input_type in ("submit", "button", "hidden", "file"):
                    continue

                # Find matching label text
                label_text = ""
                if input_id:
                    label_el = page.query_selector(f"label[for='{input_id}']")
                    if label_el:
                        label_text = label_el.inner_text().strip().lower()

                # Try to match against answer sheet
                matched_answer = None
                for field_key, answer in answers.items():
                    if (field_key in label_text or
                        field_key in input_name.lower() or
                        field_key in placeholder.lower()):
                        matched_answer = answer
                        break

                if matched_answer:
                    tag = inp.evaluate("el => el.tagName.toLowerCase()")
                    if tag == "select":
                        # Try to select matching option
                        options = inp.query_selector_all("option")
                        for opt in options:
                            if matched_answer.lower() in opt.inner_text().lower():
                                opt.click()
                                break
                    elif input_type == "checkbox":
                        if matched_answer.lower() in ("yes", "true", "1"):
                            inp.check()
                    else:
                        inp.fill(matched_answer)

                    filled.append(label_text or input_name or placeholder)
                else:
                    skipped.append(label_text or input_name or placeholder or input_id)

            except Exception as field_error:
                skipped.append(f"[error: {field_error}]")
                continue

        # ── Report ──────────────────────────────────────────────────────────
        print(f"✓ Fields filled ({len(filled)}):")
        for f in filled:
            print(f"  - {f}")

        if skipped:
            print(f"\n⚠️  Fields skipped — fill manually ({len(skipped)}):")
            for s in skipped:
                if s:
                    print(f"  - {s}")

        # ── Pause before submit ──────────────────────────────────────────────
        print("\n" + "="*60)
        print("REVIEW THE FORM IN THE BROWSER BEFORE SUBMITTING.")
        print("Check every field. Correct anything that filled incorrectly.")
        print("="*60)
        confirm = input("\nType 'submit' to submit, or anything else to cancel: ").strip()

        if confirm.lower() == "submit":
            # Look for submit button
            submit_btn = page.query_selector("button[type='submit'], input[type='submit']")
            if submit_btn:
                submit_btn.click()
                page.wait_for_load_state("networkidle", timeout=15000)
                print("\n✓ Form submitted.")
                print("Log this in your tracker: python scripts/tracker.py --update ...")
            else:
                print("Could not find submit button. Submit manually in the browser.")
                input("Press Enter when done...")
        else:
            print("Cancelled. No changes submitted.")

        browser.close()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fill ATS application form using Playwright (Claude Code only)"
    )
    parser.add_argument("--url", required=True, help="ATS form URL")
    parser.add_argument("--application", required=True, help="Path to application folder (e.g. data/applications/sdaia)")
    parser.add_argument("--headless", action="store_true", help="Run browser headlessly (no window)")
    parser.add_argument("--dry-run", action="store_true", help="Print answers without opening browser")
    args = parser.parse_args()

    platform = detect_platform(args.url)
    print(f"Detected platform: {platform.upper()}")

    answers = load_answer_sheet(args.application)
    print(f"Loaded {len(answers)} answers from answer sheet")

    if args.dry_run:
        print("\n--- DRY RUN: Answer Sheet Contents ---")
        for field, answer in answers.items():
            print(f"\n[{field}]")
            print(answer[:200] + ("..." if len(answer) > 200 else ""))
        return

    fill_form(args.url, answers, platform, headless=args.headless)


if __name__ == "__main__":
    main()
