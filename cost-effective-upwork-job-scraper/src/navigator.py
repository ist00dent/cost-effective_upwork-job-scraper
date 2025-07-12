"""
Navigator for building Upwork search URLs and handling navigation.
"""
from urllib.parse import quote_plus

async def build_search_url(keyword: str, location: str) -> str:
    """
    Constructs a URL-encoded Upwork search URL from keyword and location.
    The location is double-encoded to match observed Upwork navigation (e.g., United%2520States).
    """
    base_url = "https://www.upwork.com/nx/jobs/search/"
    # Double-encode location as requested
    encoded_location = quote_plus(quote_plus(location))
    params = f"?q={quote_plus(keyword)}&location={encoded_location}"
    return base_url + params

async def navigate_to_search_page(page, url: str):
    """
    Navigates the Playwright page to the given search URL.
    """
    import random, asyncio
    await page.goto(url, wait_until="networkidle")
    # Human-like delay
    await asyncio.sleep(random.uniform(2, 4))
    # Simulate scrolling to load more jobs (infinite scroll)
    for _ in range(random.randint(2, 4)):
        await page.mouse.wheel(0, 2000)
        await asyncio.sleep(random.uniform(1, 2)) 