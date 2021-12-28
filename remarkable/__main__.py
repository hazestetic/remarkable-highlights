from remarkable.const import DATA_DIR
from remarkable.document import Document
from remarkable.translator import translate
from remarkable.device import Monitor, host_up, sync_documents
from remarkable.highlight import extract_texts_from_highlights

import click
import time
from termcolor import colored

WAIT_SECONDS = 1

@click.command()
@click.option("--scan", is_flag=True)
@click.option("--update", is_flag=True, help="Update translations dictionary.")
def run(scan: bool, update: bool):

    if not host_up():
        return

    monitor = Monitor(document_id="efad8af2-09c4-4091-bb0b-6259b055c882")
    doc = Document(id="efad8af2-09c4-4091-bb0b-6259b055c882", allowed_colors=[3])

    if scan:
        while True:
            if monitor.modification_occured():
                sync_documents()
                new_highlights = doc.update_highlights()
                if new_highlights:
                    texts = extract_texts_from_highlights(doc.highlights)
                    trans = translate(texts[-1])
                    print(f"ENG: {colored(texts[-1], 'green')}")
                    print(f"PL:  {colored(trans, 'red')}")
            time.sleep(WAIT_SECONDS)

    if update:
        sync_documents()
        doc = Document(id="efad8af2-09c4-4091-bb0b-6259b055c882")
        texts = extract_texts_from_highlights(doc.highlights)

        mydictionary = []
        for text in texts:
            trans = translate(text)
            mydictionary.append((text, trans))

        with open(DATA_DIR.joinpath("mydictionary.txt"), mode='w', encoding='utf-8') as f:
            for text, trans in mydictionary:
                print()
                print(f"ENG: {colored(text, 'green')}")
                print(f"PL:  {colored(trans, 'red')}")
                f.write(f"ENG: {text}\nPL:  {trans}\n\n")
    

if __name__ == "__main__":
    run()