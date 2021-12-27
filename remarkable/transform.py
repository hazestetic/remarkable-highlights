from remarkable.document import Highlight


def extract_merge_texts(highlights: list[Highlight]) -> list[str]:
    """
        Gdy zaznaczysz 2 linijki oddzielnie, remarkable potraktuje je jako 2 zaznaczenia.
        Ta funkcja łączy takie przypadki w jeden tekst.
    """
    texts = list()
    prolonged_text = ""
    highlight_count = len(highlights)

    for i in range(1, highlight_count):
        prev: Highlight = highlights[i - 1]
        curr: Highlight = highlights[i]
        prev_end = prev.start + prev.length
        distance = curr.start - prev_end

        if distance in [1, 2]:
            # Aktualne wyróznienie jest przedłuzeniem poprzedniego wyróznienia
            if prolonged_text == "":
                prolonged_text = f"{prev.text} {curr.text}"
            else:
                prolonged_text += f" {curr.text}"
        else:
            if prolonged_text != "":
                # Zapisz przedłuony tekst
                text = prolonged_text
                prolonged_text = ""
            else:
                # Zapisz aktualne wyróznienie
                text = prev.text
            
            # Usuń niepotrzebne znaki specjalne
            if text[-1] in ['"', "'", ",", " "]:
                text = text[:-1]

            texts.append(text)

    # Obsługa ostatniego wyróznienia
    if prolonged_text == "":
        texts.append(highlights[-1].text)
    else:
        texts.append(prolonged_text)

    # Deduplicate
    texts = list(dict.fromkeys(texts))

    return texts