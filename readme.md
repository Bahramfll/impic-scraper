# IMPIC Portugal Company Scraper

A robust Python web scraper for collecting company information from the Portuguese IMPIC public directory.

The scraper is designed for long-running data extraction tasks and includes automatic retry handling, checkpoint recovery, duplicate prevention, and structured CSV export.

---

## Features

- Extracts company information from the IMPIC public directory
- Supports filtering by district and company classification
- Automatic retry mechanism for temporary server errors
- Session-based HTTP requests for improved performance
- Checkpoint recovery to resume interrupted scraping sessions
- Failed ID tracking for later retries
- Duplicate detection
- Clean CSV export
- Modular project architecture
- Configurable scraping parameters

---

## Extracted Data

Each record contains:

- Company Name
- Company ID
- District
- Address
- Postal Code
- City
- Phone Number
- Email
- Website
- Company Classification
- Additional available details

---

## Project Structure

```
impic_scraper/
│
├── src/
│   ├── scraper.py
│   ├── parser.py
│   ├── storage.py
│   ├── config.py
│   └── ...
│
├── output/
│
├── tests/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/impic-scraper.git

cd impic-scraper
```

Create a virtual environment (recommended):

```bash
python -m venv .venv
```

Activate it:

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the scraper:

```bash
python -m src.main
```

Depending on the configuration, the scraper will:

- Fetch company pages
- Parse company details
- Save extracted records
- Track progress
- Resume automatically if interrupted

---

## Configuration

Scraping behavior can be adjusted inside:

```
src/config.py
```

Examples include:

- Request delay
- Retry attempts
- Timeout
- Output location
- District selection
- Classification filters

---

## Error Handling

The scraper is designed to handle unstable network conditions.

Implemented mechanisms include:

- Automatic retries
- HTTP status validation
- Exception handling
- Failed request logging
- Resume after interruption

---

## Checkpoint Recovery

Long scraping jobs can safely resume after interruption.

Progress is periodically saved, allowing the scraper to continue from the last processed record instead of restarting from the beginning.

---

## Output

Scraped data is exported as CSV.

Example:

```
Company Name,Address,City,Phone,Website,...
ABC Company,Lisbon Street 10,Lisbon,+351...,https://...
```

---

## Technologies

- Python 3
- Requests
- BeautifulSoup
- CSV
- HTTP Sessions

---

## Design Principles

The project follows a modular architecture with clear separation of responsibilities.

- Scraper handles HTTP communication
- Parser extracts structured data
- Storage manages persistence
- Configuration is centralized

This design improves readability, maintainability, and future extensibility.

---

## Possible Future Improvements

- Parallel scraping
- SQLite/PostgreSQL storage
- Proxy rotation
- Automatic captcha handling
- Docker support
- Command-line arguments
- JSON export
- Unit tests

---

## Disclaimer

This project was created for educational purposes and legitimate data extraction from publicly accessible information.

Users are responsible for complying with the target website's Terms of Service and applicable laws.

---
