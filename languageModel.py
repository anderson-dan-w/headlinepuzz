#!/usr/bin/python3

import collections
import re

## dwanderson modules
from dwanderson import texts

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

alice_fname = [t for t in texts if t.endswith("alice.txt")][0]
with open(alice_fname) as fh:
    text = str(fh.read()).upper()
    text, _n = re.subn("[^A-Z]", " ", text)    
    words = text.split()

single_freq = collections.Counter("".join(words))
double_freq = collections.defaultdict(int)
for word in words:
    if len(word) < 2:
        continue
    for i in range(len(word) - 1):
        double_freq[word[i:i+2]] += 1
triple_freq = collections.defaultdict(int)
for word in words:
    if len(word) < 3:
        continue
    for i in range(len(word) - 2):
        triple_freq[word[i:i+3]] += 1

single_probability = collections.defaultdict(float)
total = sum(single_freq.values())
for key, val in single_freq.items():
    single_probability[key] = val / total
double_probability = collections.defaultdict(float)
total = sum(double_freq.values())
for key, val in double_freq.items():
    double_probability[key] = val / total
triple_probability = collections.defaultdict(float)
total = sum(triple_freq.values())
for key, val in triple_freq.items():
    triple_probability[key] = val / total

def get_prob_3(string):
    if "?" not in string:
        return 0  ## i dont know what im trying to do. im tired. fuck this
