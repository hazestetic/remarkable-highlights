import gtts
from tempfile import TemporaryDirectory
import os


def speak(text: str, lang="en"):
    # make request to google to get synthesis
    tts = gtts.gTTS(text, lang=lang)

    with TemporaryDirectory() as tempdir:
        filepath = f"{tempdir}/speach.mp3"
        tts.save(filepath)
        os.system(f"afplay {filepath}")


if __name__ == "__main__":
    text = "That's one small step for a man, one giant leap for mankind."
    speak(text)