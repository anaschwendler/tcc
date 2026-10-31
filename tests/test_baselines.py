from conceptrank.baselines import lead_ratings, random_ratings
from conceptrank.summarize import select_by_word_budget


def test_lead_takes_opening_sentences_in_turns():
    sources = [["a1 x", "a2 x", "a3 x"], ["b1 x", "b2 x"]]
    sentences = [s for source in sources for s in source]
    chosen = select_by_word_budget(sentences, lead_ratings(sources), 6)
    assert chosen == ["a1 x", "a2 x", "b1 x"]


def test_lead_keeps_the_best_rating_of_a_repeated_sentence():
    sources = [["igual", "a2"], ["b1", "igual"]]
    assert lead_ratings(sources)["igual"] == 0


def test_random_is_reproducible():
    sentences = ["a", "b", "c"]
    assert random_ratings(sentences, 1) == random_ratings(sentences, 1)
    assert random_ratings(sentences, 1) != random_ratings(sentences, 2)
