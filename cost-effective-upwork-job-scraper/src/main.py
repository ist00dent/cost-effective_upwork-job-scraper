"""Module defines the main entry point for the Apify Actor.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from apify import Actor  # type: ignore  # For linter: apify is installed at runtime
from .browser import launch_stealth_browser
from .navigator import build_search_url, navigate_to_search_page
from .parser import parse_job_listings
from .job_detail import parse_job_detail
from .utils import log_progress, retry_on_failure
import asyncio

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        keyword = str(actor_input.get("keyword", ""))
        location = str(actor_input.get("location", ""))
        if not keyword or not location:
            await log_progress("Missing required input: keyword or location.")
            await Actor.exit()

        await log_progress(f"Launching browser for keyword='{keyword}', location='{location}'...")
        playwright, browser, context = await launch_stealth_browser()
        page = await context.new_page()
        try:
            search_url = await build_search_url(keyword, location)
            await log_progress(f"Navigating to search URL: {search_url}")
            await retry_on_failure(navigate_to_search_page, page, search_url)
            html = await page.content()
            jobs = await parse_job_listings(html)
            await log_progress(f"Found {len(jobs)} jobs on search page.")
            results = []
            for job in jobs:
                job_link = job.get("jobLink")
                if not job_link:
                    continue
                await log_progress(f"Navigating to job: {job_link}")
                await retry_on_failure(page.goto, job_link, wait_until="networkidle")
                await asyncio.sleep(2)  # Human-like delay
                job_html = await page.content()
                job_details = await parse_job_detail(job_html)
                # Merge summary fields (jobTitle, jobLink, jobId) with details
                job_details["jobTitle"] = job.get("jobTitle") or job_details.get("jobTitle")
                job_details["jobLink"] = job_link
                job_details["jobId"] = job.get("jobId") or job_details.get("jobId")
                await log_progress(f"Scraped job: {job_details.get('jobTitle')}")
                await Actor.push_data(job_details)
                results.append(job_details)
            await log_progress(f"Scraping complete. Total jobs scraped: {len(results)}")
        finally:
            await browser.close()
            await playwright.stop()
