from pathlib import Path

# =============================================================================
# BASE URL
# =============================================================================

BASE_URL = "https://www.impic.pt/impic/ajax/call/impic_api/consultar/ajax/43"

# =============================================================================
# REQUEST SETTINGS
# =============================================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
}

REQUEST_TIMEOUT = 30          # seconds
MAX_RETRIES = 5               # retries for failed requests
RETRY_DELAY = 5               # seconds between retries

# Delay between detail requests.
# Increase if server starts returning HTTP 500.
REQUEST_DELAY = 1.0

# Delay between page requests.
PAGE_DELAY = 0.5

# =============================================================================
# SEARCH FILTERS
# =============================================================================

DISTRICTS = [
    "Porto",
    "Braga",
]

CLASSES = [
    3,
    4,
    5,
    6,
    7,
]

# =============================================================================
# OUTPUT
# =============================================================================

OUTPUT_DIR = Path("output")

OUTPUT_CSV = OUTPUT_DIR / "companies.csv"

CHECKPOINT_CSV = OUTPUT_DIR / "checkpoint.csv"

FAILED_IDS_FILE = OUTPUT_DIR / "failed_ids.txt"

LOG_FILE = OUTPUT_DIR / "scraper.log"

# =============================================================================
# CSV COLUMNS
# =============================================================================

CSV_COLUMNS = [
    "ID",
    "Company Name",
    "Email",
    "District",
    "Class",
]

# =============================================================================
# LOGGING
# =============================================================================

LOG_LEVEL = "INFO"

# =============================================================================
# FEATURES
# =============================================================================

ENABLE_LOGGING = True

ENABLE_CHECKPOINT = True

ENABLE_RETRY = True

ENABLE_PROGRESS = True

ENABLE_FAILED_RETRY = True

# =============================================================================
# CREATE OUTPUT DIRECTORY
# =============================================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)