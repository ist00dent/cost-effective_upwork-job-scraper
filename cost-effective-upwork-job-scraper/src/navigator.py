"""
Navigator for building Upwork search URLs and handling navigation.
"""
from urllib.parse import quote_plus
import random
import asyncio

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
    await page.goto(url, wait_until="networkidle")
    # Human-like random delay
    await asyncio.sleep(random.uniform(2, 4))
    # Simulate human-like mouse movement and scrolling
    width, height = random.randint(1000, 1600), random.randint(700, 1000)
    await page.set_viewport_size({"width": width, "height": height})
    for _ in range(random.randint(3, 6)):
        # Move mouse to a random position
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        await page.mouse.move(x, y, steps=random.randint(5, 20))
        await asyncio.sleep(random.uniform(0.2, 0.7))
        # Scroll a small random amount
        await page.mouse.wheel(0, random.randint(200, 800))
        await asyncio.sleep(random.uniform(0.5, 1.5))
    # Randomly click somewhere (simulate focus/search bar click)
    if random.random() < 0.5:
        await page.mouse.click(random.randint(100, width-100), random.randint(100, height-100))
        await asyncio.sleep(random.uniform(0.5, 1.2)) 