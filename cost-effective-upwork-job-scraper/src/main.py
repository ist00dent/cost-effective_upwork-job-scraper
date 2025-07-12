"""Module defines the main entry point for the Apify Actor.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from apify import Actor  # type: ignore  # For linter: apify is installed at runtime
from .browser import launch_stealth_browser
from .navigator import build_search_url, navigate_to_search_page
from .parser import parse_job_listings
from .job_detail import parse_job_detail
from .utils import log_progress, retry_on_failure, is_login_required
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
            max_retries = 2
            for attempt in range(1, max_retries + 2):
                try:
                    import time
                    start_time = time.time()
                    await retry_on_failure(navigate_to_search_page, page, search_url)
                    elapsed = time.time() - start_time
                    page_title = await page.title()
                    page_url = page.url
                    await log_progress(f"After navigation attempt: Page title='{page_title}', URL='{page_url}', waited {elapsed:.2f} seconds.")
                    break  # Success, exit retry loop
                except Exception as nav_exc:
                    page_content = await page.content()
                    page_title = await page.title()
                    page_url = page.url
                    await log_progress(f"Navigation failed after {time.time() - start_time:.2f} seconds. Page title='{page_title}', URL='{page_url}'")
                    if "cloudflare" in page_content.lower() or "attention required" in page_content.lower():
                        await log_progress(f"Navigation failed due to Cloudflare or anti-bot protection. Restarting browser (attempt {attempt})...")
                        if attempt < max_retries + 1:
                            await browser.close()
                            await playwright.stop()
                            playwright, browser, context = await launch_stealth_browser()
                            page = await context.new_page()
                            continue
                        else:
                            await log_progress("Max browser restarts reached. Exiting.")
                            await Actor.exit()
                    else:
                        await log_progress(f"Navigation failed: {nav_exc}")
                        await Actor.exit()
            html = await page.content()
            jobs = await parse_job_listings(html)
            await log_progress(f"Found {len(jobs)} jobs on search page.")
            
            # Output search results data (available without cookies)
            for job in jobs:
                await log_progress(f"Scraped job listing: {job.get('jobTitle')}")
                await Actor.push_data(job)
            
            # Attempt to scrape detailed job information (may require cookies)
            await log_progress("Attempting to scrape detailed job information...")
            await log_progress("Note: Detailed job info may require authentication/cookies")
            
            detailed_results = []
            for i, job in enumerate(jobs[:5]):  # Limit to first 5 jobs to avoid rate limiting
                job_link = job.get("jobLink")
                if not job_link:
                    continue
                    
                await log_progress(f"Attempting to access job detail: {job_link}")
                try:
                    await retry_on_failure(page.goto, job_link, wait_until="networkidle")
                    await asyncio.sleep(2)  # Human-like delay
                    job_html = await page.content()
                    
                    # Check if we got redirected to login page
                    if is_login_required(page.url):
                        await log_progress(f"Redirected to login page for job {i+1}. Authentication required for detailed info.")
                        continue
                    
                    job_details = await parse_job_detail(job_html)
                    
                    # Merge search result data with detailed data
                    merged_job = {**job, **job_details}
                    await log_progress(f"Successfully scraped detailed info for: {merged_job.get('jobTitle')}")
                    await Actor.push_data(merged_job)
                    detailed_results.append(merged_job)
                    
                except Exception as e:
                    await log_progress(f"Failed to scrape job detail {i+1}: {str(e)}")
                    # Still output the basic job info we have
                    await Actor.push_data(job)
            
            await log_progress(f"Scraping complete. Total jobs scraped: {len(jobs)}")
            await log_progress(f"Detailed info successfully scraped: {len(detailed_results)}")
            await log_progress("Note: For full detailed scraping, consider using authenticated sessions/cookies")
            
        finally:
            await browser.close()
            await playwright.stop()
