"""
fit_score.py
Score a job opportunity against the candidate profile using the 6-dimension rubric.
Reads data/profile.md for candidate context.

Usage:
    python scripts/fit_score.py --job "url or job description text"
    python scripts/fit_score.py --job job.txt --profile data/profile.md
    python scripts/fit_score.py --compare job_a.txt job_b.txt job_c.txt
"""

import argparse
import sys
from pathlib import Path

DIMENSIONS = [
    {
        "key": "technical_fit",
        "label": "Technical fit",
        "description": "Does the required stack match what the candidate has actually used in real projects?",
        "score_guide": {
            5: "Used 80%+ of listed tools in real projects",
            4: "Used most tools, one or two gaps",
            3: "Used about half, knows the rest conceptually",
            2: "Some overlap but significant gaps",
            1: "Almost no overlap, major ramp-up required",
        },
    },
    {
        "key": "seniority_match",
        "label": "Seniority match",
        "description": "Is this role calibrated to the candidate's current level?",
        "score_guide": {
            5: "Exactly right level, small stretch at most",
            4: "Slightly senior but achievable",
            3: "Moderate stretch, possible with strong application",
            2: "Too senior — not credible, or too junior — wasted",
            1: "Clearly out of range in either direction",
        },
    },
    {
        "key": "location_logistics",
        "label": "Location / logistics",
        "description": "Is the location, remote policy, and timing compatible?",
        "score_guide": {
            5: "Perfect match, no friction",
            4: "Minor adjustment needed",
            3: "Workable with some flexibility",
            2: "Significant logistical hurdle",
            1: "Requires relocation, sponsorship, or timing ruled out",
        },
    },
    {
        "key": "growth_potential",
        "label": "Growth potential",
        "description": "Will this role improve the candidate's profile in 12 months?",
        "score_guide": {
            5: "Strong brand, real ownership, mentorship, high network value",
            4: "Good experience, solid network",
            3: "Decent experience, moderate network",
            2: "Limited learning or weak brand",
            1: "Filler role — no strategic upside",
        },
    },
    {
        "key": "reachability",
        "label": "Reachability",
        "description": "How realistic is an interview given the candidate's profile?",
        "score_guide": {
            5: "Strong match, not oversubscribed — very likely to get an interview",
            4: "Competitive but possible",
            3: "Possible with a strong application",
            2: "Unlikely without a connection or referral",
            1: "Very unlikely — overqualified applicants or top-tier requirement",
        },
    },
    {
        "key": "strategic_value",
        "label": "Strategic value",
        "description": "Does this role add long-term leverage?",
        "score_guide": {
            5: "Opens doors to next-tier roles, key network, target domain",
            4: "Strong stepping stone",
            3: "Solid but not transformational",
            2: "Limited strategic upside",
            1: "No meaningful leverage in the candidate's target field",
        },
    },
]

THRESHOLDS = [
    (25, "Strong Match",   "Invest full tailored materials — LaTeX CV, cover letter, ATS sheet"),
    (18, "Moderate Match", "Worth applying with standard tailoring"),
    (12, "Weak Match",     "Flag concerns to candidate before investing time"),
    (0,  "Skip",           "Not worth the candidate's time — explain why"),
]


def get_verdict(total: int) -> tuple:
    for threshold, label, action in THRESHOLDS:
        if total >= threshold:
            return label, action
    return "Skip", "Not worth applying"


