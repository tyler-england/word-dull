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
    yesses = []
    for i in range(len(fdlst)):
        remlist = []
        for word in wordlist:
            if fdlst[i] == "y":
                yesses.append(guess[i])
                if word[i] != guess[i]:  # correct location
                    remlist.append(word)
            elif fdlst[i] == "x":
                yesses.append(guess[i])
                if word[i] == guess[i] or word.count(guess[i]) < 1:
                    remlist.append(word)
            elif fdlst[i] == "n":
                if guess[i] in yesses:  # only remove for that letter position
                    if word[i] == guess[i]:
                        remlist.append(word)
                elif word.count(guess[i]) > 0:  # remove for the whole word
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


def organize(words):  # put in optimal guessing order
    outlist = []
    freqlist = []
    wordsadded = []
    toplets = Counter("".join(words)).most_common()
    for i in range(len(toplets)):
        positions = []
        for word in words:  # find most frequent letter placement
            positions.append(word.find(toplets[i][0]))
        toppos = max(positions, key=positions.count)
        for word in words:  # find words with that letter placement
            try:
                if word.find(toplets[i][0]) == toppos and not hasdupes(word):  # correct pos
                    freqlist.append(word)
                    if word not in wordsadded:
                        wordsadded.append(word)
            except:  # that letter isn't in the word
                pass
    for word in words:  # add any that haven't been added
        if not word in wordsadded:
            freqlist.append(word)
    topwords = Counter(freqlist).most_common(20)
    for i in range(len(topwords)):
        outlist.append(topwords[i][0])
    return outlist


def suggest(wordlist, numwords):  # suggests the next input (max. letter usage)
    toplets = Counter("".join(wordlist)).most_common(
        10)  # find top 10 most used letters
    newwords = []
    wordsout = []
    for word in wordlist:
        # has letter, no dupes
        if not hasdupes(word) and word.count(toplets[0][0]) > 0:
            newwords.append(word)
    if len(newwords) < numwords:  # redo, allow duplicates
        for word in wordlist:
            if word.count(toplets[0][0]) > 0:  # has letter
                newwords.append(word)
    i = 1
    if len(newwords) < numwords + 1:
        wordsout = newwords
    else:
        while len(newwords) > numwords:
            wordsout = organize(newwords)
            remlist = []
            try:
                for word in newwords:
                    if word.count(toplets[i][0]) < 1:
                        remlist.append(word)
            except:  # i got too big
                pass
            newwords = [x for x in newwords if x not in remlist]
            i += 1
    newwords = []
    for i in range(numwords):
        try:
            newwords.append(wordsout[i])
        except:  # may not be that many left
            pass
    return ", ".join(newwords)


# Find top initial guess
# all_org = organize(words)
# sugg=[]
# for i in range(3):
#     sugg.append(all_org[i])
# print("\n" + ", ".join(sugg))

seed = input("\nEnter initial word guess: ").lower()
words = pare(words, seed)

i = 1
while i < 6 and len(words) > 1:
    attempt = "more"
    j = -2
    while attempt.lower() == "more":  # if more word suggestions are requested
        j = j + 3
        sugg = suggest(words, min(len(words), j))
        attempt = input(
            "\nEnter next word guess or \"more\" (suggested: " + sugg.upper() + ")\n")
    words = pare(words, attempt)
    i += 1

if len(words) > 0:
    print("\nDone:")
    print(words[0].upper())
else:
    print("No more potential words")
