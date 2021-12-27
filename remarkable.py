import os
from pathlib import Path
import logging
import json
import paramiko
import re


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s : %(message)s"
)

COLORS = {
    3: "yellow",
    4: "green",
    5: "magenta"
}

HIGHLIGHTS_PATH_LOCAL = Path(__file__).parent.joinpath("data/highlights")
HIGHLIGHTS_FOLDER_NAME = "efad8af2-09c4-4091-bb0b-6259b055c882.highlights"
HIGHLISHTS_PATH_REMOTE = f"/home/root/.local/share/remarkable/xochitl/{HIGHLIGHTS_FOLDER_NAME}"
HOST = "192.168.1.178"

def host_up():
    return True if os.system(f"ping -c 1 {HOST}") == 0 else False

def update_highlights() -> bool:
    """Kopiuje dane zaznaczeń z reMarkable do data/highlights."""
    if host_up():
        os.system(f"rsync -avh root@{HOST}:{HIGHLISHTS_PATH_REMOTE} {HIGHLIGHTS_PATH_LOCAL}")
        # os.system(f"scp -r root@{HOST}:{HIGHLISHTS_PATH_REMOTE} {HIGHLIGHTS_PATH_LOCAL}")
        logging.info("Updated latest highlights from reMarkable 2.")
    else:
        logging.info("Can't update highlights - remote host is down!")
    return host_up


def load_highlights() -> list[dict]:
    """Ładuje zaznaczenia z data/highlights do listy słowników."""
    clean = []
    for filepath in HIGHLIGHTS_PATH_LOCAL.joinpath(HIGHLIGHTS_FOLDER_NAME).iterdir():
        with open(filepath) as file:
            data = json.load(file)["highlights"][0]

        for element in data:
            clean.append({
                "color": COLORS[element["color"]],
                "start": element["start"],
                "length": element["length"],
                "text": element["text"],
                "src": str(filepath.stem)
            })

    return clean

def load_latest_highlight_filename():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    # key = paramiko.RSAKey.from_private_key_file("/Users/marcin/.ssh/id_rsa")
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.178", username="root", password="IiOtM5l4po")
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(
        "ls -lrt .local/share/remarkable/xochitl/efad8af2-09c4-4091-bb0b-6259b055c882.highlights"
    )
    line = ssh_stdout.readlines()[-1]
    filename = line.strip("\n").split(" ")[-1].strip(".json")
    return filename