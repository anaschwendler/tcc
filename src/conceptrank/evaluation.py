"""ROUGE for Portuguese summaries, scored against the CSTNews human extract.

Tokenizers:

- "portuguese" (default): words, keeping accented letters.
- "rouge155": rouge-score's default, which follows the original ROUGE-1.5.5
  script: it lowercases and replaces everything outside [a-z0-9] with spaces,
  so "ação" becomes the tokens "a" and "o".
- "thesis2016": one token per [a-z0-9] character. The thesis called pyrouge's
  score_summary() with plain strings, and pyrouge iterated over them as if
  they were lists of sentences, so ROUGE-1.5.5 scored character n-grams. This
  reproduces the 2016 scores exactly.

ROUGE-SU4, reported in the thesis, is not available in rouge-score.

    uv run python -m conceptrank.evaluation runs/lexrank lexrank_summ.txt runs/lexrank.csv
"""

import argparse
import csv
import re
import unicodedata
from pathlib import Path

from rouge_score import rouge_scorer, tokenizers

from conceptrank.corpus import load_corpus

ROUGE_TYPES = ("rouge1", "rouge2", "rouge3", "rouge4", "rougeL")


class PortugueseTokenizer(tokenizers.Tokenizer):
    _WORD = re.compile(r"[^\W_]+")

    def tokenize(self, text):
        return self._WORD.findall(unicodedata.normalize("NFC", text).lower())


class Thesis2016Tokenizer(tokenizers.Tokenizer):
    _CHAR = re.compile(r"[a-z0-9]")

    def tokenize(self, text):
        return self._CHAR.findall(text.lower())


TOKENIZERS = {
    "portuguese": PortugueseTokenizer(),
    "rouge155": None,
    "thesis2016": Thesis2016Tokenizer(),
}


def score(summary, reference, tokenizer="portuguese"):
    scorer = rouge_scorer.RougeScorer(ROUGE_TYPES, tokenizer=TOKENIZERS[tokenizer])
    return scorer.score(reference, summary)


def reference_text(cluster):
    return "\n".join(e.text for e in cluster.human_extract)


def evaluate(summaries, references, tokenizer="portuguese"):
    """Score {cluster_id: summary} against {cluster_id: reference}, one row per metric."""
    rows = []
    for cluster_id, summary in summaries.items():
        for metric, s in score(summary, references[cluster_id], tokenizer).items():
            rows.append({
                "cluster": cluster_id,
                "metric": metric,
                "precision": s.precision,
                "recall": s.recall,
                "f": s.fmeasure,
            })
    return rows


def read_summaries(summaries_dir, filename):
    """Read <summaries_dir>/<cluster folder>/<filename>, keyed by cluster id ("C1")."""
    summaries = {}
    for cluster_dir in sorted(Path(summaries_dir).iterdir()):
        path = cluster_dir / filename
        if path.exists():
            summaries[cluster_dir.name.split("_")[0]] = path.read_text(encoding="utf-8")
    return summaries


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cluster", "metric", "precision", "recall", "f"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("summaries_dir", type=Path)
    parser.add_argument("filename")
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("--tokenizer", choices=TOKENIZERS, default="portuguese")
    args = parser.parse_args()
    references = {c.id: reference_text(c) for c in load_corpus()}
    summaries = read_summaries(args.summaries_dir, args.filename)
    write_csv(evaluate(summaries, references, args.tokenizer), args.out_csv)


if __name__ == "__main__":
    main()
