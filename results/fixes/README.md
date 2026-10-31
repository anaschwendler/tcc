# Fixes to the thesis pipeline

Each known issue in [results/legacy/](../legacy/README.md) is fixed and
measured on its own, one script per fix.

**Method.** Every script summarizes the 50 CSTNews clusters twice with the
ported thesis code (`conceptrank.summarize`): a baseline and a variant that
changes one thing. Both are scored with word-level ROUGE (Portuguese
tokenizer) against the human extract without source tags, and compared with
paired Wilcoxon signed-rank tests. "Better / worse" counts the clusters whose
score went up or down. Each script runs 8 tests (2 systems × 4 metrics), so a
single p-value near 0.05 is weak evidence on its own.

The baseline is the ported code, not the 2016 files: ConceptRank now iterates
words in sorted order, so its baseline differs slightly from the thesis
summaries (ROUGE-1 R 0.540 against 0.546).

```sh
uv run python results/fixes/<fix>.py
```

Needs the raw corpus in `data/raw/CSTNews/` (see [data/README.md](../../data/README.md)).

## Summary

| Fix | Script | LexRank | ConceptRank |
|---|---|---|---|
| Keep hyphenated words | `hyphens.py` | +0.005 to +0.016, not significant | +0.012 to +0.019, p ≤ 0.049 on all 4 metrics |
| Word budget from the human extract | `length.py` | ROUGE-1 F +0.028 (p = 0.007); others +0.011 to +0.026, not significant | ROUGE-1 F +0.036 (p < 0.001); others +0.008 to +0.024, not significant |
| Portuguese stemmer and stop words | `portuguese.py` | −0.030 to −0.007, not significant; summaries 6.6% shorter | −0.006 to +0.002, not significant; summaries 4.8% shorter |

## Keep hyphenated words

The thesis used sumy 0.4.1, whose tokenizer dropped every hyphenated word
("segunda-feira", "porta-voz", "vice-presidente"), so they never counted
towards sentence similarity. The variant uses sumy's current tokenizer, which
keeps them. Summaries changed: LexRank 26, ConceptRank 18.

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.523 | 0.527 | +0.005 | 13 / 12 | 0.563 |
| LexRank | ROUGE-2 R | 0.315 | 0.330 | +0.016 | 12 / 11 | 0.162 |
| LexRank | ROUGE-1 F | 0.522 | 0.528 | +0.006 | 12 / 14 | 0.534 |
| LexRank | ROUGE-2 F | 0.316 | 0.333 | +0.016 | 17 / 9 | 0.137 |
| ConceptRank | ROUGE-1 R | 0.540 | 0.552 | +0.012 | 10 / 6 | 0.034 |
| ConceptRank | ROUGE-2 R | 0.337 | 0.356 | +0.019 | 10 / 6 | 0.049 |
| ConceptRank | ROUGE-1 F | 0.527 | 0.538 | +0.012 | 15 / 3 | 0.006 |
| ConceptRank | ROUGE-2 F | 0.330 | 0.347 | +0.018 | 12 / 6 | 0.028 |

Keeping hyphenated words helps both systems on average; the gain is
consistent for ConceptRank and within noise for LexRank.

## Word budget from the human extract

The thesis gave each summary as many sentences as there are '.' characters in
the CSTSumm summary of the cluster, which miscounts sentences ("1.5", "Jr.")
and leaves the number of words free. The variant uses the word count of the
cluster's human extract as a budget: sentences are taken by rating until it is
reached, the last one taken is cut to fit (like ROUGE's `-l` option), and the
summary keeps document order. Summaries changed: all 50 for both systems.

Mean length in words: reference 190.6; baseline LexRank 176.8, ConceptRank
189.3; variant LexRank 190.5, ConceptRank 190.8.

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.523 | 0.549 | +0.026 | 29 / 20 | 0.110 |
| LexRank | ROUGE-2 R | 0.315 | 0.328 | +0.013 | 26 / 17 | 0.134 |
| LexRank | ROUGE-1 F | 0.522 | 0.549 | +0.028 | 33 / 17 | 0.007 |
| LexRank | ROUGE-2 F | 0.316 | 0.328 | +0.011 | 29 / 21 | 0.184 |
| ConceptRank | ROUGE-1 R | 0.540 | 0.563 | +0.024 | 27 / 23 | 0.372 |
| ConceptRank | ROUGE-2 R | 0.337 | 0.345 | +0.008 | 24 / 21 | 0.808 |
| ConceptRank | ROUGE-1 F | 0.527 | 0.563 | +0.036 | 35 / 15 | 0.000 |
| ConceptRank | ROUGE-2 F | 0.330 | 0.345 | +0.015 | 25 / 25 | 0.337 |

Matching the reference length improves ROUGE-1 F significantly for both
systems. It also removes length as a confounder, so later comparisons are
fairer.

## Portuguese stemmer and stop words

The thesis used the English Snowball stemmer and sumy's English stop words on
Portuguese text. The variant uses the Portuguese Snowball stemmer and NLTK's
Portuguese stop words; sentence and word splitting stay English so that only
these two change. Needs `uv run python -c "import nltk; nltk.download('stopwords')"`.

sumy's own Portuguese stop word list is broken: 36 of its 195 entries are
stored as literal escapes (`n\xe3o` instead of `não`), so "não", "já", "são",
"há" and "você" are never removed, and a few entries are two words joined by a
comma. The script also runs it, for reference; its results are similar.

Summaries changed: LexRank 50, ConceptRank 49.

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.523 | 0.492 | -0.030 | 17 / 30 | 0.079 |
| LexRank | ROUGE-2 R | 0.315 | 0.303 | -0.011 | 24 / 26 | 0.598 |
| LexRank | ROUGE-1 F | 0.522 | 0.505 | -0.017 | 22 / 28 | 0.282 |
| LexRank | ROUGE-2 F | 0.316 | 0.310 | -0.007 | 28 / 22 | 0.878 |
| ConceptRank | ROUGE-1 R | 0.540 | 0.533 | -0.006 | 21 / 27 | 0.418 |
| ConceptRank | ROUGE-2 R | 0.337 | 0.337 | +0.000 | 22 / 24 | 0.823 |
| ConceptRank | ROUGE-1 F | 0.527 | 0.528 | +0.001 | 23 / 26 | 0.972 |
| ConceptRank | ROUGE-2 F | 0.330 | 0.331 | +0.002 | 25 / 24 | 0.784 |

Almost every summary changes, but quality does not measurably improve. The
change is confounded with summary length: the number of sentences is fixed,
and the variant picks shorter ones (LexRank 176.8 → 165.1 words on average,
ConceptRank 189.3 → 180.2), which lowers recall while F-scores hold. This
should be measured again once summary length is fixed by a word budget.
