import os
import json
import re
import logging
from dataclasses import dataclass
from remarkable.const import *

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s : %(message)s"
)

def host_up():
    # Timeout = 1 second
    if os.system(f"ping -t 1 -c 1 {REMARKABLE_IP}") == 0:
        return True
    else:
        logging.warning("Host is down!")
        return False

def sync_documents():
    if not host_up():
        return

    cmd = f"rsync -avh --include='*.metadata' --include='*.json' --include='*/' --exclude='*' root@{REMARKABLE_IP}:{REMARKABLE_DATA_DIR}/* {DOCS_DIR}"
    if os.system(cmd) != 0:
        logging.warning("Could not synchronize documents.")


@dataclass
class Highlight:
    text: str
    color: int
    start: int
    length: int
    src: str


class Document:

    def __init__(self, id="efad8af2-09c4-4091-bb0b-6259b055c882") -> None:
        self.id = id
        self.load_metadata()
        self.load_highlights()

    def load_metadata(self):
        with open(DOCS_DIR.joinpath(f"{self.id}.metadata")) as f:
            self.meta = json.loads(f.read())

    def load_highlights(self):
        self.highlights = []

        highlights_dir = DOCS_DIR.joinpath(f"{self.id}.highlights")
        if filenames := self.filenames_by_modification_date():
            filepaths = [highlights_dir.joinpath(name) for name in filenames]
        else:
            filepaths = [fp for fp in highlights_dir.iterdir()]

        for filepath in filepaths:
            with open(filepath) as f:
                highlights_list: list[dict] = json.load(f)["highlights"][0]

            for highlight in highlights_list:
                self.highlights.append(Highlight(
                    text=highlight.get("text"),
                    color=highlight.get("color"),
                    start=highlight.get("start"),
                    length=highlight.get("length"),
                    src=filepath.name.split('.')[0]
                ))

    def filenames_by_modification_date(self) -> list[str]:
        if not host_up():
            return
        output = os.popen(f"ssh remarkable ls -lrt {REMARKABLE_DATA_DIR}/{self.id}.highlights").read()
        uuid_pattern = re.compile(r"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b")
        return [f"{match}.json" for match in uuid_pattern.findall(output)]

    
    def stats(self):
        print(f"# {self.meta['visibleName']}")
        print(f"Highlight count: {len(self.highlights)}")
        