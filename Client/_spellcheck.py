import re
from spellchecker import SpellChecker
checker = SpellChecker()

async def spellcheck(self, message):
    wordlist = re.sub("[^\w\s]", "", message.content).strip().split(" ")
    wordlist = filter(lambda x: len(x) > 0, wordlist)

    misspellings = list(checker.unknown(wordlist))

    if misspellings:
        amount = len(misspellings)
        text = f"Oh no, **{message.author.display_name}**! You misspelled **{amount}** {'word' if amount == 1 else 'words'}. Here are your mistakes:"

        print(misspellings)

        for i in range(amount):
            if not misspellings[i]:
                continue

            text += "\n"
            text += f"    {i + 1}. You said **{misspellings[i]}**; did you mean **{checker.correction(misspellings[i])}** instead?"

        await message.channel.send(text)