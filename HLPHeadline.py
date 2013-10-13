#!/usr/bin/python

## python modules
import collections

## dwanderson modules
import dwanderson
import HLPWord as W

ALPHABET = W.ALPHABET

##############################################################################
class Headline(object):
    def __init__(self, string, quick=None):
        self.real_cipher = string.upper()
        self.cipher = "".join(l for l in self.real_cipher
                if l.isalpha() or l.isspace())
        self.word_list = self.cipher.split(" ")
        self.nwords = len(self.word_list)
        self.words = {w : W.Word(w, quick=quick) for w in self.word_list}
        self.loop_strings = []
        self.mapping = collections.defaultdict(lambda:"?")

    ##======================================================================##
    def _get_plain(self):
        return " ".join(self.words[w].get_plain() for w in self.word_list)

    def __str__(self):
        string = ""
        width, _h = dwanderson.get_terminal_size()
        plain = self._get_plain()
        for lines in range((len(self.cipher) + width - 1) // width):
            start, stop = width * lines, width * lines + width
            string += self.cipher[start:stop] + "\n"
            string += plain[start:stop] + "\n\n"
        return string[:-2] ## chop off the last two newlines

    ##======================================================================##
    def update_possibles(self):
        for word in self.words.values():
            word.mapping = self.mapping
            word.set_possibles()
        return

    def get_possibles_for(self, value=None):
        if isinstance(value, str) and value.upper() in self.word_list:
            return value.upper(), self.words[value.upper()].possibles
        if not isinstance(value, (int, type(None))):
            return "{} not found...".format(value)
        words = sorted(self.words.values(), key=lambda x:len(x.possibles))
        if isinstance(value, int):
            n = self.nwords
            if value < -1*n or value >= n:
                return "Pick value between [{},{})".format(-1*n, n)
            word = words[value]
            return word.word, word.possibles
        ## value=None, get first non-filled-in word
        for word in words:
            if word.is_fully_set():
                continue
            return word.word, word.possibles
        return "[Everything is set...]"

    ##======================================================================##
    def set_letters(self, cipher, plain, update=True):
        cipher, plain = cipher.upper(), plain.upper()
        self.mapping.update(dict(zip(cipher, plain)))
        if update:
            self.update_possibles()
        return

    def unset_letters(self, cipher, update=True):
        for lett in cipher.upper():
            try:
                self.mapping.pop(lett)
            except KeyError as e:
                pass
        if update:
            self.update_possibles()
        return

    def unset_all(self, update=True):
        self.mapping = collections.defaultdict(lambda:"?")
        if update:
            self.update_possibles()
        return
