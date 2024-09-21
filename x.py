import emoji


print(emoji.__version__)

print(emoji.emojize('Python is :thumbs_up:'))
print(emoji.demojize('Python is 👍'))

print(emoji.emoji_list('♥ ️👍 🦁'))