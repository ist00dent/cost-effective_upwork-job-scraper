"""
Shared helpers for logging, formatting, and retry logic.
"""
import logging
import asyncio

logger = logging.getLogger("upwork_scraper")

async def log_progress(message: str):
    """
    Logs progress for debugging and tracing.
    """
    logger.info(message)

async def retry_on_failure(func, *args, retries=3, delay=2, **kwargs):
    """
    Retry logic for handling failures or bot detection.
    Retries the coroutine up to `retries` times with exponential backoff.
    """
    for attempt in range(1, retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                raise
            await asyncio.sleep(delay * attempt)

async def is_login_required(page_url: str) -> bool:
    """
    Detects if the current page URL indicates login/authentication is required.
    """
    login_indicators = [
        "login",
        "signin",
        "sign-in",
        "auth",
        "authentication",
        "upwork.com/ab/account-security"
    ]

    page_url_lower = page_url.lower()
    return any(indicator in page_url_lower for indicator in login_indicators) 