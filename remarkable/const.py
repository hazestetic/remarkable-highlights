from pathlib import Path

REMARKABLE_IP = "192.168.1.178"
REMARKABLE_DATA_DIR = "/home/root/.local/share/remarkable/xochitl"

DATA_DIR = Path(__file__).parent.joinpath("data")
DOCS_DIR = DATA_DIR.joinpath("documents")
CACHE_DIR = DATA_DIR.joinpath("cache")