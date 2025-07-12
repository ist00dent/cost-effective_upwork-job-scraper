"""
Shared helpers for logging, formatting, and retry logic.
"""
import logging

logger = logging.getLogger("upwork_scraper")

async def log_progress(message: str):
    """
    Logs progress for debugging and tracing.
    """
    # TODO: Implement logging logic
    pass

async def retry_on_failure(func, *args, **kwargs):
    """
    Retry logic for handling failures or bot detection.
    """
    # TODO: Implement retry logic
    pass 