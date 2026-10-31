"""Loading the raw CSTNews corpus. Skipped when data/raw/CSTNews/ is absent."""

import pytest

from conceptrank.corpus import RAW_DIR, load_corpus, parse_extract, repair_name

needs_corpus = pytest.mark.skipif(not RAW_DIR.exists(), reason="raw CSTNews not in data/raw/")


@pytest.fixture(scope="module")
def corpus():
    return load_corpus()


@needs_corpus
def test_corpus_size(corpus):
    assert [c.id for c in corpus] == [f"C{i}" for i in range(1, 51)]
    assert sum(len(c.sources) for c in corpus) == 140


@needs_corpus
def test_names_are_repaired(corpus):
    by_id = {c.id: c for c in corpus}
    assert by_id["C37"].topic == "MotimMaranhão"
    assert by_id["C37"].agreement == "CST"
    assert by_id["C40"].category == "Politica"
    assert {c.category for c in corpus} == {
        "Ciencia", "Cotidiano", "Dinheiro", "Esportes", "Mundo", "Politica",
    }


@needs_corpus
def test_titles_are_not_sentences(corpus):
    for cluster in corpus:
        for source in cluster.sources:
            if source.title is not None:
                assert source.title not in source.sentences


@needs_corpus
def test_extract_points_to_existing_sources(corpus):
    for cluster in corpus:
        source_ids = {s.id for s in cluster.sources}
        assert cluster.human_extract
        assert {e.source_id for e in cluster.human_extract} <= source_ids


@needs_corpus
def test_extract_source_contains_the_sentence(corpus):
    for cluster in corpus:
        sources = {s.id: s for s in cluster.sources}
        for e in cluster.human_extract:
            if e.text in cluster.sentences:
                assert e.text in sources[e.source_id].sentences


@needs_corpus
def test_extract_source_overrides_wrong_tag(corpus):
    by_id = {c.id: c for c in corpus}
    # Tagged "<D1_C31_Estadao; ...>", but D1 is Folha and the sentence is in D2.
    assert {e.source_id for e in by_id["C31"].human_extract} == {"D2"}
    # Tagged "<D1_C30_OGlobo; ...>", but D1 is Folha; two sentences are found in
    # D3 (OGlobo) and two differ from the source, so the agency decides.
    assert {e.source_id for e in by_id["C30"].human_extract} == {"D3"}


@needs_corpus
def test_text_has_no_encoding_leftovers(corpus):
    for cluster in corpus:
        texts = [cluster.cstsumm, cluster.human_abstract, *cluster.sentences]
        texts += [e.text for e in cluster.human_extract]
        for text in texts:
            assert "�" not in text and "\x93" not in text and "\x94" not in text


def test_parse_extract_tag_variants():
    text = "\n".join([
        "Primeira frase. <D1_C1_Folha; p1-s1>",
        "Segunda frase. <D2_C41_Estadao: p3-s2>",
        "Terceira frase. <D1_C5_Folha_p2-s1>",
        "Quarta frase. <D3_C9_JB; P4-S2>",
        "Quinta frase. <D1_C2_Folha; p1_s3>",
        "Sexta frase. D2_C26_Estadao; p5-s1>",
    ])
    extract = parse_extract(text)
    assert [e.text for e in extract] == [
        "Primeira frase.", "Segunda frase.", "Terceira frase.",
        "Quarta frase.", "Quinta frase.", "Sexta frase.",
    ]
    assert [(e.source_id, e.position) for e in extract] == [
        ("D1", "p1-s1"), ("D2", "p3-s2"), ("D1", "p2-s1"),
        ("D3", "p4-s2"), ("D1", "p1-s3"), ("D2", "p5-s1"),
    ]


def test_repair_name():
    assert repair_name("C40_Polбtica_ProcuradorRenan") == "C40_Política_ProcuradorRenan"
    assert repair_name("C1_Mundo_AviaoCongo") == "C1_Mundo_AviaoCongo"
