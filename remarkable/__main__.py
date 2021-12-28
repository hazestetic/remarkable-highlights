from remarkable.document import Document, sync_documents
from remarkable.transform import extract_merge_texts
from remarkable.translator import translate

import click
import time
from termcolor import colored

WAIT_SECONDS = 1


@click.command()
@click.option("--scan", is_flag=True)
@click.option("--update", is_flag=True, help="Update translations dictionary.")
def run(scan: bool, update: bool):

    if scan:
        newest_prev = ""
        newest = ""

        while True:
            sync_documents()

            doc = Document()
            texts = extract_merge_texts(doc.highlights)
            
            newest_prev = newest
            newest = texts[-1]
            if newest_prev != newest:
                print()
                translation = translate(newest)
                print()
                print(f"ENG: {colored(newest, 'green')}")
                print(f"PL:  {colored(translation, 'red')}")

            time.sleep(WAIT_SECONDS)
    

if __name__ == "__main__":
    run()