import sys
from typing import Any, Callable, Dict, List, Tuple, Union
if sys.version_info < (3, 9):
    from typing_extensions import Literal  # type: ignore
else:
    from typing import Literal
import random
from pathlib import Path

try:
    import emoji
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    import emoji

def load_all_languages():
    """Load all keys from JSON files into EMOJI_DATA and
    build all language packs (i.e. fill the cache)"""
    emoji.emojize('', language='alias')
    for lang_code in emoji.LANGUAGES:
        emoji.emojize('', language=lang_code)



def test_text(load_all_languages):  # type:ignore
    emoji.config.demojize_keep_zwj = False  # Restore default config value
    emoji.config.replace_emoji_keep_zwj = False  # Restore default config value

    UCS2 = len('Hello 🇫🇷👌') > 9  # don't break up characters on python with UCS-2

    text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat in reprehenderit in cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Stróż pchnął kość w quiz gędźb vel fax myjń.
Høj bly gom vandt fræk sexquiz på wc.
Съешь же ещё этих мягких французских булок, да выпей чаю.
За миг бях в чужд плюшен скърцащ фотьойл.
هلا سكنت بذي ضغثٍ فقد زعموا — شخصت تطلب ظبياً راح مجتازا
שפן אכל קצת גזר בטעם חסה, ודי
ऋषियों को सताने वाले दुष्ट राक्षसों के राजा रावण का सर्वनाश करने वाले विष्णुवतार भगवान श्रीराम, अयोध्या के महाराज दशरथ के बड़े सपुत्र थे।
とりなくこゑす ゆめさませ みよあけわたる ひんかしを そらいろはえて おきつへに ほふねむれゐぬ もやのうち
視野無限廣，窗外有藍天
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

    def default_select(emj_data: Dict[str, Any]) -> str:
        return emj_data['en']

    def add_random_emoji(
        text: str,
        lst: List[Tuple[str, Dict[str, Any]]],
        select: Callable[[Dict[str, Any]], Union[str, Literal[False]]] = default_select,
    ) -> Tuple[str, str, List[str]]:
        emoji_list: List[str] = []
        text_with_unicode = ''
        text_with_placeholder = ''
        for i in range(0, len(text), 10):
            while True:
                emj, emj_data = random.choice(lst)
                placeholder = select(emj_data)
                if placeholder:
                    break

            if UCS2:
                j = text.find(' ', i, i + 10)
                if j == -1:
                    continue
            else:
                j = random.randint(i, i + 10)

            text_with_unicode += text[i:j]
            text_with_unicode += emj
            text_with_unicode += text[j : i + 10]

            text_with_placeholder += text[i:j]
            text_with_placeholder += placeholder
            text_with_placeholder += text[j : i + 10]

            emoji_list.append(emj)

        return text_with_unicode, text_with_placeholder, emoji_list

    def clean(s: str) -> str:
        return s.replace('\u200d', '').replace('\ufe0f', '')

    all_emoji_list = list(emoji.EMOJI_DATA.items())
    qualified_emoji_list = [
        (emj, item)
        for emj, item in emoji.EMOJI_DATA.items()
        if item['status'] == emoji.STATUS['fully_qualified']
    ]

    # qualified emoji
    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(
        text, qualified_emoji_list
    )
    assert emoji.demojize(text_with_unicode) == text_with_placeholder
    assert emoji.emojize(text_with_placeholder) == text_with_unicode
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]

    # qualified emoji from "es"
    def select_es(emj_data: Dict[str, Any]) -> Union[str, Literal[False]]:
        return emj_data['es'] if 'es' in emj_data else False

    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(
        text, qualified_emoji_list, select=select_es
    )
    assert emoji.demojize(text_with_unicode, language='es') == text_with_placeholder
    assert emoji.emojize(text_with_placeholder, language='es') == text_with_unicode
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]

    # qualified emoji from "alias"
    def select_alias(emj_data: Dict[str, Any]) -> Union[str, Literal[False]]:
        return emj_data['alias'][0] if 'alias' in emj_data else False

    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(
        text, qualified_emoji_list, select=select_alias
    )
    assert emoji.demojize(text_with_unicode, language='alias') == text_with_placeholder
    assert emoji.emojize(text_with_placeholder, language='alias') == text_with_unicode
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]

    # all emoji
    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(
        text, all_emoji_list
    )
    assert emoji.demojize(text_with_unicode) == text_with_placeholder
    assert clean(emoji.emojize(text_with_placeholder)) == clean(text_with_unicode)
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]


if __name__ == '__main__':
    load_all_languages()

    # Run test_text() multiple times because it relies on a random text
    i = 0
    while i < 10000:
        test_text(load_all_languages)
        i += 1
        if i % 10 == 0:
            print(f"Run N° {i}")
