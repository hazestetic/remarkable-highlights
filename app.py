from remarkable import load_latest_highlight_filename, update_highlights, load_highlights
from translator import translate

from termcolor import colored


def main():
    host_up = update_highlights()
    if not host_up:
        return

    highlights = load_highlights()
    filename = load_latest_highlight_filename()

    print(filename)

    latest = [
        h for h in highlights if h["src"] == filename
    ][-1]

    text = latest["text"]
    print(f"\nPhrase:      {colored(text, 'yellow')}")
    # translation = translate(text)
    # print(f"\nTranslation: {colored(translation, 'green')}")


if __name__ == '__main__':
    main()