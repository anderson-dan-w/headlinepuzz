#!/usr/bin/python3
import unittest

from headlinepuzz import headline as hlpheadline

class HeadlineTestCase(unittest.TestCase):
    def setUp(self):
        self.true_plain = "HEADLINE PUZZLES SOMETIMES CONFUSE CRYPTOGRAPHERS"
        ## nb: rot13 for simplicity
        self.cipher = "URNQYVAR CHMMYRF FBZRGVZRF PBASHFR PELCGBTENCUREF"
        self.plain = "".join("?" if l.isupper() else l for l in self.cipher)
        self.headline_words = self.cipher.split()
        self.headline = hlpheadline.Headline(self.cipher)

    def test_init(self):
        headline = hlpheadline.Headline(self.cipher)
        self.assertEqual(len(self.headline_words), len(headline.words))
        for exp, got in zip(self.headline_words, headline.words):
            self.assertEqual(exp, got.word)

    def test_strs(self):
        self.assertEqual(self.cipher, self.headline.cipher)
        self.assertEqual(self.plain, self.headline.plain)
        self.assertEqual("{}\n{}".format(self.cipher, self.plain),
                         str(self.headline))

    def test_shared_mapping(self):
        for word in self.headline.words:
            self.assertIs(self.headline.mapping, word.mapping,
                    "word mappings aren't pointing to headline mapping")

    def test_mapping(self):
        self.headline.set_letters("PEL", "CRY")
        d = {c: p for c, p in zip("PEL", "CRY")}
        self.assertDictEqual(d, self.headline.mapping)
        self.headline.unset_cipher("P")
        self.assertNotIn("P", self.headline.mapping)
        self.headline.unset_plain("Y")
        self.assertNotIn("Y", self.headline.mapping.values())
        self.headline.unset_cipher()
        self.assertDictEqual({}, self.headline.mapping)

    def test_is_fully_set(self):
        self.assertFalse(self.headline.is_fully_set)
        self.headline.words[0].plain = self.plain.split(" ")[0]
        self.assertFalse(self.headline.is_fully_set)
        for plain, word in zip(self.true_plain.split(" "), self.headline.words):
            print("{}: {}".format(word, word.possibles))
            word.plain = plain
        self.assertTrue(False)
        self.assertTrue(self.headline.is_fully_set)
