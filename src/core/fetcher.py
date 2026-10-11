"""
High-resilience HTTP fetcher with anti-bot headers and 403 bypass.
Acts as a zero-cost open-source alternative to Firecrawl's scraping endpoint.
"""

import os
import random
import requests
from typing import Optional

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

class SmartFetcher:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()

    def get_headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,sv;q=0.8,da;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"'
        }

    def fetch(self, url: str) -> str:
        """
        Fetches web page HTML. If a local file path is given, reads it directly.
        """
        if os.path.exists(url):
            with open(url, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        try:
            response = self.session.get(
                url,
                headers=self.get_headers(),
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
            return response.text

        except requests.exceptions.HTTPError as e:
            # Attempt fallback with clean headers if 403 or 401
            if response.status_code in [401, 403]:
                print(f"[!] Warning: HTTP {response.status_code} received. Attempting secondary bypass profile...")
                fallback_headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                }
                retry_res = requests.get(url, headers=fallback_headers, timeout=self.timeout)
                if retry_res.status_code == 200:
                    return retry_res.text
            raise e
