import re
from spellchecker import SpellChecker
checker = SpellChecker()


async def spellcheck(self, message):
    wordlist = re.sub("[^\w\s]", "", message.content).strip().split(" ")
    wordlist = filter(lambda x: len(x) > 0, wordlist)

    misspellings = list(checker.unknown(wordlist))

    fixed = {}
    for m in misspellings:
        corrected = checker.correction(m)
        fixed[m] = corrected

    if len(fixed) > 0:
        amount = len(fixed)
        text = f"Oh no, **{message.author.display_name}**! You misspelled **{amount}** {'word' if amount == 1 else 'words'}. Here are your mistakes:"

        for i, wrong_word in enumerate(fixed):
            text += f"\n    {i + 1}. "
            if wrong_word == fixed[wrong_word]:
                text += f"You said **{wrong_word}**. I didn't find any good corrections for that."
            else:
                text += f"You said **{wrong_word}**. did you mean **{fixed[wrong_word]}** instead?"

        await message.channel.send(text)
