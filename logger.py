import logging
from settings import BASE_DIR

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "clipstack.log"
logger = logging.getLogger("clipstack")
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# File handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)
