#!/usr/bin/python3
import os
import sys
import json
import unittest

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(HERE))))
from headlinepuzz import word as hlpword

DATA_DIR = os.path.join(HERE, "..", "data")

class TestPatternMapper(unittest.TestCase):
    def setUp(self):
        self.pattern_fname = os.path.join(DATA_DIR, "patterns.json")
        self.dict_fnames = [os.path.join(DATA_DIR, "words.dict"),
                            os.path.join(DATA_DIR, "more_words.dict")]
        self.cipher_fname = os.path.join(DATA_DIR, "cipher_words.json")
        with open(self.pattern_fname) as fh:
            self.expected_patterns = json.load(fh)
        self.expected_words = {word for words in self.expected_patterns.values()
                                    for word in words}
        with open(self.cipher_fname) as fh:
            self.cipher_words = json.load(fh)
        ## json doesn't like python sets; override it
        for d in self.cipher_words.values():
            d['words'] = set(d['words'])
        ## for premade PatternMapper, when we aren't testing the init
        self.pm = hlpword.PatternMapper(pattern_fname=self.pattern_fname)

    def test_readin_pattern_file(self):
        pm = hlpword.PatternMapper(pattern_fname=self.pattern_fname)
        self.assertEqual(self.expected_patterns, pm.patterns,
                "expected {}; got {}"
                .format(self.expected_patterns, pm.patterns))
        self.assertEqual(self.expected_words, pm.words,
                "expected {}; got {}".format(self.expected_words, pm.words))

    def test_readin_dict_files(self):
        pm = hlpword.PatternMapper(pattern_fname="nonexistent_file",
                                   dict_fnames=self.dict_fnames)
        self.assertEqual(self.expected_words, pm.words,
                "expected {}; got {}".format(self.expected_words, pm.words))

    def test_save_pattern_file(self):
        test_fname = "test_save.json"
        try:
            self.pm.save_pattern_file(test_fname, DATA_DIR)
            ## strip newlines because json.dump() has noeol at eof
            ## but manually created files implicitly do
            with open(os.path.join(DATA_DIR, self.pattern_fname)) as fh:
                expected_text = fh.read().replace("\n","")
            with open(os.path.join(DATA_DIR, test_fname)) as fh:
                text = fh.read().replace("\n","")
            self.assertEqual(expected_text, text,
                    "expected {}; got {}".format(expected_text, text))
        finally:
            if os.path.exists(os.path.join(DATA_DIR, test_fname)):
                os.remove(os.path.join(DATA_DIR, test_fname))

    def test_get_pattern(self):
        for word in self.expected_words:
            pattern = self.pm.get_pattern(word)
            self.assertIn(pattern, self.expected_patterns,
                    "didn't find expected pattern {}".format(pattern))
            self.assertIn(word, self.pm.patterns[pattern],
                    "word {} didn't show up under pattern {} as expected"
                    .format(word, pattern))

    def test_find_words(self):
        for cipher_word, values in self.cipher_words.items():
            words = self.pm.find_words(cipher_word)
            expected_words = values['words']
            self.assertEqual(expected_words, words,
                    "expected {}; got {}".format(expected_words, words))

    def test_find_words_with_mapping(self):
        for cipher_word, values in self.cipher_words.items():
            maps = {'all': len(values['words']), 'one':1, 'none':0}
            for map_type, count in maps.items():
                mapping = values['mapping'][map_type]
                words = self.pm.find_words(cipher_word, mapping=mapping)
                self.assertEqual(count, len(words),
                        "expected {} words; got {}".format(count, len(words)))

class TestWord(unittest.TestCase):
    ''' Tests for headlinepuzz.word '''
    def setUp(self):
        self.pattern_fname = os.path.join(DATA_DIR, "patterns.json")
        self.cipher_fname = os.path.join(DATA_DIR, "cipher_words.json")
        with open(self.cipher_fname) as fh:
            self.cipher_words = json.load(fh)
        ## json doesn't like python sets; override it
        for d in self.cipher_words.values():
            d['words'] = set(d['words'])
        ## override default Word.PATTERN_MAPPER; work with smaller dicts, etc
        self.pm = hlpword.PatternMapper(pattern_fname=self.pattern_fname)
        hlpword.Word.PATTERN_MAPPER = self.pm

    def test_init(self):
        for cipher_word, values in self.cipher_words.items():
            word = hlpword.Word(cipher_word)
            self.assertEqual(cipher_word, word.original_word)
            self.assertEqual(cipher_word, word.word)
            self.assertEqual(values['pattern'], word.pattern)

    def test_plain(self):
        word = hlpword.Word("DOGS")
        self.assertEqual(self.pm.DIT*len(word.word), word.plain)
        word.plain = "F"
        self.assertEqual("F"+self.pm.DIT*(len(word.word) - 1), word.plain)
        word.plain = "FISH"
        self.assertEqual("FISH", word.plain)

    def test_is_fully_set(self):
        word = hlpword.Word("DOGS")
        self.assertFalse(word.is_fully_set)
        word.plain = "F"
        self.assertFalse(word.is_fully_set)
        word.plain = "FISH"
        self.assertTrue(word.is_fully_set)

    def test_possibles(self):
        word = hlpword.Word("BUBBA")
        self.assertEqual({'SASSY', 'NANNY'}, word.possibles)
        word.plain = "P"
        self.assertEqual(set(), word.possibles)
        word.plain = ""
        self.assertEqual({'SASSY', 'NANNY'}, word.possibles)
        word.plain = "S"
        self.assertEqual({'SASSY'}, word.possibles)

if __name__ == '__main__':
    unittest.main()
