#!/usr/bin/python3

class Decimation(object):
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def startAlphabetAt(self, letter):
        index = self.alphabet.index(letter)
        self.alphabet = self.alphabet[index:] + self.alphabet[:index]

    def suggest(self):
        back_one, back_two = "", ""
        last = "UVWXYZ"
        for letter in last:
            index = self.alphabet.index(letter)
            back_one += self.alphabet[index - 1]
            back_two += self.alphabet[index - 2]
        return back_two, back_one, last
