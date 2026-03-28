import csv
from typing import List
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import sys

def get_urls_from_file(file_address: str) -> List[str]:
    links = []

    with open(file_address, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames and "urls" in reader.fieldnames:
            for row in reader:
                url = (row.get("urls") or "").strip()
                if url:
                    links.append(url)

    return links

def exception_classifier(e: Exception) -> str:
    if isinstance(e, requests.exceptions.Timeout):
        return "TIMEOUT"

    elif isinstance(e, requests.exceptions.ConnectionError):
        if "Name or service not known" in str(e) or \
           "Temporary failure in name resolution" in str(e):
            return "DNS_ERROR"
        return "CONNECTION_ERROR"

    elif isinstance(e, requests.exceptions.SSLError):
        return "SSL_ERROR"

    elif isinstance(e, requests.exceptions.TooManyRedirects):
        return "TOO_MANY_REDIRECTS"

    elif isinstance(e, requests.exceptions.InvalidURL):
        return "INVALID_URL"

    elif isinstance(e, requests.exceptions.RequestException):
        return "REQUEST_FAILED"

    return "UNKNOWN_ERROR"


def get_status_code(session: requests.Session, url: str, timeout: int = 10, retries: int = 2) -> str:
    last_error = "UNKNOWN_ERROR"

    for attempt in range(retries):
        try:
            # trying HEAD first as it is faster
            response = session.head(
                url,
                timeout=timeout,
                headers={"User-Agent": "Mozilla/5.0"},
                allow_redirects=True
            )
            return str(response.status_code)

        except requests.exceptions.RequestException:
            try:
                # fall back to GET if HEAD throws exception
                response = session.get(
                    url,
                    timeout=timeout,
                    headers={"User-Agent": "Mozilla/5.0"},
                    allow_redirects=True
                )
                return str(response.status_code)

            except requests.exceptions.RequestException as e:
                error_type = exception_classifier(e)
                last_error = error_type

                # Retrying only for the short-term issues
                if error_type in ["TIMEOUT", "CONNECTION_ERROR", "DNS_ERROR"]:
                    time.sleep(0.5)
                    continue

                return error_type

    return last_error

def obtain_ouput_from_urls(links: List[str], max_workers: int = 5) -> None:
    session = requests.Session()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        output = list(executor.map(lambda u: get_status_code(session, u), links))

    # output
    for url, status_code in zip(links, output):
        print(f"({status_code}) {url}", flush=True)


def main(file_address: str) -> None:
    links = get_urls_from_file(file_address)

    if not links:
        print("No valid URLs found in the CSV file.")
        return

    obtain_ouput_from_urls(links)


if __name__ == "__main__":
    try:
        from google.colab import files

        print("Upload CSV file:")
        file = files.upload()
        file_address = list(file.keys())[0]

    except ImportError:
         if len(sys.argv) > 1:
          file_address=  sys.argv[1]
         else:
           file_address = input("Enter CSV file address: ")

    main(file_address)
