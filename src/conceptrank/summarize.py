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


def summarize_cluster(cluster_dir, summarizer_cls, language=LANGUAGE, tokenizer_cls=LegacyTokenizer,
                      tokenizer_language=None, stop_words=None):
    """`language` sets the stemmer and, unless `stop_words` is given, sumy's
    stop words; `tokenizer_language`, which defaults to it, sets sentence and
    word splitting."""
    tokenizer = tokenizer_cls(tokenizer_language or language)
    parser = PlaintextParser.from_file(cluster_dir / "original.txt", tokenizer)
    summarizer = summarizer_cls(Stemmer(language))
    summarizer.stop_words = get_stop_words(language) if stop_words is None else stop_words
    sentences = summarizer(parser.document, sentences_count(cluster_dir))
    return "".join(str(sentence) for sentence in sentences)


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
