"""
linkedin_csv.py
Parse a LinkedIn connections CSV export and cross-reference against target companies.
LinkedIn exports connections from: Settings → Data Privacy → Get a copy of your data → Connections.

Usage:
    python scripts/linkedin_csv.py --file data/connections.csv
    python scripts/linkedin_csv.py --file data/connections.csv --targets config/targets.yml
    python scripts/linkedin_csv.py --file data/connections.csv --company "SDAIA"
"""

import argparse
import csv
import sys
from pathlib import Path
from collections import defaultdict


def load_connections(csv_path: str) -> list:
    """
    LinkedIn connections CSV has these columns (may vary by export):
    First Name, Last Name, Email Address, Company, Position, Connected On
    """
    path = Path(csv_path)
    if not path.exists():
        print(f"ERROR: File not found: {csv_path}")
        print("Export from: LinkedIn → Settings → Data Privacy → Get a copy of your data → Connections")
        sys.exit(1)

    connections = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        # Skip LinkedIn's header notes (first 3 lines are often metadata)
        lines = f.readlines()
        # Find the actual header row
        start_line = 0
        for i, line in enumerate(lines):
            if "First Name" in line or "first name" in line.lower():
                start_line = i
                break

        reader = csv.DictReader(lines[start_line:])
        for row in reader:
            # Normalise column names (LinkedIn sometimes uses slightly different names)
            normalised = {}
            for k, v in row.items():
                clean_key = k.strip().lower().replace(" ", "_")
                normalised[clean_key] = (v or "").strip()
            connections.append(normalised)

    return connections


def load_targets(targets_path: str) -> list:
    """Load target company names from YAML or plain text."""
    path = Path(targets_path)
    if not path.exists():
        return []

    if path.suffix in (".yml", ".yaml"):
        try:
            import yaml
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data.get("companies", [])
            return data or []
        except ImportError:
            # Fallback: read as plain text
            pass

    # Plain text: one company per line
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def get_company_name(conn: dict) -> str:
    """Extract company name from connection dict (column name varies)."""
    for key in ("company", "organization", "employer", "current_company"):
        if conn.get(key):
            return conn[key]
    return ""


def get_full_name(conn: dict) -> str:
    first = conn.get("first_name") or conn.get("firstname") or ""
    last = conn.get("last_name") or conn.get("lastname") or ""
    return f"{first} {last}".strip()


def cross_reference(connections: list, targets: list) -> dict:
    """
    For each target company, find connections who work there.
    Returns: {company_name: [list of connection dicts]}
    """
    results = defaultdict(list)

    for conn in connections:
        company = get_company_name(conn).lower()
        for target in targets:
            if target.lower() in company or company in target.lower():
                results[target].append(conn)

    return dict(results)


def print_network_report(matches: dict, targets: list, connections: list):
    print(f"\n{'='*60}")
    print("NETWORK OVERLAP REPORT")
    print(f"{'='*60}")
    print(f"Total connections: {len(connections)}")
    print(f"Target companies checked: {len(targets)}")
    print()

    found = {k: v for k, v in matches.items() if v}
    not_found = [t for t in targets if t not in found]

    if found:
        print("TARGET COMPANIES WITH CONNECTIONS FOUND:")
        for company, conns in sorted(found.items()):
            print(f"\n  {company} ({len(conns)} connection{'s' if len(conns) > 1 else ''})")
            for c in conns:
                name = get_full_name(c)
                position = c.get("position") or c.get("title") or c.get("job_title") or "Role unknown"
                connected = c.get("connected_on") or c.get("connection_date") or ""
                email = c.get("email_address") or c.get("email") or ""
                print(f"    • {name} — {position}")
                if connected:
                    print(f"      Connected: {connected}")
                if email:
                    print(f"      Email: {email}")

    if not_found:
        print(f"\nNO CONNECTIONS FOUND AT ({len(not_found)}):")
        for t in not_found:
            print(f"  - {t}")

    if found:
        print(f"\n{'='*60}")
        print("WARM OUTREACH PRIORITY")
        print(f"{'='*60}")
        print("Message these people BEFORE cold outreach to anyone else.")
        print("You already have a connection — use it.")
        print()
        print("Suggested message:")
        print("""
  Hi [Name],

  I noticed we're connected on LinkedIn — I'm targeting [Company]
  for a summer internship starting [month]. What's it like working there?
  And is there anything you'd recommend knowing going in?

  [Your Name]
""")


def main():
    parser = argparse.ArgumentParser(description="Cross-reference LinkedIn connections with target companies")
    parser.add_argument("--file", required=True, help="Path to LinkedIn connections CSV")
    parser.add_argument("--targets", help="Path to targets YAML or text file (default: config/targets.yml)")
    parser.add_argument("--company", help="Search for a specific company name")
    parser.add_argument("--output", help="Save report to file")
    args = parser.parse_args()

    connections = load_connections(args.file)
    print(f"✓ Loaded {len(connections)} connections")

    if args.company:
        targets = [args.company]
    else:
        targets_path = args.targets or "config/targets.yml"
        targets = load_targets(targets_path)
        if not targets:
            print(f"No targets found at {targets_path}")
            print("Add company names to config/targets.yml or use --company 'Company Name'")
            sys.exit(1)

    matches = cross_reference(connections, targets)
    print_network_report(matches, targets, connections)

    if args.output:
        # Simple text export
        import io
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        print_network_report(matches, targets, connections)
        sys.stdout = old_stdout
        Path(args.output).write_text(buffer.getvalue(), encoding="utf-8")
        print(f"\n✓ Report saved to {args.output}")


if __name__ == "__main__":
    main()
