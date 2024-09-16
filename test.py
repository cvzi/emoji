 
import emoji

assert 'es' not in emoji.EMOJI_DATA[emoji.emojize(':lion:')]


def repl(x, value):
    print(x)
    print(value)
    print(value['es'])



emoji.replace_emoji('🦁', replace=repl)
