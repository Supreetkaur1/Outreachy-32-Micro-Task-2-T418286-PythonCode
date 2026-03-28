# Outreachy-32-Micro-Task-2-T418286-PythonCode
[T418286](https://phabricator.wikimedia.org/T418286): Addressing the lusophone technological wishlist proposals - Create a Python script to get and print the `status code` of the response of a list of URLs from a `.csv` file.

##  Overview

This script reads a list of URLs from a CSV file, fetches their HTTP status codes and prints the results in the following format:
A. (STATUS CODE) URL
B. e.g. (200) https://www.nytimes.com/1999/07/04/sports/women-s-world-cup-sissi-of-brazil-has-right-stuff-with-left-foot.html.

It is designed to be:
- Efficient (uses multithreading)
- Robust (handles various network errors)
- User-friendly (clear output)

---

##  Features

- ✅ Reads URLs from a CSV file (`urls` column)
- ✅ Fetches HTTP status codes using `requests`
- ✅ Uses `HEAD` request first for efficiency, falls back to `GET`
- ✅ Retries transient failures (timeouts, connection issues)
- ✅ Classifies errors into meaningful categories:
  - TIMEOUT
  - CONNECTION_ERROR
  - DNS_ERROR
  - SSL_ERROR
  - TOO_MANY_REDIRECTS
  - INVALID_URL
  - REQUEST_FAILED
  - UNKNOWN_ERROR
- ✅ Processes URLs concurrently using threads

---
## Project Structure
```bash
url-status-checker/
│
├── README.md
├── Task2_mycode.py
├── Task 2 - Intern.csv
```
---

##  Input Format

The input CSV must contain a column named:

urls

```bash

### Example:


urls
https://google.com

https://invalid-url

https://github.com
```
The given .csv file has been included in this repository
---

##  How to Run

### ▶️ Local (Terminal)

```bash
python script.py <path_to_csv>
```
Example:
```bash
python script.py data.csv
```
☁️ Google Colab

Run the script
Upload your CSV file when prompted

🖥️ Sample Output
```bash
(200) https://google.com
(404) https://example.com/notfound
(DNS_ERROR) https://invalid-url
```
---
## Design Decisions
1. HEAD → GET fallback
HEAD is attempted first for efficiency
Falls back to GET if the server does not support HEAD
2. Retry mechanism
Retries are applied only for transient errors:
TIMEOUT
CONNECTION_ERROR
DNS_ERROR
3. Error classification
Exceptions are mapped to meaningful categories for better analysis
4. Concurrency
Uses ThreadPoolExecutor to process multiple URLs in parallel
Improves performance for large datasets
---
## Dependencies
Python 3.x
requests

### Install dependencies:

pip install requests



---

If you want next step:
I can help you write a **perfect PR description + cover message** (this often matters more than the
