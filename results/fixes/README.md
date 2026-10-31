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
