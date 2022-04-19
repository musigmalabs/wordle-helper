from english_words import english_words_set as words
from collections import defaultdict, namedtuple


candidate_words = set([w.lower() for w in words if len(w) == 5])


GREY = 'grey'
GREEN = 'green'
YELLOW = 'yellow'


class Hint:
    """
    Represents a single letter in a response from the wordle puzzle.
    """
    def __init__(self, letter, color):
        self.letter = letter
        self.color = color


def grey(letter):
    """
    A helper method to indicate a grey letter.
    """
    return Hint(letter, GREY)


def green(letter):
    """
    A helper method to indicate a green letter.
    """
    return Hint(letter, GREEN)


def yellow(letter):
    """
    A helper method to indicate a yellow letter.
    """
    return Hint(letter, YELLOW)


class EqualsFilter:
    def __init__(self, operator, word):
        self.operator = operator
        self.word = word

    def is_valid(self, word):
        if self.operator == 'e':
            return self.word == word
        return self.word != word


class LocationFilter:
    def __init__(self, operator, location, letter):
        self.operator = operator
        self.location = location
        self.letter = letter
    
    def is_valid(self, word):
        if self.operator == 'e':
            return word[self.location] == self.letter
        return word[self.location] != self.letter


class CountingFilter:
    def __init__(self, operator, count, letter):
        self.operator = operator
        self.count = count
        self.letter = letter
    
    def is_valid(self, word):
        if self.operator == 'e':
            return word.count(self.letter) == self.count
        elif self.operator == 'ge':
            return word.count(self.letter) >= self.count

class Result:
    """
    Represents a five letter result from the wordle puzzle.
    """
    
    def __init__(self, result):
        assert len(result) == 5
        self.result = result
    
    def build_rules(self):
        rules = []

        grey = defaultdict(lambda: 0)
        yellow = defaultdict(lambda: 0)

        for i, clue in enumerate(self.result):
            if clue.color == GREEN:
                rules.append(LocationFilter('e', i, clue.letter))
            elif clue.color == GREY:
                grey[clue.letter] += 1
            elif clue.color == YELLOW:
                yellow[clue.letter] += 1
                rules.append(LocationFilter('ne', i, clue.letter))

        for clue_letter, count in yellow.items():
            # If this letter also appears in grey tiles, we know this is the final count.
            if clue_letter in grey:
                rules.append(CountingFilter('e', count, clue_letter))
                del grey[clue_letter]
            else:
                rules.append(CountingFilter('ge', count, clue_letter))
        
        for clue_letter, count in grey.items():
            rules.append(CountingFilter('e', 0, clue_letter))
        
        return rules


def build_histogram(words):
    hist = defaultdict(lambda: 1)
    for word in words:
        for c in word:
            hist[c] += 1
    return hist


def score(hist, word):
    uniq = set(list(word))

    s = 1
    for c in uniq:
        s *= hist[c]
    return s


def best_guess(candidates):
    """
    Produces the best guess from given candidates.
    """
    hist = build_histogram(candidates)
    ranked = sorted([(w, score(hist, w)) for w in candidates], key=lambda x: x[1], reverse=True)

    return ranked[0][0]


class Wordle:

    def __init__(self, blocked_words):
        self.rules = []
    
    def valid_candidate(self, candidate_word):
        for rule in self.rules:
            if not rule.is_valid(candidate_word):
                return False
        return True

    def filter_candidates(self, candidate_words):
        filtered = []

        for word in candidate_words:
            if self.valid_candidate(word):
                filtered.append(word)
        
        return filtered

    def next_guess(self):
        """
        Return the next guess to be presented to the wordle puzzle.
        """

        candidates = self.filter_candidates(candidate_words)
        return best_guess(candidates)

    def submit_result(self, result):
        """
        Provide the result from submitting a guess to the wordle puzzle.
        """
        self.rules += result.build_rules()


if __name__ == '__main__':
    wordle = Wordle()
    wordle.submit_result(Result([grey('a'), yellow('r'), yellow('o'), grey('s'), yellow('e')]))
    wordle.submit_result(Result([grey('t'), yellow('e'), grey('n'), yellow('o'), green('r')]))
    print (wordle.next_guess())
