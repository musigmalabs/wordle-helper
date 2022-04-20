from collections import defaultdict


class WordleSimulator:
    """
    Simulates the wordle game for the given word.
    """

    def __init__(self, word):
        self.word = word

    def guess(self, word):
        result = ['' for i in range(5)]

        char_counter = defaultdict(lambda: 0)
        for c in self.word:
            char_counter[c] += 1

        for i, c in enumerate(word):
            if self.word[i] == c:
                result[i] = 'green'
                char_counter[c] -= 1
            elif c not in self.word:
                result[i] = 'grey'
            else:
                if char_counter[c] != 0:
                    result[i] = 'yellow'
                    char_counter[c] -= 1
                else:
                    result[i] = 'grey'
        
        return result
