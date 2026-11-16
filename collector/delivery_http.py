"""Bounded retries for transient delivery failures; retain certificate validation."""
import time
import requests


def request(client, method, url, attempts=4, **kwargs):
    for attempt in range(attempts):
        try:
            response = client.request(method, url, **kwargs)
        except requests.RequestException:
            if attempt == attempts - 1:
                # Do not leak URLs/credentials from requests exception strings.
                raise RuntimeError('delivery network failure after bounded retries') from None
        else:
            limited = response.status_code == 403 and response.headers.get('X-RateLimit-Remaining') == '0'
            if response.status_code not in (408, 429, 500, 502, 503, 504) and not limited:
                return response
            if attempt == attempts - 1:
                return response
        time.sleep(min(2 ** attempt, 8))
    raise AssertionError('unreachable')


def checked_download(client, url, expected_sha256, **kwargs):
    import hashlib
    for attempt in range(3):
        options = dict(kwargs)
        options['params'] = dict(options.get('params') or {}, v=time.time_ns())
        response = request(client, 'GET', url, **options)
        response.raise_for_status()
        if hashlib.sha256(response.content).hexdigest() == expected_sha256:
            return response
        if attempt < 2:
            time.sleep(2 ** attempt)
    raise ValueError('public checksum mismatch after retries')
