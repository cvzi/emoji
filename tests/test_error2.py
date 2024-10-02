import sys
from pathlib import Path

try:
    import emoji
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    import emoji


def test_text():  # type:ignore
    # Load all languages
    emoji.emojize('', language='alias')
    for lang_code in emoji.LANGUAGES:
        emoji.emojize('', language=lang_code)

    emoji.config.demojize_keep_zwj = True  # Restore default config value
    emoji.config.replace_emoji_keep_zwj = False # Restore default config value



    text_with_placeholder = """:right-facing_fist::dark_skin_tone:"""

    text_with_unicode = """🤜🏿"""

    print(text_with_placeholder)
    print(text_with_unicode)
    print(emoji.demojize(text_with_unicode))

    assert emoji.demojize(text_with_unicode) == text_with_placeholder




if __name__ == '__main__':

    # Run test_text() multiple times because it relies on a random text
    i = 0
    while i < 10000:
        test_text()
        i += 1
        if i % 10 == 0:
            print(f"Run N° {i}")
