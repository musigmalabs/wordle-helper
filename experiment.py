from english_words import english_words_set as words

from wordle_helper import *
from simulator import *


candidate_words = sorted([w.lower() for w in words if len(w) == 5][:1000])


def format_result(result, guess):
    resp = []
    for i, color in enumerate(result):
        if color == 'grey':
            resp.append(grey(guess[i]))
        elif color == 'green':
            resp.append(green(guess[i]))
        else:
            resp.append(yellow(guess[i]))
    return Result(resp)


def run_word(word):
    wordle = Wordle()
    sim = WordleSimulator(word)

    attempts = 0
    while True:
        guess = wordle.next_guess()
        if guess == sim.word:
            return attempts

        result = format_result(sim.guess(guess), guess)
        wordle.submit_result(result)

        attempts += 1


def run_experiment():
    hist = defaultdict(lambda: 0)

    for word in candidate_words:
        attempts = run_word(word)
        hist[attempts] += 1
    
    print(hist)


if __name__ == '__main__':
    run_experiment()
