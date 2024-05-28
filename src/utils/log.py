from logging import getLogger, INFO
import logging.handlers
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os

logger = getLogger(__name__)
logfile = os.path.abspath("ams.log")

tofile = ConcurrentRotatingFileHandler(logfile, "a", 512 * 1024, 5)
tofile.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

toconsole = logging.StreamHandler()
toconsole.setLevel(logging.INFO)
toconsole.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(tofile)
logger.addHandler(toconsole)
logger.setLevel(INFO)
