"""
BeautifulSoup scraping logic for Upwork job listings.
"""
from bs4 import BeautifulSoup

async def parse_job_listings(html: str):
    """
    Parses the job listings from the search results HTML.
    Returns a list of job summary dicts (with jobLink, jobTitle, etc.).
    """
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    # Upwork job cards are usually in <section> or <div> with data-test/job-tile or similar
    for job_card in soup.find_all("section", {"data-test": "job-tile-list-item"}):
        title_tag = job_card.find("a", {"data-test": "job-title-link"})
        job_link = "https://www.upwork.com" + title_tag["href"] if title_tag else None
        job_title = title_tag.get_text(strip=True) if title_tag else None
        job_id = job_card.get("data-job-id")
        jobs.append({
            "jobTitle": job_title,
            "jobLink": job_link,
            "jobId": job_id,
        })
    return jobs 