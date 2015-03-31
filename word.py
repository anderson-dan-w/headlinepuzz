#!/usr/bin/python3
import collections
import os
import sys
import json
import string

text_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "texts")
TEXTS = {os.path.join(text_dir, fname) for fname in os.listdir(text_dir)
                if fname.endswith(".dict")}

class PatternMapper():
    ALPHABET = string.ascii_uppercase
    DIT = "?"

    def __init__(self, pattern_fname=None, dict_fnames=None):
        self.patterns = collections.defaultdict(set)
        self.words = set()
        self.readin_pattern_file(pattern_fname) or self.readin_dict(dict_fnames)

    def get_pattern(self, word):
        first, last = None, None
        lenword = len(word)
        for idx, letter in enumerate(word):
            if word.count(letter) > 1:
                first = idx
                break
        if first is None:
            return self.ALPHABET[:len(word)] + ":0:0"
        for idx, letter in enumerate(reversed(word), 1):
            if word.count(letter) > 1:
                last = lenword - idx
                break

        substring = word[first:last + 1]
        alphabet_iter = iter(self.ALPHABET)
        mapper = collections.defaultdict(lambda: next(alphabet_iter))
        pattern = "".join(mapper[letter] for letter in substring)
        return pattern + ":{}:{}".format(first, lenword - last - 1)
    
    def find_words(self, word, pattern=None, mapping=None):
        if pattern is None:
            pattern = self.get_pattern(word)
        preset = collections.defaultdict(lambda:self.DIT)
        if mapping is not None:
            preset.update(mapping)
        preset_values = set(preset.values())
        answers = set()
        for potential in self.patterns[pattern]:
            if any(wlett == plett or preset[wlett] not in (self.DIT, plett) or
                   (preset[wlett] == self.DIT and plett in preset_values)
                   for wlett, plett in zip(word, potential)):
                continue
            answers.add(potential)
        return answers

    ##########################################################################
    def save_pattern_file(self):
        hlpdir = os.path.join(os.getenv("HOME"), ".hlp")
        pattern_fname = os.path.join(hlpdir, "patterns.txt")
        if os.path.exists(pattern_fname):
            return
        if not os.path.exists(hlpdir):
            os.mkdir(hlpdir)
        json.dump(self.patterns, open(pattern_fname, "w"), indent=4)
        print("done writing {}".format(pattern_fname))
        return

    def readin_pattern_file(self, filename=None):
        if filename is None:
            filename = os.path.join(os.getenv("HOME"), ".hlp", "patterns.txt")
        if not os.path.exists(filename):
            print("{} doesn't seem to exist".format(filename))
            return False
        self.patterns.update(json.load(open(filename)))
        for word_list in self.patterns.values():
            self.words.update(word_list)
        return True

    def readin_dict(self, word_len=None, dict_fnames=None):
        if dict_fnames is None:
            dict_fnames = TEXTS
        for fname in dict_fnames:
            with open(fname) as fh:
                text = str(fh.read()).replace("\r","").upper()
                word_list = {w for w in text.split("\n") if w.isalpha() and
                                    (len(w) == word_len or word_len is None)}
                self.words.update(word_list)
        for word in self.words:
            self.patterns[get_pattern(word)].append(word)
        if word_len == None:
            self.save_pattern_file()
        return True
## want a singleton-esque pattern-mapper
PATTERN_MAPPER = PatternMapper()

##############################################################################
class Word(object):
    PATTERN_MAPPER = PATTERN_MAPPER
    DIT = PATTERN_MAPPER.DIT

    def __init__(self, letters, mapping=None, quick=None):
        self.original_word = letters.upper()
        self.word = "".join(l for l in self.original_word if l.isalpha())
        self.pattern = self.PATTERN_MAPPER.get_pattern(self.word)
        self.mapping = mapping
        if self.mapping is None:
            self.mapping = collections.defaultdict(lambda: self.DIT)

    @property
    def plain(self):
        return "".join(self.mapping[l] for l in self.word)

    @plain.setter
    def plain(self, plainword):
        self.mapping.update(dict(zip(self.word, plainword)))

    @property
    def possibles(self):
        return self.PATTERN_MAPPER.find_words(self.word, self.pattern,
                                              self.mapping)

    @property
    def is_fully_set(self):
        return not self.DIT in self.plain

##############################################################################
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: Provide 1 argument, the word")
        sys.exit(1)
    word = sys.argv[1].upper()
    print(sorted(PATTERN_MAPPER.find_words(word)))
