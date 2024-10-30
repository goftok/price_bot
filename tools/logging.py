import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

main_dir = Path(__file__).resolve().parent.parent
log_file_path = main_dir / "output.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Logger setted up correctly")
