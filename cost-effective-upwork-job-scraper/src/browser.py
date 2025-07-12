"""
Stealth Playwright browser launcher for Upwork scraping.

Note: Ensure Playwright is installed in your environment for the import below to work.
"""
from playwright.async_api import async_playwright
import random

USER_AGENTS = [
    # A few common desktop user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

async def launch_stealth_browser():
    """
    Launches a Playwright browser in stealth mode with anti-bot measures.
    Returns the browser and context objects.
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    user_agent = random.choice(USER_AGENTS)
    context = await browser.new_context(
        user_agent=user_agent,
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        java_script_enabled=True,
    )
    # Stealth: block some bot-detectable APIs
    await context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return playwright, browser, context 