#!/usr/bin/python
import collections

from headlinepuzz import word as W
from headlinepuzz.alphabetSubstitution import AlphabetSubstitution

##############################################################################
class Headline(object):
    def __init__(self, headline_str):
        self.mapping = AlphabetSubstitution()
        self.words = [W.Word(w, self.mapping) for w in headline_str.split()]

    @property
    def plain(self):
        return " ".join(w.plain for w in self.words)

    @property
    def cipher(self):
        return " ".join(w.word for w in self.words)

    def __str__(self):
        return "{}\n{}".format(self.cipher, self.plain)

    @property
    def is_fully_set(self):
        return all(w.is_fully_set for w in self.words)

    def set_letters(self, cipher, plain):
        self.mapping.update(dict(zip(cipher, plain)))

    def unset_cipher(self, cipher=None):
        if cipher is None:
            self.mapping.clear()
            return
        for letter in cipher:
            self.mapping.pop(letter, None)

    def unset_plain(self, plain_letters):
        ## can't remove from mapping while iterating over it; two step process:
        to_remove = {c for c, p in self.mapping.items() if p in plain_letters}
        for cipher in to_remove:
            self.mapping.pop(cipher, None)

    @property
    def next_likeliest(self):
        by_npossible = sorted(self.words, key=lambda w:len(w.possibles))
        for word in by_npossible:
            if not word.is_fully_set and word.possibles:
                return word
        return None
