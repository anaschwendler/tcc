from conceptrank.summarize import select_by_word_budget, select_mmr


def test_word_budget_takes_best_sentences_in_document_order():
    sentences = ["um dois três", "quatro cinco", "seis sete oito nove"]
    ratings = {"um dois três": 0.5, "quatro cinco": 0.1, "seis sete oito nove": 0.9}
    assert select_by_word_budget(sentences, ratings, 7) == ["um dois três", "seis sete oito nove"]


def test_word_budget_cuts_the_lowest_rated_sentence_taken():
    sentences = ["um dois três", "quatro cinco", "seis sete oito nove"]
    ratings = {"um dois três": 0.5, "quatro cinco": 0.1, "seis sete oito nove": 0.9}
    assert select_by_word_budget(sentences, ratings, 5) == ["um", "seis sete oito nove"]


def test_word_budget_larger_than_text_takes_everything():
    sentences = ["um dois", "três"]
    ratings = {"um dois": 0.2, "três": 0.8}
    assert select_by_word_budget(sentences, ratings, 100) == ["um dois", "três"]


def test_mmr_with_lambda_one_is_selection_by_score():
    sentences = ["um dois", "três quatro", "cinco seis"]
    scores = [0.2, 0.9, 0.5]
    similarities = [[1, 0.9, 0], [0.9, 1, 0], [0, 0, 1]]
    ratings = dict(zip(sentences, scores))
    assert select_mmr(sentences, scores, similarities, 4, 1.0) == select_by_word_budget(sentences, ratings, 4)


def test_mmr_skips_a_near_duplicate():
    sentences = ["avião caiu congo", "avião caiu no congo", "onu confirmou mortes"]
    scores = [0.9, 0.85, 0.6]
    similarities = [[1, 0.95, 0.1], [0.95, 1, 0.1], [0.1, 0.1, 1]]
    # after the first sentence: near-duplicate 0.7 * 0.944 - 0.3 * 0.95 = 0.376,
    # third sentence 0.7 * 0.667 - 0.3 * 0.1 = 0.437
    assert select_mmr(sentences, scores, similarities, 6, 0.7) == ["avião caiu congo", "onu confirmou mortes"]
