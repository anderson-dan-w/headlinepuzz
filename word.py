#!/usr/bin/python3
import collections
import os
import sys
import json
import string

text_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "texts")
TEXTS = {os.path.join(text_dir, fname) for fname in os.listdir(text_dir)
                if fname.endswith(".dict")}
ALPHABET = string.ascii_uppercase
PATTERNS = collections.defaultdict(list)
WORDS = set()

##############################################################################
class Word(object):
    def __init__(self, string, mapping=None, quick=None):
        self.real_word = string.upper()
        self.word = "".join(l for l in self.real_word if l.isalpha())
        self.pattern = get_pattern(self.word)
        self.mapping = collections.defaultdict(lambda: "?")
        if mapping is not None:
            self.mapping.update(mapping)
        if quick is None:
            self.set_possibles()
    
    def get_plain(self):
        return "".join(self.mapping[l] for l in self.word)

    def update_mapping(self, mapping):
        self.mapping.update(mapping)
        return

    def set_possibles(self, mapping=None):
        if mapping is None:
            mapping = self.mapping
        self.possibles = find_words(self.word, self.pattern, mapping)
        return

    def is_fully_set(self):
        return not "?" in self.get_plain()


##############################################################################
def get_pattern(word):
    word = word.upper()
    letters = collections.defaultdict(list)
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
def save_pattern_file():
    hlpdir = os.path.join(os.getenv("HOME"), ".hlp")
    pattern_fname = os.path.join(hlpdir, "patterns.txt")
    if os.path.exists(pattern_fname):
        return
    if not os.path.exists(hlpdir):
        os.mkdir(hlpdir)
    json.dump(PATTERNS, open(pattern_fname, "w"), indent=4)
    print("done making {}".format(pattern_fname))
    return

def readin_pattern_file(filename=None, patterns=PATTERNS, words=WORDS):
    if filename is None:
        filename = os.path.join(os.getenv("HOME"), ".hlp", "patterns.txt")
    if not os.path.exists(filename):
        print("File doesn't seem to exist")
        return False
    patterns.update(json.load(open(filename)))
    for word_list in patterns.values():
        words.update(word_list)
    return True

def readin_dict(word_len=None, words=WORDS, patterns=PATTERNS, texts=TEXTS):
    for fname in texts:
        with open(fname) as fh:
            text = str(fh.read()).replace("\r","").upper()
            word_list = {w for w in text.split("\n") if w.isalpha() and
                                (len(w) == word_len or word_len is None)}
            words.update(word_list)
    for word in words:
        patterns[get_pattern(word)].append(word)
    if word_len == None:
        save_pattern_file()
    return True

##############################################################################
def not_main():
    readin_pattern_file() or readin_dict()

def main():
    if len(sys.argv) != 2:
        print("USAGE: Provide 1 argument, the word")
        return
    word = sys.argv[1].upper()
    readin_pattern_file() or readin_dict(len(word))
    print(sorted(find_words(word)))
    return

if __name__ == '__main__':
    main()
else:
    not_main()
