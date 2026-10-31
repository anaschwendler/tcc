from conceptrank.summarize import select_by_word_budget


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
