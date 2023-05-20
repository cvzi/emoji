# -*- coding: UTF-8 -*-


"""
emoji.core
~~~~~~~~~~

Core components for emoji.

"""

import re
from typing import NamedTuple, Union

from emoji import unicode_codes

__all__ = [
    'emojize', 'demojize', 'analyze', 'config',
    'emoji_list', 'distinct_emoji_list', 'emoji_count',
    'replace_emoji', 'is_emoji', 'version',
    'Token', 'EmojiMatch', 'EmojiMatchNonRGI',
]

_SEARCH_TREE = None
_DEFAULT_DELIMITER = ':'


class config():
    """Module-wide configuration"""

    demojize_keep_zwj = True
    """Change the behavior of :func:`emoji.demojize()` regarding
    zero-width-joiners (ZWJ/``\\u200D``) in emoji that are not
    "recommended for general interchange" (non-RGI).
    It has no effect on RGI emoji.

    For example this family emoji with different skin tones "👨‍👩🏿‍👧🏻‍👦🏾" contains four
    person emoji that are joined together by three ZWJ characters:
    ``👨\\u200D👩🏿\\u200D👧🏻\\u200D👦🏾``

    If ``True``, the zero-width-joiners will be kept and :func:`emoji.emojize()` can
    reverse the :func:`emoji.demojize()` operation:
    ``emoji.emojize(emoji.demojize(s)) == s``

    The example emoji would be converted to
    ``:man:\\u200d:woman_dark_skin_tone:\\u200d:girl_light_skin_tone:\\u200d:boy_medium-dark_skin_tone:``

    If ``False``, the zero-width-joiners will be removed and :func:`emoji.emojize()`
    can only reverse the individual emoji: ``emoji.emojize(emoji.demojize(s)) != s``

    The example emoji would be converted to
    ``:man::woman_dark_skin_tone::girl_light_skin_tone::boy_medium-dark_skin_tone:``
    """

    replace_emoji_keep_zwj = False
    """Change the behavior of :func:`emoji.replace_emoji()` regarding
    zero-width-joiners (ZWJ/``\\u200D``) in emoji that are not
    "recommended for general interchange" (non-RGI).
    It has no effect on RGI emoji.

    See :attr:`config.demojize_keep_zwj` for more information.
    """


def emojize(
        string,
        delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER),
        variant=None,
        language='en',
        version=None,
        handle_version=None
):
    """
    Replace emoji names in a string with unicode codes.
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbsup:", language='alias'))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun {thumbs_up}", delimiters = ("{", "}")))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :red_heart:", variant="text_type"))
        Python is fun ❤
        >>> print(emoji.emojize("Python is fun :red_heart:", variant="emoji_type"))
        Python is fun ❤️ # red heart, not black heart

    :param string: String contains emoji names.
    :param delimiters: (optional) Use delimiters other than _DEFAULT_DELIMITER. Each delimiter
        should contain at least one character that is not part of a-zA-Z0-9 and ``_-–&.’”“()!?#*+,/\\``
    :param variant: (optional) Choose variation selector between "base"(None), VS-15 ("text_type") and VS-16 ("emoji_type")
    :param language: Choose language of emoji name: language code 'es', 'de', etc. or 'alias'
        to use English aliases
    :param version: (optional) Max version. If set to an Emoji Version,
        all emoji above this version will be ignored.
    :param handle_version: (optional) Replace the emoji above ``version``
        instead of ignoring it. handle_version can be either a string or a
        callable; If it is a callable, it's passed the unicode emoji and the
        data dict from emoji.EMOJI_DATA and must return a replacement string
        to be used::

            handle_version(u'\\U0001F6EB', {
                'en' : ':airplane_departure:',
                'status' : fully_qualified,
                'E' : 1,
                'alias' : [u':flight_departure:'],
                'de': u':abflug:',
                'es': u':avión_despegando:',
                ...
            })

    :raises ValueError: if ``variant`` is neither None, 'text_type' or 'emoji_type'

    """

    if language == 'alias':
        language_pack = unicode_codes.get_aliases_unicode_dict()
    else:
        language_pack = unicode_codes.get_emoji_unicode_dict(language)

    pattern = re.compile(u'(%s[\\w\\-&.’”“()!#*+?–,/]+%s)' %
                         (re.escape(delimiters[0]), re.escape(delimiters[1])), flags=re.UNICODE)

    def replace(match):
        mg = match.group(1)[len(delimiters[0]):-len(delimiters[1])]
        emj = language_pack.get(_DEFAULT_DELIMITER + mg + _DEFAULT_DELIMITER)
        if emj is None:
            return match.group(1)

        if version is not None and unicode_codes.EMOJI_DATA[emj]['E'] > version:
            if callable(handle_version):
                emj_data = unicode_codes.EMOJI_DATA[emj].copy()
                emj_data['match_start'] = match.start()
                emj_data['match_end'] = match.end()
                return handle_version(emj, emj_data)

            elif handle_version is not None:
                return str(handle_version)
            else:
                return ''

        if variant is None or 'variant' not in unicode_codes.EMOJI_DATA[emj]:
            return emj

        if emj[-1] == u'\uFE0E' or emj[-1] == u'\uFE0F':
            # Remove an existing variant
            emj = emj[0:-1]
        if variant == "text_type":
            return emj + u'\uFE0E'
        elif variant == "emoji_type":
            return emj + u'\uFE0F'
        else:
            raise ValueError(
                "Parameter 'variant' must be either None, 'text_type' or 'emoji_type'")

    return pattern.sub(replace, string)