def score_interactively(job_text: str, profile_text: str) -> dict:
    """
    Interactive scoring mode.
    Claude (or the user running locally) provides scores 1-5 for each dimension.
    """
    print("\n" + "=" * 60)
    print("FIT SCORING")
    print("=" * 60)
    print("\nJob description (first 300 chars):")
    print(job_text[:300])
    if profile_text:
        print("\nCandidate profile (first 200 chars):")
        print(profile_text[:200])
    print("\nScore each dimension 1-5 (or press Enter to skip):")
    print()

    scores = {}
    reasons = {}

    for dim in DIMENSIONS:
        print(f"{dim['label']}")
        print(f"  {dim['description']}")
        for score, guide in sorted(dim["score_guide"].items(), reverse=True):
            print(f"  {score} = {guide}")
        while True:
            raw = input(f"  Score (1-5): ").strip()
            if raw == "":
                scores[dim["key"]] = None
                reasons[dim["key"]] = "Not scored"
                break
            try:
                val = int(raw)
                if 1 <= val <= 5:
                    scores[dim["key"]] = val
                    reason = input(f"  Reason (one sentence): ").strip()
                    reasons[dim["key"]] = reason or dim["score_guide"][val]
                    break
                else:
                    print("  Enter a number between 1 and 5.")
            except ValueError:
                print("  Enter a number between 1 and 5.")
        print()

    return scores, reasons


def format_score_output(scores: dict, reasons: dict, label: str = "") -> str:
    total = sum(v for v in scores.values() if v is not None)
    verdict, action = get_verdict(total)

    lines = [f"\n## Fit Score{': ' + label if label else ''}\n"]
    for dim in DIMENSIONS:
        key = dim["key"]
        score = scores.get(key, "—")
        reason = reasons.get(key, "")
        lines.append(f"{dim['label']:<22} {score}/5 — {reason}")

    lines.append("")
    lines.append(f"Total: {total}/30")
    lines.append(f"Verdict: {verdict}")
    lines.append(f"Recommendation: {action}")

    return "\n".join(lines)


def compare_jobs(job_files: list, profile_text: str) -> str:
    """Score multiple jobs and produce a comparison table."""
    all_scores = []
    all_reasons = []
    labels = []

    for jf in job_files:
        path = Path(jf)
        job_text = path.read_text(encoding="utf-8") if path.exists() else jf
        label = path.stem if path.exists() else jf[:20]
        print(f"\n{'='*60}")
        print(f"Scoring: {label}")
        scores, reasons = score_interactively(job_text, profile_text)
        all_scores.append(scores)
        all_reasons.append(reasons)
        labels.append(label)

    # Build comparison table
    lines = ["\n## Opportunity Comparison\n"]
    header = "| Dimension             |" + "".join(f" {l[:12]:<12} |" for l in labels)
    sep    = "|---|" + "---|" * len(labels)
    lines.append(header)
    lines.append(sep)

    for dim in DIMENSIONS:
        row = f"| {dim['label']:<21} |"
        for scores in all_scores:
            v = scores.get(dim["key"], "—")
            row += f" {str(v):<12} |"
        lines.append(row)

    # Totals row
    totals = [sum(v for v in s.values() if v is not None) for s in all_scores]
    row = f"| **Total /30**          |"
    for t in totals:
        row += f" **{t}**          |"
    lines.append(row)

    lines.append("")
    # Ranking
    ranked = sorted(zip(totals, labels), reverse=True)
    lines.append("**Priority:**")
    for i, (total, label) in enumerate(ranked, 1):
        verdict, action = get_verdict(total)
        lines.append(f"{i}. {label} ({total}/30) — {verdict} — {action}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fit score a job against the candidate profile")
    parser.add_argument("--job", help="Job description text, file path, or URL")
    parser.add_argument("--profile", default="data/profile.md", help="Candidate profile file")
    parser.add_argument("--compare", nargs="+", help="Compare multiple job files")
    parser.add_argument("--output", help="Save output to file")
    args = parser.parse_args()

    # Load profile
    profile_text = ""
    profile_path = Path(args.profile)
    if profile_path.exists():
        profile_text = profile_path.read_text(encoding="utf-8")

    if args.compare:
        output = compare_jobs(args.compare, profile_text)
    elif args.job:
        job_path = Path(args.job)
        job_text = job_path.read_text(encoding="utf-8") if job_path.exists() else args.job
        scores, reasons = score_interactively(job_text, profile_text)
        output = format_score_output(scores, reasons)
    else:
        parser.print_help()
        return

    print(output)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n✓ Score saved to {args.output}")


if __name__ == "__main__":
    main()
