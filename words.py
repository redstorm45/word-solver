

ALPHABET = ''.join([chr(ord('a')+i) for i in range(26)])

class Possibility:
    def __init__(self, letter, complete, extendable_end, extendable_start):
        self.letter = letter
        self.complete = complete
        self.extendable_end = extendable_end
        self.extendable_start = extendable_start
'''
class PatternNode:
    def __init__(self):
        self.childs = {}

    def get(self, letter):
        if letter not in self.childs.keys():
            self.childs[letter] = PatternNode()
        return self.childs[letter]

    def get_node(self, string):
        if len(string) == 0:
            return self
        elif string[0] not in self.childs.keys():
            return None
        return self.childs[string[0]].get_node(string[1:])

    def has_childs(self):
        return len(self.childs.keys()) > 0

    def completions(self):
        return set(self.childs.keys())

    def pretty_print(self, base_level=1, ignore=1, limit=None):
        K = sorted(list(self.childs.keys()))
        for k in K:
            w = ""
            if ignore > 0:
                w = ":" + self.childs[k].repr_list()
            print(" "*base_level + "-" + k + w)
            if limit is not None and limit > 1:
                self.childs[k].pretty_print(base_level+1, ignore+1, limit-1)

    def repr_list(self):
        return "{" + ",".join(sorted(list(self.words))) + "}"
'''

class PatternNode:
    def __init__(self):
        self.childs = [None]*26

    def get(self, letter):
        pos = ord(letter)-ord('a')
        if self.childs[pos] is None:
            self.childs[pos] = PatternNode()
        return self.childs[pos]

    def get_node(self, string):
        if len(string) == 0:
            return self
        pos = ord(string[0])-ord('a')
        if self.childs[pos] is None:
            return None
        return self.childs[pos].get_node(string[1:])

    def has_childs(self):
        return any(c is not None for c in self.childs)

    def completions(self):
        return set(ALPHABET[i] for i,e in enumerate(self.childs) if e is not None)
'''
    def pretty_print(self, base_level=1, ignore=1, limit=None):
        K = sorted(list(self.childs.keys()))
        for k in K:
            w = ""
            if ignore > 0:
                w = ":" + self.childs[k].repr_list()
            print(" "*base_level + "-" + k + w)
            if limit is not None and limit > 1:
                self.childs[k].pretty_print(base_level+1, ignore+1, limit-1)

    def repr_list(self):
        return "{" + ",".join(sorted(list(self.words))) + "}"
'''
class PatternDict:
    def __init__(self):
        self.root = PatternNode()

    def add(self, obj):
        if isinstance(obj, str):
            self._add_word(obj)
        elif isinstance(obj, list):
            for w in obj:
                self.add(w)

    def _add_word(self, word):
        for i in range(len(word)):
            self._add_word_forward(word[i:], word)

    def _add_word_forward(self, chain, word):
        node = self.root
        for letter in chain:
            node = node.get(letter)
            #node.register(word)

    def get_node(self, string):
        return self.root.get_node(string)

    def pretty_print(self, limit=None):
        print("Patterns:")
        self.root.pretty_print(limit=limit)

class WordMatcher:
    def __init__(self):
        self.dictionnary = set()
        self.search_forward = PatternDict()
        self.search_reverse = PatternDict()

    def set_dict(self, L, cb_progress=None, cb_stop=None):
        for i in range(len(L)):
            e = L[i]
            self.dictionnary.add(e)
            self.search_forward.add(e)
            self.search_reverse.add(e[::-1])
            if cb_progress is not None:
                cb_progress(i, len(L))
            if cb_stop is not None:
                if cb_stop():
                    break

    def are_valid(self, words):
        # all words exist
        return all(w in self.dictionnary for w in words)

    def _simple_possibilities(self, string):
        start, end = string.split('.')
        after_start = self.search_forward.get_node(start)
        if after_start is None:
            return []
        after_end = self.search_reverse.get_node(end[::-1])
        if after_end is None:
            return []
        join_letters = after_start.completions().intersection(after_end.completions())
        if len(join_letters) == 0:
            return []
        # there are possibilities! just list them all
        poss = []
        for k in join_letters:
            proposition = start+k+end
            forward_node = after_start.get_node(k+end)
            if forward_node is None:
                continue
            reverse_node = after_end.get_node(k+start[::-1])
            if reverse_node is None:
                continue
            #complete = forward_node.has(proposition)
            complete = proposition in self.dictionnary
            extendable_end = forward_node.has_childs()
            extendable_start = reverse_node.has_childs()
            poss.append(Possibility(k, complete, extendable_end, extendable_start))
        return poss

    def get_possibilities(self, option):
        complete_sides = [s for s in option.side_patterns if (('.' not in s) and len(s) > 1)]
        if not self.are_valid(complete_sides):
            return []
        incomplete_sides = [s for s in option.side_patterns if '.' in s and len(s) > 1]
        if len(incomplete_sides) > 0:
            possibilities_side = self._simple_possibilities(incomplete_sides[0])
            possibilities_side = [pos for pos in possibilities_side if pos.complete]
            if len(possibilities_side) == 0:
                return []
            side_letters = {p.letter for p in possibilities_side}
        else:
            side_letters = {l for l in ALPHABET}
        main_possibilities = self._simple_possibilities(option.combined_main())
        possibilities = []
        for poss in main_possibilities:
            if poss.letter in side_letters:
                possibilities.append(poss)
        return possibilities

'''
P = PatternDict()
P.add(["panneau", "train", "voiture", "eau", "tete", "geant"])
P.pretty_print(limit=3)
'''



