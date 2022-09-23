# Adding a new language

## Unicode repository

Find out if the language exists in the Unicode repository:
https://github.com/unicode-org/cldr/tree/main/common/annotations

(The data on https://emojiterra.com/ is also sourced from the unicode repository)

If the language exists, open the `{language-code}.xml` file and check if there are actually translations for emoji.
We use the entries that have the attribute `type="tts"` because they only contain one translation, so we don't have to decide which translation to use.
For example for Spanish, we can look at [`es.xml`](https://github.com/unicode-org/cldr/blob/main/common/annotations/es.xml). Let's look at the entries for 😼:

```xml
<annotation cp="😼">cara | gato | gato haciendo una mueca | irónico | sonrisa</annotation>
<annotation cp="😼" type="tts">gato haciendo una mueca</annotation>
```

We use the second one with the `type="tts"`. This would result in the emoji name `:gato_haciendo_una_mueca:`

## Generate EMOJI_DATA

To generate all these names automatically, we use [`utils/get_codes_from_unicode_emoji_data_files.py`](get_codes_from_unicode_emoji_data_files.py)

Open the script and add the two letter code of the language to the dict `languages = {`. For example we can add `es`:

```python
    languages = {
        'es': extract_names(get_language_data_from_url(github_tag, 'es'), 'es')
    }
```

Now we run the script and store the output in `out.py`. The output is a new `EMOJI_DATA` dict

```sh
python utils/get_codes_from_unicode_emoji_data_files.py > out.py
```

Copy the content of `out.py` into the `EMOJI_DATA` dict in [`emoji/unicode_codes/data_dict.py`](../emoji/unicode_codes/data_dict.py) and add `'es'` to `LANGUAGES` variable.

You can also add the new langauge to the `languages` dict in [`utils/gh-pages/generatePages.py`](gh-pages/generatePages.py).

## Test the new `EMOJI_DATA`

The final step is to run the tests to check that everything works as it should:

```sh
pytest

```
