

ALPHABET = ''.join([chr(ord('a')+i) for i in range(26)])

class Possibility:
    def __init__(self, letter, complete, extendable_end, extendable_start):
        self.letter = letter
        self.complete = complete
        self.extendable_end = extendable_end
        self.extendable_start = extendable_start

class PatternNode:
    def __init__(self):
        self.childs = {}

    def get(self, letter):
        if letter not in self.childs:
            self.childs[letter] = PatternNode()
        return self.childs[letter]

    def get_node(self, string):
        if len(string) == 0:
            return self
        if string[0] not in self.childs:
            return None
        return self.childs[string[0]].get_node(string[1:])

    def has_childs(self):
        return len(self.childs) > 0

    def completions(self):
        return set(self.childs.keys())

class PatternDict:
    def __init__(self):
        self.root = PatternNode()

    def add(self, obj):
        if isinstance(obj, str):
            #self._add_word(obj)
            self._fast_add_word(obj)
        elif isinstance(obj, list):
            for w in obj:
                self.add(w)
                
    def _fast_add_word(self, word):
        for i in range(len(word)):
            node = self.root
            for j in range(i, len(word)):
                node = node.get(word[j])

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
        """
        Check that all words in a list are valid words
        """
        return all(w in self.dictionnary for w in words)

    def _simple_possibilities(self, string):
        """
        Using a string un the format "%.%" where % is a string of any length (including 0),
        get all possible letters in place of the '.', including possible incomplete words (extending left or right).
        The possible letters are returned as `Possibility` structs
        """
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
        possibilities = [poss for poss in main_possibilities if poss.letter in side_letters]
        return possibilities

'''
P = PatternDict()
P.add(["panneau", "train", "voiture", "eau", "tete", "geant"])
P.pretty_print(limit=3)
'''



