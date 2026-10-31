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
