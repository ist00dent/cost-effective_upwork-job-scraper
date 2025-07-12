"""
Navigator for building Upwork search URLs and handling navigation.
"""
from urllib.parse import quote_plus

async def build_search_url(keyword: str, location: str) -> str:
    """
    Constructs a URL-encoded Upwork search URL from keyword and location.
    """
    base_url = "https://www.upwork.com/nx/jobs/search/"
    params = f"?q={quote_plus(keyword)}&location={quote_plus(location)}"
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