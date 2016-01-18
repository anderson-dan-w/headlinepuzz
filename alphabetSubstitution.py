#!/usr/bin/python3
import collections
import string

ALPHABET = string.ascii_uppercase
DIT = "?"

class AlphabetSubstitution(collections.defaultdict):
    ALPHABET = ALPHABET
    DIT = DIT

    def __init__(self, *args, **kwargs):
        super(AlphabetSubstitution, self).__init__(lambda: DIT, *args, **kwargs)

    @property
    def cycles(self):
        ## modifies cycles in place
        def changes(cycle, cycles):
            change = False
            start, end = cycle[:-1], cycle[-1]
            for index, cycle2 in enumerate(cycles):
                if cycle2.startswith(end) and cycle2 != cycle:
                    cycles[index] = start + cycle2
                    change = True
                    break
            if change:
                cycles.remove(cycle)
            return change

        cycles = [k+v for k,v in self.items() if v != self.DIT]
        while any(changes(c, cycles) for c in cycles):
            pass ## changes() operates in-place
        return cycles

    @property
    def is_fully_set(self):
        return set(self.values()) == set(self.ALPHABET)
