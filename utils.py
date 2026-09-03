"""
Helper Utilities & Data Validation Module
Provides common data formatting, validation, file operations, and benchmarking tools.
"""

import os
import re
import json
import time
import platform
import functools
from datetime import datetime
from typing import Any, Dict, Optional, Callable

# ==========================================
# 1. DATA VALIDATION HELPERS
# ==========================================
def validate_email(email: str) -> bool:
    """Validates if a string is a properly formatted email address."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))

def validate_phone(phone: str) -> bool:
    """Validates if a string contains a valid 10-digit or formatted phone number."""
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15

def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
    """Checks if a string matches a specified date format."""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

# ==========================================
# 2. STRING & TEXT FORMATTING
# ==========================================
def slugify(text: str) -> str:
    """Converts string into a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_-]+', '-', text)

def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncates text to maximum length with a suffix if exceeded."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_currency(amount: float, symbol: str = "$", decimals: int = 2) -> str:
    """Formats float number to localized currency representation."""
    return f"{symbol}{amount:,.{decimals}f}"

# ==========================================
# 3. FILE SYSTEM & JSON UTILITIES
# ==========================================
def ensure_directory(path: str) -> str:
    """Ensures a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)
    return path

def read_json_safe(file_path: str, default_value: Any = None) -> Any:
    """Safely reads JSON file, returning default_value on failure or missing file."""
    if not os.path.exists(file_path):
        return default_value
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default_value

def write_json_safe(file_path: str, data: Any, indent: int = 4) -> bool:
    """Safely writes data to a JSON file."""
    try:
        directory = os.path.dirname(file_path)
        if directory:
            ensure_directory(directory)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=str)
        return True
    except OSError:
        return False

# ==========================================
# 4. SYSTEM & DECORATORS
# ==========================================
def measure_execution_time(func: Callable) -> Callable:
    """Decorator to measure and log the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = (end_time - start_time) * 1000
        print(f"[Timer] Function '{func.__name__}' executed in {elapsed:.2f} ms")
        return result
    return wrapper

def get_system_info() -> Dict[str, str]:
    """Returns basic system environment metadata."""
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("=== Testing Utility Functions ===")
    print("Email check (test@example.com) :", validate_email("test@example.com"))
    print("Slugify ('Hello World & Python'):", slugify("Hello World & Python"))
    print("Format Currency (1234567.89)   :", format_currency(1234567.89))
    print("System Metadata                :", get_system_info())
