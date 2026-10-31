import pytest

from conceptrank.concept import WivesSummarizer


def similarity(words1, words2):
    tf1, tf2 = WivesSummarizer()._compute_tf([words1, words2])
    return WivesSummarizer.compute_distance(words1, words2, tf1, tf2, {})


def test_identical_sentences():
    assert similarity(["aviao", "caiu", "congo"], ["aviao", "caiu", "congo"]) == pytest.approx(1.0)


def test_disjoint_sentences():
    assert similarity(["aviao", "caiu"], ["chuva", "forte"]) == 0.0


def test_symmetric():
    a, b = ["aviao", "aviao", "caiu", "congo"], ["aviao", "congo", "onu"]
    assert similarity(a, b) == pytest.approx(similarity(b, a))


def test_equal_weights_reduce_to_jaccard():
    # every word appears once, so all weights are 1 and each common word adds 1
    assert similarity(["a", "b", "c"], ["b", "c", "d", "e"]) == pytest.approx(2 / 5)


def test_different_weights_count_less():
    # "aviao" has weight 1 in the first sentence and 0.5 in the second:
    # m1 = min(0.5, 2, 1) = 0.5; negations 0 and 0.5 give m2 = min(1, 0, 1) = 0,
    # so it adds 0.25, over 2 distinct words in the union
    a, b = ["aviao"], ["aviao", "caiu", "caiu"]
    assert similarity(a, b) == pytest.approx(0.25 / 2)
