"""Fix: summary length set by a word budget.

Baseline: as many sentences as there are '.' in the CSTSumm summary, as in the
thesis ("1.5" or "Jr." count as sentence ends, and word length is not
controlled).
Variant: the word count of the cluster's human extract. Sentences are taken by
rating until the budget is reached and the last one taken is cut to fit, as
ROUGE's length limit (-l) would.

    uv run python results/fixes/length.py
"""

from common import (changed_summaries, mean_words, print_comparison, reference_word_counts,
                    references, score_all, summarize_all)

if __name__ == "__main__":
    refs = references()
    baseline = summarize_all()
    variant = summarize_all(word_budgets=reference_word_counts(refs))
    print("Summaries changed:", changed_summaries(baseline, variant))
    print("Mean length in words: reference", mean_words(refs),
          "| baseline", {s: mean_words(t) for s, t in baseline.items()},
          "| variant", {s: mean_words(t) for s, t in variant.items()}, "\n")
    print_comparison(score_all(baseline, refs), score_all(variant, refs))
