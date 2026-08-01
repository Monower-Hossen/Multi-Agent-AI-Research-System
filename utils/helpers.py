import re
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger("utils.helpers")

def sanitize_text(text: str) -> str:
    """Removes excessive whitespace, control characters, and normalizes spacing."""
    if not text:
        return ""
    # Remove control characters except newlines and tabs
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    # Replace multiple consecutive spaces or tabs with a single space
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    # Normalize multiple newlines to a maximum of two
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    return cleaned.strip()

def format_timestamp() -> str:
    """Returns a formatted UTC timestamp string for reports and logs."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")

def truncate_text(text: str, max_length: int = 1500) -> str:
    """Truncates text to a specified maximum character limit cleanly."""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length] + "\n... [Truncated due to length]"