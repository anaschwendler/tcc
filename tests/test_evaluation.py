import pytest

from conceptrank.evaluation import PortugueseTokenizer, evaluate, score


def test_portuguese_tokenizer_keeps_accents():
    tokens = PortugueseTokenizer().tokenize("A Ação do Governo, na segunda-feira: R$ 3,5 mi.")
    assert tokens == ["a", "ação", "do", "governo", "na", "segunda", "feira", "r", "3", "5", "mi"]


def test_portuguese_tokenizer_normalizes_unicode():
    composed = "ação"
    decomposed = "ação"
    assert PortugueseTokenizer().tokenize(decomposed) == PortugueseTokenizer().tokenize(composed)


def test_identical_texts_score_one():
    text = "O avião caiu na floresta. Não houve sobreviventes."
    for s in score(text, text).values():
        assert s.precision == s.recall == s.fmeasure == 1.0


def test_accents_matter_only_with_portuguese_tokenizer():
    # "sessão" and "seção" share no token in Portuguese, but the ROUGE-1.5.5
    # tokenizer reduces both to "se", "o" (plus "ss" / nothing).
    summary, reference = "seção", "sessão"
    assert score(summary, reference, "portuguese")["rouge1"].recall == 0.0
    assert score(summary, reference, "rouge155")["rouge1"].recall > 0.0


def test_rouge1_counts():
    s = score("o avião caiu", "o avião explodiu e caiu")["rouge1"]
    assert s.precision == 1.0
    assert s.recall == pytest.approx(3 / 5)


def test_evaluate_rows():
    rows = evaluate({"C1": "o avião caiu"}, {"C1": "o avião caiu"})
    assert {r["metric"] for r in rows} == {"rouge1", "rouge2", "rouge3", "rouge4", "rougeL"}
    assert all(r["cluster"] == "C1" for r in rows)
