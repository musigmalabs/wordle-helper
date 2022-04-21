from english_words import english_words_set as words

candidate_words = set([w.lower() for w in words if len(w) == 5])

def get_words():
    return candidate_words
