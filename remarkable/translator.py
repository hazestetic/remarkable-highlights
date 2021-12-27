import os
import deepl
from diskcache import Cache
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s : %(message)s"
)

def translate(text: str) -> str:
    """
    Tłumaczy podany tekst na język polski, 
    korzystając z cache'a gdy to mozliwe.
    W przeciwnym wypadku tłumeczenie jest pozyskiwane z DeepL API.
    """
    CACHE_DIR = Path(__file__).parent.joinpath("data/cache")
    cache = Cache(CACHE_DIR)
    if text in cache:
        logging.info("Translation loaded from cache.")
        return cache[text]
    else:
        translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
        result = translator.translate_text(text, target_lang="PL")
        cache[text] = result.text
        logging.info("Translation fetched from DeepL API.")
        return result.text

if __name__ == "__main__":
    # res = translate("This is a test text")
    # print(res)
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    usage = translator.get_usage()
    if usage.character.limit_exceeded:
        print("Character limit exceeded.")
    else:
        print(f"Character usage: {usage.character}")


