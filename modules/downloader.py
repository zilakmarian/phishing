"""Module for downloading data."""
from requests import Session
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RetryError


class DownloadException(Exception):
    pass


def download(url: str):
    """Download data from specified URL."""
    retries = Retry(total=6,
                    backoff_factor=0.7,
                    status_forcelist=[429, 500])
    header = {"User-Agent": "phishtank/app-downloader"}
    with Session() as s:
        s.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            response = s.get(url, headers=header)
            if response.status_code != 200:
                raise DownloadException("Failed to download report")
        except RetryError:
            raise DownloadException("Exceeded retry limit on report download.")

        return response.json()
