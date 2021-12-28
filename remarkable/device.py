import os
import subprocess
import logging

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


class Monitor:
    def __init__(self, document_id: str):
        self.document_id = document_id
        self.last_state = self.last_highlights_modification_state()

    def modification_occured(self) -> bool:
        curr_state = self.last_highlights_modification_state()
        if curr_state == self.last_state:
            return False
        else:
            self.last_state = curr_state
            return True

    def last_highlights_modification_state(self) -> str:
        """Datetime-string of latest update in xochitl (data) directory."""
        return os.popen(f"ssh remarkable ls -lrt {REMARKABLE_DATA_DIR}/{self.document_id}.highlights").read()
