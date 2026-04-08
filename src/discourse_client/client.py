"""HTTP client for the Discourse API with auth, rate limiting, and retry."""

import time
from typing import Any

import httpx

DEFAULT_RATE_LIMIT = 12  # Discourse default: 12 requests/sec


class RateLimiter:
    """Simple token-bucket rate limiter."""

    def __init__(self, requests_per_second: float = DEFAULT_RATE_LIMIT):
        self._interval = 1.0 / requests_per_second
        self._last_request = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_request
        if elapsed < self._interval:
            time.sleep(self._interval - elapsed)
        self._last_request = time.monotonic()


class DiscourseClient:
    """Synchronous Discourse API client."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        api_username: str = "system",
        *,
        rate_limit: float = DEFAULT_RATE_LIMIT,
        max_retries: int = 3,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self._rate_limiter = RateLimiter(rate_limit)
        self._max_retries = max_retries
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Api-Key": api_key,
                "Api-Username": api_username,
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> dict | list:
        """Make an API request with rate limiting and retry."""
        last_exc = None
        for attempt in range(self._max_retries):
            self._rate_limiter.wait()
            try:
                resp = self._client.request(method, path, **kwargs)
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    continue
                resp.raise_for_status()
                if resp.status_code == 204:
                    return {}
                return resp.json()
            except httpx.HTTPStatusError:
                raise
            except httpx.HTTPError as exc:
                last_exc = exc
                if attempt < self._max_retries - 1:
                    time.sleep(2**attempt)
        raise last_exc  # type: ignore[misc]

    def get(self, path: str, params: dict | None = None) -> dict | list:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict | None = None) -> dict | list:
        return self._request("POST", path, json=json)

    def put(self, path: str, json: dict | None = None) -> dict | list:
        return self._request("PUT", path, json=json)

    def delete(self, path: str) -> dict | list:
        return self._request("DELETE", path)

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
