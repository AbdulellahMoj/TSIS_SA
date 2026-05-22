"""
cv_parser.py
Parse a CV from PDF or plain text and extract structured data.
Output saved to data/profile.md (appended to existing profile).

Usage:
    python scripts/cv_parser.py --file path/to/cv.pdf
    python scripts/cv_parser.py --text "paste CV text here"
    python scripts/cv_parser.py --file cv.pdf --output data/cv_parsed.md
"""

import argparse
import sys
import os
import re
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract plain text from a PDF file using pdfminer."""
    try:
        from pdfminer.high_level import extract_text
        return extract_text(pdf_path)
    except ImportError:
        print("ERROR: pdfminer.six not installed. Run: pip install pdfminer.six")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR reading PDF: {e}")
        sys.exit(1)


def extract_sections(text: str) -> dict:
    """
    Heuristically extract CV sections from raw text.
    Returns a dict of section_name -> content.
    """
    # Common section headers in CVs
    section_patterns = [
        r"education",
        r"experience",
        r"work experience",
        r"projects?",
        r"skills?",
        r"technical skills?",
        r"certifications?",
        r"awards?",
        r"publications?",
        r"leadership",
        r"activities",
        r"volunteering",
        r"extracurricular",
        r"languages?",
        r"summary",
        r"objective",
        r"profile",
    ]

    # Build regex to find section headers (all caps or title case on own line)
    header_re = re.compile(
        r"^[ \t]*(" + "|".join(section_patterns) + r")[s]?[ \t]*$",
        re.IGNORECASE | re.MULTILINE,
    )

    sections = {}
    lines = text.splitlines()
    current_section = "header"
    current_content = []

    for line in lines:
        if header_re.match(line.strip()):
            # Save previous section
            sections[current_section] = "\n".join(current_content).strip()
            current_section = line.strip().lower()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    sections[current_section] = "\n".join(current_content).strip()

    return sections


def extract_contact_info(header_text: str) -> dict:
    """Pull name, email, phone, LinkedIn, GitHub from the header block."""
    info = {}

    # Email
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", header_text, re.IGNORECASE)
    if email_match:
        info["email"] = email_match.group()

    # Phone (Saudi and international formats)
    phone_match = re.search(r"(\+966|00966|05)\d{8,9}", header_text)
    if phone_match:
        info["phone"] = phone_match.group()

    # LinkedIn
    linkedin_match = re.search(r"linkedin\.com/in/[\w-]+", header_text, re.IGNORECASE)
    if linkedin_match:
        info["linkedin"] = "https://" + linkedin_match.group()

    # GitHub
    github_match = re.search(r"github\.com/[\w-]+", header_text, re.IGNORECASE)
    if github_match:
        info["github"] = "https://" + github_match.group()

    # Name (assume first non-empty line of header is the name)
    for line in header_text.splitlines():
        line = line.strip()
        if line and len(line.split()) <= 5 and "@" not in line:
            info["name"] = line
            break

    return info


def format_parsed_output(sections: dict, contact: dict) -> str:
    """Format extracted data as a structured markdown profile."""
    lines = ["# Parsed CV\n"]

    # Contact
    lines.append("## Contact Info")
    for key, val in contact.items():
        lines.append(f"- **{key.capitalize()}:** {val}")
    lines.append("")

    # Each section
    for section, content in sections.items():
        if section == "header" or not content.strip():
            continue
        lines.append(f"## {section.title()}")
        lines.append(content)
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Parse a CV from PDF or text")
    parser.add_argument("--file", help="Path to CV PDF")
    parser.add_argument("--text", help="Raw CV text (paste directly)")
    parser.add_argument(
        "--output",
        default="data/cv_parsed.md",
        help="Output path (default: data/cv_parsed.md)",
    )
    args = parser.parse_args()

    if not args.file and not args.text:
        print("ERROR: Provide --file or --text")
        sys.exit(1)

    # Extract text
    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"ERROR: File not found: {args.file}")
            sys.exit(1)
        if path.suffix.lower() == ".pdf":
            raw_text = extract_text_from_pdf(str(path))
        else:
            raw_text = path.read_text(encoding="utf-8")
    else:
        raw_text = args.text

    # Parse
    sections = extract_sections(raw_text)
    contact = extract_contact_info(sections.get("header", raw_text[:500]))
    output = format_parsed_output(sections, contact)

    # Write
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    print(f"✓ Parsed CV written to {out_path}")

    # Print summary
    print(f"\nExtracted sections: {[s for s in sections if s != 'header']}")
    if contact:
        print(f"Contact info found: {list(contact.keys())}")


if __name__ == "__main__":
    main()
