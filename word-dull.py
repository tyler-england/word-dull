from collections import Counter
from pathlib import Path

path = str(Path(__file__).parents[0])
pathdoc = path + "/words.txt"

with open(pathdoc) as wordfile:
    wordsall = [line.rstrip() for line in wordfile]

let_cnt = 5

words = list({word.lower() for word in wordsall if let_cnt == len(word)})


def pare(wordlist, guess):  # gets info about letters & pares down list
    lets = [let for let in guess]
    wrd = ""
    for let in lets:
        wrd = wrd + "  " + let.upper()
    print("\nEnter the following for each letter in the word, separated by commas")
    print("Y - the letter is at the correct location in the word")
    print("N - the letter does not appear in the word")
    print("X - the letter is in the word, but not at that location")
    feedback = input(wrd.strip() + "\n").lower()
    fdlst = [x.strip() for x in feedback.split(",")]
    for i in range(len(fdlst)):
        remlist = []
        for word in wordlist:
            if fdlst[i] == "y":
                if word[i] != guess[i]:  # correct location
                    remlist.append(word)
            elif fdlst[i] == "x":
                if word[i] == guess[i] or word.find(guess[i]) < 0:
                    remlist.append(word)
            elif fdlst[i] == "n":
                if word.find(guess[i]) > -1:
                    remlist.append(word)
        if len(remlist) > 0:
            remlist = list(set(remlist))
            wordlist = [x for x in wordlist if x not in remlist]
    return wordlist


def hasdupes(wrd_input):
    byesno = False
    lst = []
    lst.extend(wrd_input)
    lst = list(set(lst))
    if len(lst) < len(wrd_input):
        byesno = True
    return byesno


def suggest(wordlist, numwords):  # suggests the next input (max. letter usage?)
    toplets = Counter("".join(wordlist)).most_common(
        10)  # find top 10 most used letters
    newwords = []
    wordsout = []
    for word in wordlist:
        # has letter, no dupes
        if not hasdupes(word) and word.find(toplets[0][0]) > -1:
            newwords.append(word)
    if len(newwords) < numwords:  # redo, allow dupes
        for word in wordlist:
            if word.find(toplets[0][0]) > -1:  # has letter
                newwords.append(word)
    i = 1
    if len(newwords) < numwords + 1:
        wordsout = newwords
    else:
        while len(newwords) > numwords - 1 and i < 10:
            wordsout = newwords
            remlist = []
            for word in newwords:
                if word.find(toplets[i][0]) < 0:
                    remlist.append(word)
            newwords = [x for x in newwords if x not in remlist]
            i += 1
    newwords = []
    for i in range(numwords):
        try:
            newwords.append(wordsout[i])
        except:  # may not be that many left
            pass
    return ", ".join(newwords)


sugg = suggest(words, 3)
print("\n" + sugg)

seed = input("\nEnter initial word guess: ").lower()
words = pare(words, seed)

i = 1
while i < 6 and len(words) > 1:
    attempt = "more"
    j = -2
    while attempt.lower() == "more":  # if more word suggestions are requested
        j = j + 3
        sugg = suggest(words, j)
        attempt = input(
            "\nEnter next word guess or \"more\" (suggested: " + sugg.upper() + ")\n")
    words = pare(words, attempt)
    i += 1

if len(words) > 0:
    print("\nDone:")
    print(words[0])
else:
    print("No more potential words")
