#!/usr/bin/python3

# python modules
import collections
import sys

# dwanderson modules
import dwanderson

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TEXTS = dwanderson.texts
PATTERNS = collections.defaultdict(list)
WORDS = set()


##############################################################################
def get_pattern(word):
    word = word.upper()
    letters = collections.defaultdict(list)
    letters.update
    for idx, lett in enumerate(word):
        letters[lett].append(idx)
    first = min([val[0] for val in letters.values() if len(val) > 1] + [100])
    last = max([val[-1] for val in letters.values() if len(val) > 1] + [0])
    if first == 100:
        return ALPHABET[:len(word)] + ":0:0"
    substring = word[first:last + 1]
    pattern = ""
    count = 0
    for idx, lett in enumerate(substring):
        place = substring[:idx].find(lett)
        if place != -1:
            pattern += pattern[place]
        else:
            pattern += ALPHABET[count]
            count += 1
    pattern += ":{}:{}".format(first, len(word) - last - 1)
    return pattern

def readin_dict(word_len=None, words=WORDS, patterns=PATTERNS, texts=TEXTS):
    for fname in texts:
        with open(fname) as fh:
            text = str(fh.read()).replace("\r","").upper()
            word_list = [w for w in text.split("\n") if w.isalpha() and
                                (len(w) == word_len or word_len is None)]
            words.update(word_list)
    for word in words:
        patterns[get_pattern(word)].append(word)
    return words, patterns

def find_words(word, pattern=None, preset=None):
    word = word.upper()
    if pattern is None:
        pattern = get_pattern(word)
    if preset is None:
        preset = collections.defaultdict(lambda:"?")
    answers = set()
    for potential in PATTERNS[pattern]:
        if any(wlett == plett or  ## cant self-map
               preset[wlett] not in ("?", plett) or ## preset is different
               (preset[wlett] == "?" and plett in preset.values())
               for wlett, plett in zip(word, potential)):
            continue
        answers.add(potential)
    return answers

##############################################################################
@dwanderson.time_me
def not_main():
    WORDS, PATTERNS = readin_dict()

@dwanderson.time_me
def main():
    if len(sys.argv) != 2:
        print("USAGE: Provide 1 argument, the word")
        return
    word = sys.argv[1]
    WORDS, PATTERNS = readin_dict(len(word))
    dwanderson.print_list(find_words(word))
    return

if __name__ == '__main__':
    main()
else:
    not_main()
