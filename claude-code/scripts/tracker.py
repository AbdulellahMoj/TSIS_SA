"""
tracker.py
Manage the application pipeline in data/tracker.tsv.
Supports add, update, list, follow-ups, and summary.

Usage:
    python scripts/tracker.py --list
    python scripts/tracker.py --add --company "SDAIA" --role "AI Intern" --date "2026-06-01" --link "https://..."
    python scripts/tracker.py --update --company "SDAIA" --status "interview_scheduled" --notes "June 10"
    python scripts/tracker.py --followups
    python scripts/tracker.py --status-summary
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

TRACKER_PATH = Path("data/tracker.tsv")
FIELDS = ["company", "role", "applied_date", "status", "follow_up_date", "notes", "link"]

VALID_STATUSES = [
    "applied",
    "followed_up",
    "interview_scheduled",
    "interview_done",
    "offer",
    "rejected",
    "ghosted",
    "withdrawn",
]

STATUS_EMOJI = {
    "applied":              "📤",
    "followed_up":          "📬",
    "interview_scheduled":  "📅",
    "interview_done":       "✅",
    "offer":                "🎉",
    "rejected":             "❌",
    "ghosted":              "👻",
    "withdrawn":            "↩️",
}

FOLLOW_UP_DAYS = 7


# ── I/O ───────────────────────────────────────────────────────────────────────

def load_tracker() -> list:
    if not TRACKER_PATH.exists():
        return []
    with open(TRACKER_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def save_tracker(rows: list):
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKER_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def today_str() -> str:
    return datetime.today().strftime("%Y-%m-%d")


def follow_up_date(applied: str) -> str:
    try:
        d = datetime.strptime(applied, "%Y-%m-%d")
        return (d + timedelta(days=FOLLOW_UP_DAYS)).strftime("%Y-%m-%d")
    except ValueError:
        return ""


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_add(args):
    rows = load_tracker()

    # Check for duplicate
    for row in rows:
        if row["company"].lower() == args.company.lower() and row["role"].lower() == args.role.lower():
            print(f"⚠️  Entry already exists for {args.company} / {args.role}")
            print("Use --update to change its status.")
            return

    date = args.date or today_str()
    new_row = {
        "company":       args.company,
        "role":          args.role,
        "applied_date":  date,
        "status":        "applied",
        "follow_up_date": follow_up_date(date),
        "notes":         args.notes or "",
        "link":          args.link or "",
    }
    rows.append(new_row)
    save_tracker(rows)
    print(f"✓ Added: {args.company} — {args.role} (applied {date})")
    print(f"  Follow-up due: {new_row['follow_up_date']}")


def cmd_update(args):
    rows = load_tracker()
    found = False

    for row in rows:
        if row["company"].lower() == args.company.lower():
            if args.status:
                if args.status not in VALID_STATUSES:
                    print(f"Invalid status. Valid values: {', '.join(VALID_STATUSES)}")
                    sys.exit(1)
                row["status"] = args.status
                # Reset follow-up date on follow-up action
                if args.status == "followed_up":
                    row["follow_up_date"] = (
                        datetime.today() + timedelta(days=FOLLOW_UP_DAYS)
                    ).strftime("%Y-%m-%d")
            if args.notes:
                row["notes"] = args.notes
            if args.link:
                row["link"] = args.link
            found = True
            print(f"✓ Updated: {row['company']} — {row['role']} → {row['status']}")

    if not found:
        print(f"No entry found for company: {args.company}")
        print("Use --add to log a new application.")
        return

    save_tracker(rows)


def cmd_list(args):
    rows = load_tracker()
    if not rows:
        print("Pipeline is empty. Use --add to log your first application.")
        return

    active = [r for r in rows if r["status"] not in ("rejected", "ghosted", "withdrawn", "offer")]
    closed = [r for r in rows if r["status"] in ("rejected", "ghosted", "withdrawn", "offer")]

    print(f"\n{'='*70}")
    print(f"APPLICATION PIPELINE — {today_str()}")
    print(f"{'='*70}")
    print(f"Active: {len(active)}   Closed: {len(closed)}   Total: {len(rows)}")
    print()

    if active:
        print("ACTIVE")
        print(f"{'Company':<20} {'Role':<25} {'Applied':<12} {'Status':<22} {'Follow-up'}")
        print("-" * 95)
        for r in sorted(active, key=lambda x: x["applied_date"], reverse=True):
            emoji = STATUS_EMOJI.get(r["status"], "•")
            print(f"{r['company']:<20} {r['role']:<25} {r['applied_date']:<12} "
                  f"{emoji} {r['status']:<20} {r['follow_up_date']}")

    if closed:
        print("\nCLOSED")
        for r in sorted(closed, key=lambda x: x["applied_date"], reverse=True):
            emoji = STATUS_EMOJI.get(r["status"], "•")
            print(f"  {emoji} {r['company']:<20} {r['role']:<25} {r['status']}")


def cmd_followups(args):
    rows = load_tracker()
    today = datetime.today()

    due = []
    for r in rows:
        if r["status"] in ("applied", "followed_up") and r["follow_up_date"]:
            try:
                fu_date = datetime.strptime(r["follow_up_date"], "%Y-%m-%d")
                days_overdue = (today - fu_date).days
                if days_overdue >= 0:
                    due.append((days_overdue, r))
            except ValueError:
                continue

    if not due:
        print("No follow-ups due today. Good shape.")
        return

    print(f"\n⚠️  FOLLOW-UPS DUE ({len(due)})\n")
    for days, r in sorted(due, key=lambda x: x[0], reverse=True):
        overdue_str = f"{days} day{'s' if days != 1 else ''} overdue" if days > 0 else "due today"
        print(f"  {r['company']:<20} {r['role']:<25} applied {r['applied_date']} — {overdue_str}")
        if r["notes"]:
            print(f"    Notes: {r['notes']}")

    print("\nRun: python scripts/tracker.py --update --company [name] --status followed_up")


def cmd_summary(args):
    rows = load_tracker()
    if not rows:
        print("No applications logged yet.")
        return

    by_status = {}
    for r in rows:
        s = r["status"]
        by_status[s] = by_status.get(s, 0) + 1

    print(f"\n{'='*40}")
    print(f"PIPELINE SUMMARY — {today_str()}")
    print(f"{'='*40}")
    print(f"Total applications: {len(rows)}")
    print()
    for status in VALID_STATUSES:
        count = by_status.get(status, 0)
        if count:
            emoji = STATUS_EMOJI.get(status, "•")
            print(f"  {emoji} {status:<22} {count}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Manage application pipeline")

    parser.add_argument("--add", action="store_true", help="Add a new application")
    parser.add_argument("--update", action="store_true", help="Update an existing entry")
    parser.add_argument("--list", action="store_true", help="List all applications")
    parser.add_argument("--followups", action="store_true", help="Show follow-ups due")
    parser.add_argument("--status-summary", action="store_true", help="Show summary by status")

    parser.add_argument("--company", help="Company name")
    parser.add_argument("--role", help="Role title")
    parser.add_argument("--date", help="Application date (YYYY-MM-DD), defaults to today")
    parser.add_argument("--status", help=f"Status: {', '.join(VALID_STATUSES)}")
    parser.add_argument("--notes", help="Notes")
    parser.add_argument("--link", help="Job listing URL")

    args = parser.parse_args()

    if args.add:
        if not args.company or not args.role:
            print("--add requires --company and --role")
            sys.exit(1)
        cmd_add(args)
    elif args.update:
        if not args.company:
            print("--update requires --company")
            sys.exit(1)
        cmd_update(args)
    elif args.list:
        cmd_list(args)
    elif args.followups:
        cmd_followups(args)
    elif args.status_summary:
        cmd_summary(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
