import os
import deepl
from diskcache import Cache
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s : %(message)s"
)

def translate_pl(text: str) -> str:
    """
    Translate provided text to polish language.
    Use DeepL API / diskCache.
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
        usage = translator.get_usage()
        logging.info(f"Translation received from DeepL API. [Character usage: {usage.character}]")
        return result.text