"""Simple baselines, as sentence ratings for select_by_word_budget().

- Lead: the opening sentences of each text, taken in turns (first sentence of
  every text, then the second of every text, ...), the usual multi-document
  version of Lead.
- Random: random ratings from a seeded generator.
"""

import random


def lead_ratings(sources):
    """{sentence: rating} for a cluster's sources (each a list of sentences)."""
    ratings = {}
    for source_index, sentences in enumerate(sources):
        for position, sentence in enumerate(sentences):
            rating = -(position * len(sources) + source_index)
            ratings[sentence] = max(ratings.get(sentence, rating), rating)
    return ratings


def random_ratings(sentences, seed):
    generator = random.Random(seed)
    return {sentence: generator.random() for sentence in sentences}
