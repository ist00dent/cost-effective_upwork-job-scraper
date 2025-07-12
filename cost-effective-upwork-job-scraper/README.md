# cost-effective_upwork-job-scraper

**Owner:** Carl Kendrick B. Camus

## Objective
A scalable, human-like Upwork job scraper built as an Apify Actor using Playwright. Collects complete job listings using search keyword and location input, bypasses bot detection, and follows best practices for modular, debuggable code.

## Features
- Playwright-based browser automation (stealth mode, no cookies)
- Human-like navigation, scrolling, and delays
- Modular code: browser, navigator, parser, job_detail, utils
- Logs progress per job for debugging
- Retry logic for failures or bot detection
- **Two-tier scraping**: Search results (no auth) + Detailed job info (with auth)

## Inputs
| Field    | Type   | Required | Description                       |
|----------|--------|----------|-----------------------------------|
| keyword  | string | ✅        | Job title or keyword (e.g., "python dev") |
| location | string | ✅        | Geographic filter (e.g., "United States") |

## Outputs

### Search Results (Always Available - No Cookies Required)
```
{
  "jobTitle": "Data Analyst Needed for Market Research",
  "jobLink": "https://www.upwork.com/job/...",
  "jobId": "3821938712",
  "postedTime": "2 hours ago",
  "budget": "$300",
  "projectType": "One-time project",
  "experienceLevel": "Intermediate",
  "skillsRequired": ["Python", "Excel", "SQL"]
}
```

### Detailed Job Info (Requires Authentication/Cookies)
```
{
  "jobTitle": "Data Analyst Needed for Market Research",
  "jobLink": "https://www.upwork.com/job/...",
  "description": "Looking for an experienced data analyst...",
  "category": "Data Science & Analytics",
  "clientLocation": "United States",
  "clientDetails": {
    "totalSpent": "$10k+",
    "jobsPosted": 25,
    "hireRate": "90%"
  },
  "budget": "$300",
  "projectType": "One-time project",
  "postedTime": "2 hours ago",
  "skillsRequired": ["Python", "Excel", "SQL"],
  "jobId": "3821938712"
}
```

## Important Notes
- **Search Results**: Always available without authentication
- **Detailed Job Info**: May require Upwork login/cookies for full access
- **Fallback Strategy**: If detailed scraping fails, basic search results are still provided
- **Rate Limiting**: Detailed scraping is limited to first 5 jobs to avoid detection

## Architecture
```
cost-effective-upwork-job-scraper/
├── .actor/                  # Apify actor metadata
├── src/                     # Source code (modular Python files)
│   ├── main.py              # Actor entry point
│   ├── browser.py           # Stealth Playwright browser launcher
│   ├── navigator.py         # Builds search URL & handles navigation
│   ├── parser.py            # BeautifulSoup scraping logic for job listings
│   ├── job_detail.py        # Logic to scrape individual job details
│   └── utils.py             # Shared helpers (logging, formatting)
├── storage/                 # Local dataset/output storage (Apify runtime)
├── venv/                    # Virtual environment (excluded)
├── .gitignore               # Excludes venv, __pycache__, etc.
├── .dockerignore            # Files to exclude in Docker builds
├── Dockerfile               # Apify Actor container definition
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
2. Run as Apify actor or locally with Python 3.8+

## Maintenance Notes
- Each utility is self-contained, with docstrings and exception handling.
- Logging is modular and centralized for job-level/system-level tracing.
- Easy to expand with new fields or scrape strategies.
- Clear input/output schema for validation and integration.
- **Cookie Management**: For enhanced detailed scraping, consider implementing cookie/session management.