class EmojiMatch:
    """
    Represents a match of a "recommended for general interchange" (RGI)
    emoji in a string.
    """

    __slots__ = ('emoji', 'start', 'end', 'data')

    def __init__(self, emoji: str, start: int, end: int, data: Union[dict, None]):
        self.emoji = emoji
        self.start = start
        self.end = end
        self.data = data

    def emoji_data_copy(self):
        if self.data:
            emj_data = self.data.copy()
            emj_data['match_start'] = self.start
            emj_data['match_end'] = self.end
            return emj_data
        else:
            return {
                'match_start': self.start,
                'match_end': self.end
                }

    def __repr__(self):
        return f'EmojiMatch({self.emoji}, {self.start}, {self.end})'


class EmojiMatchNonRGI(EmojiMatch):
    """
    Represents a match of multiple emoji in a string that are joined by
    zero-width-joiners (ZWJ/``\\u200D``). This class is only used for emoji
    that are not "recommended for general interchange" (non-RGI) by Unicode.org.
    RGI emoji are always represented by the base :class:`EmojiMatch`.
    """
    __slots__ = ('emojis',)

    def __init__(self, first_emoji_match: EmojiMatch, second_emoji_match: EmojiMatch):
        self.emojis = [first_emoji_match, second_emoji_match]
        self._update()

    def _update(self):
        self.emoji = "\u200D".join(e.emoji for e in self.emojis)
        self.start = self.emojis[0].start
        self.end = self.emojis[-1].end
        self.data = None

    def _add(self, next_emoji_match: EmojiMatch):
        self.emojis.append(next_emoji_match)
        self._update()

    def __repr__(self):
        e = "\u200D".join(e.emoji for e in self.emojis)
        return f'EmojiMatchNonRGI({e}({"-".join(e.emoji for e in self.emojis)}), {self.start}, {self.end})'


class Token(NamedTuple):
    """
    A named tuple containing the matched string and its EmojiMatch object if it is an emoji
    or a single character that is not a unicode emoji.
    """
    chars: str
    value: Union[str, EmojiMatch]


