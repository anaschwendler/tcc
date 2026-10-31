# Analysis

Further analysis of the corrected pipeline from
[results/fixes/](../fixes/README.md): same setting (corpus sentences without
titles, hyphenated words kept, Portuguese stemming and stop words, word budget
from the human extract), word-level ROUGE against the human extract, and
paired Wilcoxon tests over the 50 clusters.

```sh
uv run python results/analysis/<script>.py
```

## Baselines

`baselines.py` adds two baselines:

- **Lead**: the opening sentences of each text, in turns (first sentence of
  every text, then the second of every text, ...) until the word budget.
- **Random**: sentences in random order until the word budget, averaged over 10
  seeds per cluster.

| System | Words | ROUGE-1 R | ROUGE-2 R | ROUGE-1 F | ROUGE-2 F |
|---|---|---|---|---|---|
| LexRank | 190.1 | 0.569 | 0.364 | 0.570 | 0.365 |
| ConceptRank | 190.4 | 0.579 | 0.376 | 0.579 | 0.377 |
| ConceptRank (thesis similarity) | 190.0 | 0.581 | 0.382 | 0.583 | 0.383 |
| CSTSumm | 144.8 | 0.505 | 0.343 | 0.562 | 0.385 |
| Lead | 191.3 | 0.587 | 0.404 | 0.586 | 0.404 |
| Random | 190.9 | 0.514 | 0.286 | 0.515 | 0.287 |

Word counts use the ROUGE tokenizer, which splits hyphenated words, so they
run slightly above the budget, which counts whitespace-separated words.

| Comparison | Metric | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|
| ConceptRank vs Lead | ROUGE-1 R | -0.008 | 23 / 24 | 0.619 |
| ConceptRank vs Lead | ROUGE-2 R | -0.028 | 20 / 29 | 0.159 |
| ConceptRank vs Lead | ROUGE-1 F | -0.007 | 24 / 26 | 0.653 |
| ConceptRank vs Lead | ROUGE-2 F | -0.027 | 21 / 29 | 0.175 |
| LexRank vs Lead | ROUGE-1 R | -0.018 | 22 / 28 | 0.415 |
| LexRank vs Lead | ROUGE-2 R | -0.040 | 21 / 29 | 0.114 |
| LexRank vs Lead | ROUGE-1 F | -0.016 | 22 / 28 | 0.438 |
| LexRank vs Lead | ROUGE-2 F | -0.039 | 21 / 29 | 0.128 |
| ConceptRank vs Random | ROUGE-1 R | +0.065 | 38 / 11 | 0.000 |
| ConceptRank vs Random | ROUGE-2 R | +0.090 | 39 / 11 | 0.000 |
| ConceptRank vs Random | ROUGE-1 F | +0.064 | 39 / 11 | 0.000 |
| ConceptRank vs Random | ROUGE-2 F | +0.090 | 39 / 11 | 0.000 |
| LexRank vs Random | ROUGE-1 R | +0.055 | 38 / 11 | 0.000 |
| LexRank vs Random | ROUGE-2 R | +0.078 | 39 / 11 | 0.000 |
| LexRank vs Random | ROUGE-1 F | +0.055 | 38 / 12 | 0.000 |
| LexRank vs Random | ROUGE-2 F | +0.078 | 39 / 11 | 0.000 |
| Lead vs CSTSumm | ROUGE-1 R | +0.082 | 37 / 13 | 0.000 |
| Lead vs CSTSumm | ROUGE-2 R | +0.061 | 32 / 18 | 0.015 |
| Lead vs CSTSumm | ROUGE-1 F | +0.025 | 29 / 21 | 0.133 |
| Lead vs CSTSumm | ROUGE-2 F | +0.019 | 27 / 23 | 0.527 |

Both graph-based systems are clearly better than random, so centrality does
pick informative sentences. But Lead scores highest on average, and neither
LexRank nor ConceptRank beats it; the gap (0.01 to 0.04) is not significant.
This is common for news, where the opening sentences already summarize the
event.

## Redundancy removal (MMR)

`mmr.py` selects sentences with Maximal Marginal Relevance: each step takes the
sentence that maximizes λ · score / max score − (1 − λ) · its highest
similarity to a sentence already taken, until the word budget. Each system uses
its own similarity (TF-IDF cosine for LexRank, WIVES for ConceptRank) to
measure redundancy. λ = 0.7 was fixed before looking at results. LexRank and
ConceptRank 44 summaries changed.

| System | Metric | Without MMR | With MMR | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.569 | 0.568 | -0.001 | 20 / 19 | 0.769 |
| LexRank | ROUGE-2 R | 0.364 | 0.356 | -0.008 | 14 / 24 | 0.328 |
| LexRank | ROUGE-1 F | 0.570 | 0.569 | -0.001 | 21 / 21 | 0.759 |
| LexRank | ROUGE-2 F | 0.365 | 0.357 | -0.008 | 16 / 25 | 0.285 |
| ConceptRank | ROUGE-1 R | 0.579 | 0.579 | -0.000 | 21 / 20 | 0.964 |
| ConceptRank | ROUGE-2 R | 0.376 | 0.366 | -0.010 | 19 / 20 | 0.586 |
| ConceptRank | ROUGE-1 F | 0.579 | 0.580 | +0.000 | 22 / 21 | 0.952 |
| ConceptRank | ROUGE-2 F | 0.377 | 0.367 | -0.010 | 22 / 20 | 0.639 |

With MMR, against Lead:

| Comparison | Metric | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|
| LexRank + MMR vs Lead | ROUGE-1 R | -0.019 | 21 / 28 | 0.332 |
| LexRank + MMR vs Lead | ROUGE-2 R | -0.048 | 21 / 29 | 0.082 |
| LexRank + MMR vs Lead | ROUGE-1 F | -0.017 | 22 / 28 | 0.404 |
| LexRank + MMR vs Lead | ROUGE-2 F | -0.047 | 21 / 29 | 0.093 |
| ConceptRank + MMR vs Lead | ROUGE-1 R | -0.009 | 25 / 23 | 0.704 |
| ConceptRank + MMR vs Lead | ROUGE-2 R | -0.038 | 21 / 28 | 0.086 |
| ConceptRank + MMR vs Lead | ROUGE-1 F | -0.007 | 27 / 23 | 0.811 |
| ConceptRank + MMR vs Lead | ROUGE-2 F | -0.037 | 22 / 28 | 0.099 |

Other values of λ, for reference only (chosen and reported on the same 50
clusters), ROUGE-1 R / ROUGE-2 R:

| λ | LexRank | ConceptRank |
|---|---|---|
| 0.5 | 0.559 / 0.336 | 0.565 / 0.344 |
| 0.6 | 0.564 / 0.345 | 0.569 / 0.346 |
| 0.7 | 0.568 / 0.356 | 0.579 / 0.366 |
| 0.8 | 0.561 / 0.346 | 0.583 / 0.375 |
| 0.9 | 0.566 / 0.353 | 0.578 / 0.369 |

MMR makes no measurable difference for either system at any λ tried, and Lead
stays ahead of both. One possible reason, not tested: the reference is a human
extract made of source sentences, and if annotators also picked information
repeated across the news agencies, penalizing repetition does not bring a
summary closer to it.
