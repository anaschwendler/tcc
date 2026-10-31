"""Summarize every CSTNews cluster the way the thesis did.

Ported from the corpus loops in src/BetaRank.ipynb and src/ConceptRank.ipynb.
The legacy choices are kept so the output can be compared with
output/experiments/: English tokenizer, stemmer and stop words; summary length
taken from the number of '.' in the CSTSumm summary; sentences written with no
separator.

    uv run python -m conceptrank.summarize lexrank output/experiments runs/legacy
"""

import argparse
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


def sentences_count(cluster_dir):
    text = (cluster_dir / "sumario_automatico_CSTSumm.txt").read_text(encoding="latin-1")
    return text.count(".")


def summarize_cluster(cluster_dir, summarizer_cls, language=LANGUAGE):
    parser = PlaintextParser.from_file(cluster_dir / "original.txt", Tokenizer(language))
    summarizer = summarizer_cls(Stemmer(language))
    summarizer.stop_words = get_stop_words(language)
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
