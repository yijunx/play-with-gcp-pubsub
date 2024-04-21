from typing import Protocol
import time
from datetime import datetime

class BaseHandler(Protocol):
    def handle(task):
        ...



class SlowHandler(BaseHandler):
    def handle(self, task):
        time.sleep(5)
        print(f"slowly handled at {datetime.now()}")
