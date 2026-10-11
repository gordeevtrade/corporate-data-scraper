# Corporate Data Scraper
### A Free, Lightweight Open-Source Alternative to Firecrawl for B2B & Lead Gen Teams

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Alternative: Firecrawl](https://img.shields.io/badge/Alternative-Firecrawl%20(Zero%20Cost)-emerald.svg)]()
[![Bypass: HTTP 403 / Anti--Bot](https://img.shields.io/badge/Bypass-HTTP%20403%20Protected-orange.svg)]()

> **A fast, self-hosted web scraping engine designed to extract corporate team rosters, executive biographies, and practice area competencies without paying for expensive scraping API subscriptions.**

---

## 💡 The Philosophy: Why Pay Firecrawl for Simple B2B Extraction?

Services like **Firecrawl** are fantastic if you have a massive venture budget. But for outbound sales teams, recruiters, and lead generation specialists, paying **\$50–\$200/month** just to scrape a few hundred team pages and company bios makes no economic sense.

| Feature | Firecrawl (Cloud API) | Corporate Data Scraper (This Repo) |
| :--- | :--- | :--- |
| **Monthly Subscription** | **\$50 – \$200+ / mo** | **\$0 (100% Free & Open Source)** |
| **Credit / Page Limits** | Hard monthly limits & overage fees | **Unlimited self-hosted scraping** |
| **HTTP 403 Anti-Bot Bypass** | Cloud managed | **Built-in browser header emulation** |
| **Team & Bio Extraction** | Raw markdown (needs LLM parsing) | **Pre-structured JSON with names, emails, roles** |
| **Zero Snippet Policy** | May truncate long competence blocks | **Guaranteed full block extraction** |
| **Data Privacy** | Sent to third-party servers | **Runs 100% locally on your machine** |

---

## ⚡ Core Features

- 🛡️ **HTTP 403 / Forbidden Bypass:** Rotates realistic Chrome/Firefox User-Agents, Sec-CH headers, and navigation profiles to navigate sites that block basic scrapers.
- 👥 **Executive & Team Roster Parser:** Automatically identifies person cards, leadership listings, and partner bio blocks.
- 🎯 **Zero Snippet Policy (Full Competencies):** Extracts entire competence lists (*Kompetens, Verksamhetsområden, Practice Areas, Specialties*) without relying on truncated search snippets.
- 🧹 **Boilerplate Stripper:** Automatically deletes cookies, navbars, footers, scripts, and trackers, leaving only high-signal text.
- 🤖 **LLM-Ready JSON / Markdown:** Directly feeds into OpenAI, Anthropic, or local AI agents for outbound personalization.

---

## 🏗️ Architecture

```
[Target Website URL]
        │
        ▼
 [SmartFetcher]          ──► Emulates Chrome headers, bypasses 403 blocks & handles retries
        │
   (Raw HTML)
        ├──► [HTMLCleaner]    ──► Strips chrome, nav & scripts ──► Clean Markdown
        │
        └──► [TeamBioParser]  ──► Locates employee cards, emails, phones & full practice areas
                                    │
                                    ▼
                         [Structured Output: JSON / Pydantic Models]
```

---

## 🚀 Quickstart & Usage

### 1. Clone the Repository
```bash
git clone git@github.com:gordeevtrade/corporate-data-scraper.git
cd corporate-data-scraper
```

### 2. Install Dependencies
Only 2 lightweight dependencies required (no heavy headless browser installs needed):
```bash
pip install -r requirements.txt
```

### 3. Run Demo Mode (Offline Sample)
Test the parser immediately without touching the web:
```bash
python main.py --demo
```

### 4. Scrape Any Corporate Website
```bash
python main.py --url "https://nordicproperty.se/team" --output team_leads.json
```

---

## 📋 Sample Extracted Output

```json
{
  "url": "https://nordicproperty.se/team",
  "total_members_found": 3,
  "members": [
    {
      "name": "Anders Lindström",
      "title": "Chef Fastighetsutveckling & Partner",
      "email": "anders.lindstrom@nordicproperty.se",
      "phone": "+4640123456",
      "bio_summary": "Anders har över 20 års erfarenhet av storskalig projektutveckling...",
      "competencies": [
        "Fastighetsutveckling",
        "Entreprenadrätt",
        "Kommersiell förvaltning",
        "Stadsplanering & Detaljplaner"
      ]
    },
    {
      "name": "Malin Bergström",
      "title": "Senior Projektchef Stadsutveckling",
      "email": "malin.bergstrom@nordicproperty.se",
      "phone": "+4640654321",
      "competencies": [
        "Kommunala planprocesser",
        "Bostadsutveckling",
        "Fastighetsrätt"
      ]
    }
  ],
  "status": "SUCCESS"
}
```

---

## 📁 Repository Structure

```
├── data/
│   └── sample_team_page.html       # Local mock corporate website for tests
├── src/
│   ├── core/
│   │   ├── cleaner.py              # HTML sanitizer and markdown generator
│   │   └── fetcher.py              # 403 bypass and HTTP client
│   ├── parsers/
│   │   └── team_parser.py          # Executive roster & practice areas extractor
│   ├── models.py                   # Clean data models (TeamMember, ScrapeResult)
│   └── __init__.py
├── .gitignore                      # Temporary data and cache ignore rules
├── LICENSE                         # MIT License
├── main.py                         # CLI entrypoint
└── requirements.txt                # Python dependencies
```

---

## 👤 Author & Connect
**Artem Ryzhov**  
*Lead Generation & RevOps Automation Engineer*  
- **GitHub:** [@gordeevtrade](https://github.com/gordeevtrade)  
- **LinkedIn:** [Artem Ryzhov](https://www.linkedin.com/in/)

---
*License: [MIT](LICENSE) © 2026 Artem Ryzhov*
