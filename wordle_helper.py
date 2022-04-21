from word_bank import get_words
from collections import defaultdict


candidate_words = get_words()

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
    
    def __repr__(self):
        return f'word {self.operator} {self.word}'


class LocationFilter:
    def __init__(self, operator, location, letter):
        self.operator = operator
        self.location = location
        self.letter = letter
    
    def is_valid(self, word):
        if self.operator == 'e':
            return word[self.location] == self.letter
        return word[self.location] != self.letter
    
    def __repr__(self):
        return f'word[{self.location}] {self.operator} {self.letter}'


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
    
    def __repr__(self):
        return f'word.count({self.letter}) {self.operator} {self.count}'

class Result:
    """
    Represents a five letter result from the wordle puzzle.
    """
    
    def __init__(self, result):
        assert len(result) == 5
        self.result = result
    
    def build_rules(self):
        rules = []

        green = defaultdict(lambda: 0)
        grey = defaultdict(lambda: 0)
        yellow = defaultdict(lambda: 0)

        for clue in self.result:
            if clue.color == GREEN:
                green[clue.letter] += 1
            if clue.color == GREY:
                grey[clue.letter] += 1
            if clue.color == YELLOW:
                yellow[clue.letter] += 1
        
        for i, clue in enumerate(self.result):
            letter = clue.letter

            greens = green[letter]
            greys = grey[letter]
            yellows = yellow[letter]

            if clue.color == GREEN:
                rules.append(LocationFilter('e', i, clue.letter))
            if clue.color == YELLOW:
                if greys != 0:
                    rules.append(CountingFilter('e', yellows + greens, letter))
                else:
                    rules.append(CountingFilter('ge', yellows, letter))
                
                rules.append(LocationFilter('ne', i, letter))
            if clue.color == GREY:
                if yellows + greens == 0:
                    rules.append(CountingFilter('e', 0, letter))
        
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


def score2(hist, word):
    counts = defaultdict(lambda: 0)
    for c in word:
        counts[c] += 1
    
    s = 1

    for c, count in counts.items():
        score = hist[c]
        s += score
        s += ((count-1) * .0001 * score)
    
    return s


def best_guess(candidates, guesses):
    """
    Produces the best guess from given candidates.
    """
    hist = build_histogram(candidates)
    ranked = sorted([(w, score2(hist, w)) for w in candidates if w not in guesses], key=lambda x: x[1], reverse=True)

    return ranked[0][0]


class Wordle:

    def __init__(self, blocked_words=[]):
        self.words = candidate_words
        self.rules = [EqualsFilter('ne', w) for w in blocked_words]
        self.guesses = set()
    
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

        candidates = self.filter_candidates(self.words)

        guess = best_guess(candidates, self.guesses)
        self.guesses.add(guess)

        return guess

    def submit_result(self, result):
        """
        Provide the result from submitting a guess to the wordle puzzle.
        """
        self.rules += result.build_rules()
        #print(self.rules)


if __name__ == '__main__':
    wordle = Wordle(['marco', 'carlo', 'osier', 'rosen'])
    wordle.submit_result(Result([grey('p'), yellow('e'), grey('a'), yellow('r'), grey('l')]))
    wordle.submit_result(Result([grey('h'), grey('o'), yellow('r'), grey('s'), green('e')]))
    wordle.submit_result(Result([grey('t'), green('r'), green('i'), grey('b'), green('e')]))
    wordle.submit_result(Result([grey('c'), green('r'), green('i'), grey('m'), green('e')]))
    print(wordle.next_guess())
