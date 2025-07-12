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