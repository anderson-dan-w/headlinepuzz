#/usr/bin/python3
import os

dict_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "texts")
DICT_FNAMES = {os.path.join(dict_dir, fname) for fname in os.listdir(dict_dir)
                if fname.endswith(".dict")}
text_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "texts")
TEXT_FNAMES = {os.path.join(text_dir, fname) for fname in os.listdir(text_dir)
                if fname.endswith(".txt")}

HLPDIR = os.path.join(os.getenv("HOME"), ".hlp")
NUMERICALS_FNAME = "numericals.json"
PATTERNS_FNAME = "patterns.json"
