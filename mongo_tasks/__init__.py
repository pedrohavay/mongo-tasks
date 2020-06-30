LOW = 0
""" Alias constant for low priority task  """

MEDIUM = 1
""" Alias constant for medium priority task  """

HIGH = 2
""" Alias constant for high priority task  """

DESCENDING = -1
""" Alias constant for search descending tasks """

ASCENDING = 1
""" Alias constant for search ascending tasks """

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MONGO-TASKS')
""" Configure logging globally """

from .jobs import Jobs
from .queue import Queue

__version__ = "0.0.1"