def _analyze(string, keep_zwj):
    """
    Finds unicode emoji in a string. Yields all normal characters as a named
    tuple ``Token(char, char)`` and all emoji as ``Token(chars, EmojiMatch)``.

    :param string: String contains unicode characters. MUST BE UNICODE.
    :param keep_zwj: Should ZWJ-characters (``\\u200D``) that join non-RGI emoji be
        skipped or should the be yielded as normal characters
    :return: An iterable of tuples Token(char, char) or Token(chars, EmojiMatch)
    """

    tree = _get_search_tree()
    result = [] # [ Token(oldsubstring0, EmojiMatch), Token(oldsubstring1, oldsubstring1), ... ]
    i = 0
    length = len(string)
    ignore = []  # index of chars in string that are skipped, i.e. the ZWJ-char in non-RGI-ZWJ-sequences
    while i < length:
        consumed = False
        char = string[i]
        if i in ignore:
            i += 1
            if char == '\u200d' and keep_zwj:
                result.append(Token(char, char))
            continue

        elif char in tree:
            j = i + 1
            sub_tree = tree[char]
            while j < length and string[j] in sub_tree:
                if j in ignore:
                    break
                sub_tree = sub_tree[string[j]]
                j += 1
            if 'data' in sub_tree:
                emj_data = sub_tree['data']
                code_points = string[i:j]

                # We cannot yield the result here, we need to defer
                # the call until we are sure that the emoji is finished
                # i.e. we're not inside an ongoing ZWJ-sequence
                match_obj = EmojiMatch(code_points, i, j, emj_data)

                i = j - 1
                consumed = True
                result.append(Token(code_points, match_obj))

        elif char == '\u200d' and result[-1].chars in unicode_codes.EMOJI_DATA and string[i - 1] in tree:
            # the current char is ZWJ and the last match was an emoji
            ignore.append(i)
            if unicode_codes.EMOJI_DATA[result[-1].chars]["status"] == unicode_codes.STATUS["component"]:
                # last match was a component, it could be ZWJ+EMOJI+COMPONENT
                # or ZWJ+COMPONENT
                i = i - sum(len(t.chars) for t in result[-2:])
                if string[i] == '\u200d':
                    # It's ZWJ+COMPONENT, move one back
                    i += 1
                    del result[-1]
                else:
                    # It's ZWJ+EMOJI+COMPONENT, move two back
                    del result[-2:]
            else:
                # last match result[-1] was a normal emoji, move cursor
                # before the emoji
                i = i - len(result[-1].chars)
                del result[-1]
            continue

        elif result:
            yield from result
            result = []

        if not consumed and char != u'\ufe0e' and char != u'\ufe0f':
            result.append(Token(char, char))
        i += 1

    yield from result


def _filter_emoji_matches(matches, only_emoji, join_emoji):
    """
    Filters the output of `_analyze()`

    :param matches: An iterable of tuples of the form ``(match_str, result)``
        where ``result`` is either an EmojiMatch or a string.
    :param only_emoji: If True, only EmojiMatch are returned in the output.
        If False all characters are returned
    :param combine_nonrgi_emoji: If True, multiple EmojiMatch are merged into
        a single EmojiMatchNonRGI if they are separated only by a ZWJ.

    :return: An iterable of tuples Token(char, char), Token(chars, EmojiMatch) or Token(chars, EmojiMatchNonRGI)
    """

    if not join_emoji and not only_emoji:
        return matches

    if not join_emoji:
        return (token for token in matches if token.chars != '\u200d')

    # Combine EmojiMatch that are separated by a ZWJ into a single EmojiMatchNonRGI
    previous_is_emoji = False
    previous_is_zwj = False
    pre_previous_is_emoji = False
    accumulator = []
    for token in matches:
        pre_previous_is_emoji = previous_is_emoji
        if previous_is_emoji and token.value == '\u200d':
            previous_is_zwj = True
        elif isinstance(token.value, EmojiMatch):
            if pre_previous_is_emoji and previous_is_zwj:
                if isinstance(accumulator[-1].value, EmojiMatchNonRGI):
                    accumulator[-1].value._add(token.value)
                    accumulator[-1] = Token(accumulator[-1].chars + '\u200d' + token.chars, accumulator[-1].value)
                else:
                    accumulator.append(Token(token.chars, EmojiMatchNonRGI(accumulator.pop().value, token.value)))
            else:
                accumulator.append(token)
            previous_is_emoji = True
            previous_is_zwj = False
        else:
            # Other character, not an emoji
            previous_is_emoji = False
            previous_is_zwj = False
            yield from accumulator
            if not only_emoji:
                yield token
            accumulator = []
    yield from accumulator


