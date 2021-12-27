from pathlib import Path
import json
from termcolor import colored
from dataclasses import dataclass

@dataclass
class Highlight:
    

DATA_DIR = Path("highlights/efad8af2-09c4-4091-bb0b-6259b055c882.highlights")

def main():

    # Load json data
    highlights: list[dict] = []
    for file_path in DATA_DIR.iterdir():
        with open(file_path) as file:
            highlights.extend(
                json.load(file)["highlights"][0]
            )

    # Transform list of dicts to pandas dataframe
    df = pd.DataFrame(highlights)
    print(df)


main()
COLORS = {
    3: "yellow",
    4: "green",
    5: "magenta"
}



def display(highlights):
    for h in highlights:
        c = COLORS[h["color"]]
        l = h["length"]
        s = h["start"]
        t = h["text"]
        print(f"{s:<5d} {l:<3d} {colored(t, c)}")
