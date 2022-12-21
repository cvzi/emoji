import os
import sys
include = os.path.relpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, include)
import emoji

print("Translations status:")

counter = {lang: 0 for lang in emoji.LANGUAGES}

for emj, data in emoji.EMOJI_DATA.items():
    for key in data:
        if key in counter:
            counter[key] += 1

complete = max(counter.values())
for lang, count in counter.items():
    print(f"{lang} [{'■' * int(30*count/complete)}{' ' * (30-int(30*count/complete))}] {int(100*count/complete)}%")
