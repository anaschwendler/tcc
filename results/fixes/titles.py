"""Fix: do not rank titles as sentences.

Baseline: original.txt, which concatenates every file in "Textos-fonte",
titles included, with no separator.
Variant: the same original.txt with the content of every *_titulo.txt file
removed, so order and joins between texts stay the same. Two clusters (C29,
C47) have two texts with the same title; both copies are removed.

    uv run python results/fixes/titles.py
"""

from conceptrank.corpus import load_corpus

from common import (ARCHIVE, changed_summaries, mean_words, print_comparison, reference_word_counts,
                    references, score_all, summarize_all)


def texts_without_titles():
    raw = {c.id: c.path for c in load_corpus()}
    texts = {}
    for cluster_dir in ARCHIVE.iterdir():
        cluster_id = cluster_dir.name.split("_")[0]
        text = (cluster_dir / "original.txt").read_bytes()
        for title in (raw[cluster_id] / "Textos-fonte").glob("*_titulo.txt"):
            text = text.replace(title.read_bytes(), b"")
        texts[cluster_id] = text.decode("utf-8")
    return texts


def compare(title, baseline, variant, refs):
    print(f"\n### {title}\n")
    print("Summaries changed:", changed_summaries(baseline, variant))
    print("Mean length in words: baseline", {s: mean_words(t) for s, t in baseline.items()},
          "| variant", {s: mean_words(t) for s, t in variant.items()}, "\n")
    print_comparison(score_all(baseline, refs), score_all(variant, refs))


if __name__ == "__main__":
    refs = references()
    texts = texts_without_titles()
    compare("Fixed sentence count", summarize_all(), summarize_all(texts=texts), refs)
    budgets = reference_word_counts(refs)
    compare("Both with the word budget", summarize_all(word_budgets=budgets),
            summarize_all(word_budgets=budgets, texts=texts), refs)
