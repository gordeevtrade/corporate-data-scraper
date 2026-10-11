"""
Corporate Data Scraper - Command Line Interface (CLI)
A free, open-source alternative to Firecrawl for B2B lead generation teams.
"""

import sys
import os
import json
import argparse

# Add src to python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Support UTF-8 terminal printing
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from core.fetcher import SmartFetcher
from core.cleaner import clean_html_to_markdown
from parsers.team_parser import TeamBioParser
from models import ScrapeResult

def run_scraper(target_url: str, output_file: str = None, as_markdown: bool = False):
    print("=" * 70)
    print(">>> CORPORATE DATA SCRAPER (Firecrawl Free Alternative)")
    print(f"[*] Target: {target_url}")
    print("=" * 70)

    fetcher = SmartFetcher()
    try:
        raw_html = fetcher.fetch(target_url)
        print(f"[OK] Fetched {len(raw_html)} bytes of raw HTML.")
    except Exception as e:
        print(f"[ERROR] Failed to fetch target URL: {e}")
        return

    # 1. Clean HTML to Markdown
    markdown_content = clean_html_to_markdown(raw_html)

    # 2. Extract structured team members and competencies
    parser = TeamBioParser(raw_html)
    members = parser.extract_members()

    result = ScrapeResult(
        url=target_url,
        total_members_found=len(members),
        members=members,
        markdown_content=markdown_content if as_markdown else None
    )

    print(f"[OK] Extraction complete: Found {len(members)} executive/team profiles.")
    print("-" * 70)
    for i, m in enumerate(members, 1):
        print(f"  {i}. {m.name} | {m.title or 'N/A'}")
        if m.email:
            print(f"     Email: {m.email}")
        if m.phone:
            print(f"     Phone: {m.phone}")
        if m.competencies:
            print(f"     Competencies: {', '.join(m.competencies)}")
        print()

    # Save output if requested or default demo
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.to_json(indent=2))
        print(f"[OK] Results saved to: {output_file}")

    return result

def main():
    parser = argparse.ArgumentParser(description="Corporate Data Scraper - Free Firecrawl Alternative")
    parser.add_argument("--url", type=str, help="Target website URL or local HTML file")
    parser.add_argument("--demo", action="store_true", help="Run with local sample team page")
    parser.add_argument("--output", type=str, default="extracted_team.json", help="Path to save output JSON")
    parser.add_argument("--markdown", action="store_true", help="Include full cleaned Markdown content in output")

    args = parser.parse_args()

    if args.demo or not args.url:
        sample_path = os.path.join(os.path.dirname(__file__), "data", "sample_team_page.html")
        print("[*] Running in DEMO mode with local corporate team dataset...")
        run_scraper(sample_path, output_file=args.output, as_markdown=args.markdown)
    else:
        run_scraper(args.url, output_file=args.output, as_markdown=args.markdown)

if __name__ == "__main__":
    main()
