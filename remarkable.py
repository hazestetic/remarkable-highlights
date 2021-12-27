import os
from pathlib import Path
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s : %(message)s"
)

HIGHLIGHTS_PATH_LOCAL = Path(__file__).parent.joinpath("data/highlights")
HIGHLIGHTS_FOLDER_NAME = "efad8af2-09c4-4091-bb0b-6259b055c882.highlights"
HIGHLISHTS_PATH_REMOTE = f"/home/root/.local/share/remarkable/xochitl/{HIGHLIGHTS_FOLDER_NAME}"
HOST = "192.168.1.178"


def update_highlights() -> bool:
    """Kopiuje dane zaznaczeń z reMarkable do data/highlights."""
    host_up = True if os.system(f"ping -c 1 {HOST}") == 0 else False
    if host_up:
        os.system(f"scp -r root@{HOST}:{HIGHLISHTS_PATH_REMOTE} {HIGHLIGHTS_PATH_LOCAL}")
        logging.info("Updated latest highlights from reMarkable 2.")
    else:
        logging.info("Can't update highlights - remote host is down!")
    return host_up


def load_highlights() -> list[dict]:
    """Ładuje zaznaczenia z data/highlights do listy słowników."""
    highlights = []
    for file_path in HIGHLIGHTS_PATH_LOCAL.joinpath(HIGHLIGHTS_FOLDER_NAME).iterdir():
        with open(file_path) as file:
            highlights.extend(
                json.load(file)["highlights"][0]
            )
    return highlights
