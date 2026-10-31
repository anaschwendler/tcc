"""Summarize every CSTNews cluster the way the thesis did.

Ported from the corpus loops in archive/BetaRank.ipynb and archive/ConceptRank.ipynb.
The legacy choices are kept so the output can be compared with
archive/experiments_2016/: English tokenizer, stemmer and stop words; the sumy 0.4.1
word filter, which drops hyphenated words; summary length taken from the
number of '.' in the CSTSumm summary; sentences written with no separator.

    uv run python -m conceptrank.summarize lexrank archive/experiments_2016 runs/legacy
"""

import argparse
import re
from pathlib import Path

from sumy.models.dom import ObjectDocumentModel, Paragraph, Sentence
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.utils import get_stop_words

from conceptrank.concept import ConceptSummarizer
from conceptrank.lexrank import LexRankSummarizer

LANGUAGE = "english"

SUMMARIZERS = {
    "lexrank": (LexRankSummarizer, "lexrank_summ.txt"),
    "concept": (ConceptSummarizer, "concept_summ.txt"),
}


class LegacyTokenizer(Tokenizer):
    """Tokenizer with the word filter of sumy 0.4.1, used for the thesis.

    Only tokens made entirely of letters count as words, so "segunda-feira"
    or "porta-voz" are dropped. Newer sumy versions keep them.
    """

    _WORD_PATTERN = re.compile(r"^[^\W\d_]+$", re.UNICODE)

    @staticmethod
    def _is_word(word):
        return bool(LegacyTokenizer._WORD_PATTERN.search(word))


def sentences_count(cluster_dir):
    text = (cluster_dir / "sumario_automatico_CSTSumm.txt").read_text(encoding="latin-1")
    return text.count(".")


def select_by_word_budget(sentences, ratings, word_budget):
    """Take sentences from the highest rated down until `word_budget` words,
    cutting the last one taken to fit, and return them in document order."""
    by_rating = sorted(range(len(sentences)), key=lambda i: ratings[sentences[i]], reverse=True)
    chosen = {}
    remaining = word_budget
    for i in by_rating:
        if remaining <= 0:
            break
        words = str(sentences[i]).split()
        chosen[i] = " ".join(words[:remaining])
        remaining -= len(words)
    return [chosen[i] for i in sorted(chosen)]


def select_mmr(sentences, scores, similarities, word_budget, mmr_lambda):
    """Maximal Marginal Relevance under a word budget.

    Repeatedly takes the sentence maximizing
    mmr_lambda * score / max(scores) - (1 - mmr_lambda) * (highest similarity
    to a sentence already taken), cutting the last one to fit the budget.
    Returns the sentences in document order.
    """
    top = max(scores) or 1
    candidates = list(range(len(sentences)))
    chosen = {}
    remaining = word_budget

    def mmr(i):
        redundancy = max((similarities[i][j] for j in chosen), default=0)
        return mmr_lambda * scores[i] / top - (1 - mmr_lambda) * redundancy

    while remaining > 0 and candidates:
        best = max(candidates, key=mmr)
        candidates.remove(best)
        words = str(sentences[best]).split()
        chosen[best] = " ".join(words[:remaining])
        remaining -= len(words)
    return [chosen[i] for i in sorted(chosen)]


def summarize_cluster(cluster_dir, summarizer_cls, language=LANGUAGE, tokenizer_cls=LegacyTokenizer,
                      tokenizer_language=None, stop_words=None, word_budget=None, text=None,
                      sentences=None, mmr_lambda=None):
    """`language` sets the stemmer and, unless `stop_words` is given, sumy's
    stop words; `tokenizer_language`, which defaults to it, sets sentence and
    word splitting. Without `word_budget`, the summary has as many sentences as
    there are '.' in the CSTSumm summary, as in the thesis. `text` replaces
    the cluster's original.txt as input, and `sentences` replaces it with
    sentences that are already split. `mmr_lambda` (with a word budget)
    selects sentences with MMR instead of by score alone."""
    tokenizer = tokenizer_cls(tokenizer_language or language)
    if sentences is not None:
        document = ObjectDocumentModel([Paragraph([Sentence(s, tokenizer) for s in sentences])])
    elif text is not None:
        document = PlaintextParser.from_string(text, tokenizer).document
    else:
        document = PlaintextParser.from_file(cluster_dir / "original.txt", tokenizer).document
    summarizer = summarizer_cls(Stemmer(language))
    summarizer.stop_words = get_stop_words(language) if stop_words is None else stop_words
    if word_budget is None:
        chosen = summarizer(document, sentences_count(cluster_dir))
        return "".join(str(sentence) for sentence in chosen)
    if mmr_lambda is not None:
        scores, similarities = summarizer.scores_and_similarities(document)
        return "".join(select_mmr(document.sentences, scores, similarities, word_budget, mmr_lambda))
    ratings = summarizer.rate_sentences(document)
    return "".join(select_by_word_budget(document.sentences, ratings, word_budget))


def summarize_corpus(experiments_dir, out_dir, system):
    summarizer_cls, filename = SUMMARIZERS[system]
    for cluster_dir in sorted(Path(experiments_dir).iterdir()):
        if not (cluster_dir / "original.txt").exists():
            continue
        target = Path(out_dir) / cluster_dir.name
        target.mkdir(parents=True, exist_ok=True)
        (target / filename).write_text(summarize_cluster(cluster_dir, summarizer_cls), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("system", choices=SUMMARIZERS)
    parser.add_argument("experiments_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    summarize_corpus(args.experiments_dir, args.out_dir, args.system)


if __name__ == "__main__":
    main()
