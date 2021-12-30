import os
import subprocess
import logging
import time

from remarkable.const import *

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s : %(message)s"
)


def host_up():
    """"""
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-t', '1', '-c', '1', REMARKABLE_IP],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            return True
        except subprocess.CalledProcessError:
            logging.warning("Host is down.")
            return False

def sync_documents():
    if not host_up():
        return

    cmd = f"rsync -a --include='*.metadata' --include='*.json' --include='*/' --exclude='*' root@{REMARKABLE_IP}:{REMARKABLE_DATA_DIR}/* {DOCS_DIR}"
    if os.system(cmd) != 0:
        logging.warning("Could not synchronize documents.")

def chronological_ls(dir: str) -> str:
    """ ls + modification date

        Used for ordering the files (highlights) in modification (chronological) order,
        and detecting whether any new phrases were highlighted.
    """
    return os.popen(f"ssh root@192.168.1.178 ls -lrt {dir}").read()


def detect_highlight(document_id: str, delay: float=3) -> str:
    # Detect any new highlights.
    dir = f"{REMARKABLE_DATA_DIR}/{document_id}.highlights"
    last_order = chronological_ls(dir)
    while True:
        curr_order = chronological_ls(dir)
        if last_order != curr_order:
            yield curr_order
        last_order = curr_order
        time.sleep(delay)





class HighlightMonitor:
    def __init__(self, document_id: str):
        self.dir = f"{REMARKABLE_DATA_DIR}/{self.document_id}.highlights"
        self.last_order = chronological_ls(self.dir)

    def check(self) -> bool:
        """Checks for change in highlights."""
        curr_order = chronological_ls()
        change = self.last_order != curr_order
        self.last_order = curr_order
        return change