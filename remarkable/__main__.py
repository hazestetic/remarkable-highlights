from remarkable.const import DATA_DIR
from remarkable.document import Document
from remarkable.translator import translate_pl
from remarkable.device import detect_highlight, host_up, sync_documents
from remarkable.highlight import extract_texts_from_highlights
from remarkable.speaker import speak

import click
import time
from termcolor import colored

WAIT_SECONDS = 1

@click.command()
@click.option("--scan", is_flag=True)
@click.option("--update", is_flag=True, help="Update translations dictionary.")
@click.option("--document_id", type=str, default="efad8af2-09c4-4091-bb0b-6259b055c882")
@click.option("--speaker", is_flag=True, help="Speak outlout english words.")
def run(scan: bool, update: bool, document_id: str, speaker: str):

    if speaker:
        while True:
            text = input("Input phrase in english:")
            speak(text)

    if not host_up():
        return

    doc = Document(id=document_id, allowed_colors=[3])

    if scan:
        for _ in detect_highlight(document_id, delay=3):
            sync_documents()

            new_highlights = doc.update_highlights()
            if new_highlights:
                texts = extract_texts_from_highlights(doc.highlights)
                trans = translate_pl(texts[-1])
                print()
                print(f"ENG: {colored(texts[-1], 'yellow')}")
                print(f"PL:  {colored(trans, 'red')}")


    if update:
        # Translate and display all highlights stored
        sync_documents()
        texts = extract_texts_from_highlights(doc.highlights)

        mydictionary = []
        for text in texts:
            trans = translate_pl(text)
            mydictionary.append((text, trans))

        with open(DATA_DIR.joinpath("mydictionary.txt"), mode='w', encoding='utf-8') as f:
            for text, trans in mydictionary:
                print()
                print(f"ENG: {colored(text, 'green')}")
                print(f"PL:  {colored(trans, 'red')}")
                f.write(f"ENG: {text}\nPL:  {trans}\n\n")
    

if __name__ == "__main__":
    run()