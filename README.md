# wordle-helper

A simple CLI tool to help solve Wordle puzzle efficiently.

## Installation

Clone this repo and install requirements. Then run the cli.py file.

```
$ python3 cli.py
```

## Example Run

This is for 21st April 2022 daily puzzle:

```
➜  wordle-helper git:(main) ✗ python3 cli.py
Welcome to wordle shell
[wordle] start
Try arose
[wordle] result bbybg
Try dolce
[wordle] result yybbg
Try oxide
[wordle]
```

## Notes

1. Sometimes Wordle rejects a word from my dictionary. If that happens, you can just write "block" to the CLI and it will update the guess.
2. The "result" 5 letter code is simply the colors you get for your guess. Note that grey code is b (for black) as grey and green both start with g.
3. In vast majority cases, the tool will get the answer in or under 3 attempts. In very rare cases (< 20 in the word bank of 3200.. see the experiments.py), it actually won't be able to guess in 6 attempts. I am working on improving that through improved scoring functions.
4. In some rare cases, there are words in the wordle app word bank that are missing from my dictionary. Any word contributions are more than welcome (see word_bank.py).