def analyze(string, only_emoji=True, join_emoji=True):
    """
    Find unicode emoji in a string. Yield each emoji as a named tuple
    ``Token(chars, EmojiMatch)`` or ``Token(chars, EmojiMatchNonRGI)``.
    All other characters as ``Token(char, char)`` if ``only_emoji`` is False.

    :param string: String to analyze
    :param only_emoji: If False also yield all non-emoji characters as Token(char, char)
    :param join_emoji: If True, multiple EmojiMatch are merged into a single
        EmojiMatchNonRGI if they are separated only by a ZWJ.
    """
    return _filter_emoji_matches(
        _analyze(string, keep_zwj=True), only_emoji=only_emoji, join_emoji=join_emoji)


def demojize(
        string,
        delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER),
        language='en',
        version=None,
        handle_version=None
):
    """
    Replace unicode emoji in a string with emoji shortcodes. Useful for storage.
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.demojize(u"Python is fun 👍"))
        Python is fun :thumbs_up:
        >>> print(emoji.demojize(u"Unicode is tricky 😯", delimiters=("__", "__")))
        Unicode is tricky __hushed_face__

    :param string: String contains unicode characters. MUST BE UNICODE.
    :param delimiters: (optional) User delimiters other than ``_DEFAULT_DELIMITER``
    :param language: Choose language of emoji name: language code 'es', 'de', etc. or 'alias'
        to use English aliases
    :param version: (optional) Max version. If set to an Emoji Version,
        all emoji above this version will be removed.
    :param handle_version: (optional) Replace the emoji above ``version``
        instead of removing it. handle_version can be either a string or a
        callable ``handle_version(emj: str, data: dict) -> str``; If it is
        a callable, it's passed the unicode emoji and the data dict from
        emoji.EMOJI_DATA and must return a replacement string  to be used.
        The passed data is in the form of::

            handle_version(u'\\U0001F6EB', {
                'en' : ':airplane_departure:',
                'status' : fully_qualified,
                'E' : 1,
                'alias' : [u':flight_departure:'],
                'de': u':abflug:',
                'es': u':avión_despegando:',
                ...
            })

    """

    if language == 'alias':
        language = 'en'
        _use_aliases = True
    else:
        _use_aliases = False

    def handle(emoji_match):
        if version is not None and emoji_match.data['E'] > version:
            if callable(handle_version):
                return handle_version(emoji_match.emoji, emoji_match.emoji_data_copy())
            elif handle_version is not None:
                return handle_version
            else:
                return None
        elif language in emoji_match.data:
            if _use_aliases and 'alias' in emoji_match.data:
                return delimiters[0] + emoji_match.data['alias'][0][1:-1] + delimiters[1]
            else:
                return delimiters[0] + emoji_match.data[language][1:-1] + delimiters[1]
        else:
            # The emoji exists, but it is not translated, so we keep the emoji
            return emoji_match.emoji

    matches = _analyze(string, keep_zwj=config.demojize_keep_zwj)
    return "".join(str(handle(token.value)) if isinstance(
        token.value, EmojiMatch) else token.value for token in matches)


def replace_emoji(string, replace='', version=-1):
    """
    Replace unicode emoji in a customizable string.

    :param string: String contains unicode characters. MUST BE UNICODE.
    :param replace: (optional) replace can be either a string or a callable;
        If it is a callable, it's passed the unicode emoji and the data dict from
        emoji.EMOJI_DATA and must return a replacement string to be used.
        replace(str, dict) -> str
    :param version: (optional) Max version. If set to an Emoji Version,
        only emoji above this version will be replaced.
    """

    def handle(emoji_match):
        if version > -1:
            if emoji_match.data['E'] > version:
                if callable(replace):
                    return replace(emoji_match.emoji, emoji_match.emoji_data_copy())
                else:
                    return str(replace)
        elif callable(replace):
            return replace(emoji_match.emoji, emoji_match.emoji_data_copy())
        elif replace is not None:
            return replace
        return emoji_match.emoji

    matches = _analyze(string, keep_zwj=config.replace_emoji_keep_zwj)
    if config.replace_emoji_keep_zwj:
        matches = _filter_emoji_matches(matches, only_emoji=False, join_emoji=True)
    return "".join(str(handle(m.value)) if isinstance(m.value, EmojiMatch) else m.value for m in matches)


def emoji_list(string):
    """
    Returns the location and emoji in list of dict format.
        >>> emoji.emoji_list("Hi, I am fine. 😁")
        [{'match_start': 15, 'match_end': 16, 'emoji': '😁'}]
    """

    return [{
        'match_start': m.value.start,
        'match_end': m.value.end,
        'emoji': m.value.emoji,
    } for m in _analyze(string, keep_zwj=False) if isinstance(m.value, EmojiMatch)]


