import os
import json
import re
import logging

from remarkable.const import *
from remarkable.highlight import load_highlights_from_file

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s : %(message)s"
)

class Document:

    def __init__(self, id="efad8af2-09c4-4091-bb0b-6259b055c882", allowed_colors=[3]) -> None:
        self.id = id
        self.allowed_colors = allowed_colors
        self.load_metadata()
        self.highlights = self.load_highlights()

    def load_metadata(self):
        with open(DOCS_DIR.joinpath(f"{self.id}.metadata")) as f:
            self.meta = json.loads(f.read())

    def load_highlights(self):
        highlights = []
        highlights_dir = DOCS_DIR.joinpath(f"{self.id}.highlights")
        # By default highlight files are unordered.
        # To load them in modification-date order, function below is used.
        if filenames := self.filenames_by_modification_date():
            filepaths = [highlights_dir.joinpath(name) for name in filenames]
        else:
            filepaths = [fp for fp in highlights_dir.iterdir()]

        for path in filepaths:
            highlights += load_highlights_from_file(path, self.allowed_colors)
        return highlights

    def update_highlights(self):
        """Updates highlights and returns info if new highlights were found."""
        latest_highlights = self.load_highlights()
        new_highlights = len(latest_highlights) > len(self.highlights)
        self.highlights = latest_highlights
        return new_highlights

    def filenames_by_modification_date(self) -> list[str]:
        """Loads file names in modification-timestamp order."""
        output = os.popen(f"ssh remarkable ls -lrt {REMARKABLE_DATA_DIR}/{self.id}.highlights").read()
        uuid_pattern = re.compile(r"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b")
        return [f"{match}.json" for match in uuid_pattern.findall(output)]