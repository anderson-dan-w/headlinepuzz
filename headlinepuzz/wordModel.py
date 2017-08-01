#!/usr/bin/python3
import collections
import itertools
import math

from .hlpConstants import TEXT_FNAMES
from .alphabetSubstitution import ALPHABET, DIT

## text_words and text should NOT be set()s, because they help determine
## n-graph frequency, so we want to know which ones show up more frequently
text_words = []
for fname in TEXT_FNAMES:
    with open(fname) as fh:
        text = fh.read()
    text = [w.upper() for w in text.split() if w.isalpha()]
    text_words.extend(text)


class Frequency(object):
    def __init__(self, graph_length, words=None):
        self.graph_length = graph_length
        self.ncounts = 0
        self.counts = collections.defaultdict(int)
        self.shorter = None
        if words is not None:
            self.updateCounts(words)

    def updateCounts(self, words):
        ## for dealing with words shorter than self.graph_length, which
        ## would otherwise have probability 0
        if self.graph_length > 1:
            shorter_words = [w for w in words if len(w) < self.graph_length]
            self.shorter = Frequency(self.graph_length - 1, shorter_words)
        for word in words:
            if len(word) < self.graph_length:
                continue
            for i in range(len(word) - self.graph_length + 1):
                graph = word[i:i + self.graph_length]
                self.counts[graph] += 1
        self.ncounts = sum(self.counts.values())

    def getGraphProbability(self, graph):
        print("prob {}".format(graph))
        vs_random = self.ncounts or 1  ## prevent divide-by-zero error
        dit_smoother = len(ALPHABET) ** graph.count(DIT)
        iterables = [ALPHABET if l == DIT else l for l in graph]
        graph_count = 0
        for it in itertools.product(*iterables):
            putative_graph = "".join(it)
            graph_count += self.counts[putative_graph]
        return (graph_count / vs_random) / dit_smoother

    def getGraphScore(self, graph):
        print("score {}".format(graph))
        graph_prob = self.getGraphProbability(graph)
        if graph_prob == 0.0:
            ## arbitrary - just make it worse than "average"
            graph_prob = self.getGraphProbability(DIT * self.graph_length) / 2
        normalized = graph_prob * (len(ALPHABET) ** self.graph_length)
        return math.log(normalized, 2)  ## base-2 is arbitrary

    ## named to present consistent interface: all scorers will have .score()
    def score(self, word):
        len_word = len(word)
        if len_word < self.graph_length:
            return self.shorter.score(word)
        ngraphs = len_word - self.graph_length + 1
        cumulative = 0
        for i in range(ngraphs):
            cumulative += self.getGraphScore(word[i:i + self.graph_length])
        average = cumulative / ngraphs
        return average

    def scoreWords(self, words):
        return sum(self.score(word) for word in words) / len(words)