def distinct_emoji_list(string):
    """Returns distinct list of emojis from the string."""
    distinct_list = list(
        {e['emoji'] for e in emoji_list(string)}
    )
    return distinct_list


def emoji_count(string, unique=False):
    """
    Returns the count of emojis in a string.

    :param unique: (optional) True if count only unique emojis
    """
    if unique:
        return len(distinct_emoji_list(string))
    return len(emoji_list(string))


def is_emoji(string):
    """Returns True if the string is an emoji and it is "recommended for
    general interchange" by Unicode.org."""
    return string in unicode_codes.EMOJI_DATA


def version(string):
    """
    Returns the Emoji Version of the emoji.

    See http://www.unicode.org/reports/tr51/#Versioning for more information.
        >>> emoji.version("😁")
        0.6
        >>> emoji.version(":butterfly:")
        3

    :param string: An emoji or a text containing an emoji
    :raises ValueError: if ``string`` does not contain an emoji
    """
    # Try dictionary lookup
    if string in unicode_codes.EMOJI_DATA:
        return unicode_codes.EMOJI_DATA[string]['E']

    language_pack = unicode_codes.get_emoji_unicode_dict('en')
    if string in language_pack:
        emj_code = language_pack[string]
        if emj_code in unicode_codes.EMOJI_DATA:
            return unicode_codes.EMOJI_DATA[emj_code]['E']

    # Try to find first emoji in string
    version = []

    def f(e, emoji_data):
        version.append(emoji_data['E'])
        return ''
    replace_emoji(string, replace=f, version=-1)
    if version:
        return version[0]
    emojize(string, language='alias', version=-1, handle_version=f)
    if version:
        return version[0]
    for lang_code in unicode_codes._EMOJI_UNICODE:
        emojize(string, language=lang_code, version=-1, handle_version=f)
        if version:
            return version[0]

    raise ValueError("No emoji found in string")


def _get_search_tree():
    """
    Generate a search tree for demojize().
    Example of a search tree::

        EMOJI_DATA =
        {'a': {'en': ':Apple:'},
        'b': {'en': ':Bus:'},
        'ba': {'en': ':Bat:'},
        'band': {'en': ':Beatles:'},
        'bandit': {'en': ':Outlaw:'},
        'bank': {'en': ':BankOfEngland:'},
        'bb': {'en': ':BB-gun:'},
        'c': {'en': ':Car:'}}

        _SEARCH_TREE =
        {'a': {'data': {'en': ':Apple:'}},
        'b': {'a': {'data': {'en': ':Bat:'},
                    'n': {'d': {'data': {'en': ':Beatles:'},
                                'i': {'t': {'data': {'en': ':Outlaw:'}}}},
                        'k': {'data': {'en': ':BankOfEngland:'}}}},
            'b': {'data': {'en': ':BB-gun:'}},
            'data': {'en': ':Bus:'}},
        'c': {'data': {'en': ':Car:'}}}

                   _SEARCH_TREE
                 /     |        ⧵
               /       |          ⧵
            a          b             c
            |        / |  ⧵          |
            |       /  |    ⧵        |
        :Apple:   ba  :Bus:  bb     :Car:
                 /  ⧵         |
                /    ⧵        |
              :Bat:    ban     :BB-gun:
                     /     ⧵
                    /       ⧵
                 band       bank
                /   ⧵         |
               /     ⧵        |
            bandi :Beatles:  :BankOfEngland:
               |
            bandit
               |
           :Outlaw:


    """
    global _SEARCH_TREE
    if _SEARCH_TREE is None:
        _SEARCH_TREE = {}
        for emj in unicode_codes.EMOJI_DATA:
            sub_tree = _SEARCH_TREE
            lastidx = len(emj) - 1
            for i, char in enumerate(emj):
                if char not in sub_tree:
                    sub_tree[char] = {}
                sub_tree = sub_tree[char]
                if i == lastidx:
                    sub_tree['data'] = unicode_codes.EMOJI_DATA[emj]
    return _SEARCH_TREE
