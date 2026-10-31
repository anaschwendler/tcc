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

Summary length turned out to confound most fixes: with a fixed number of
sentences, a change that makes the chosen sentences shorter lowers recall and
raises precision. So the main comparison puts both sides on the same **word
budget** (the word count of the cluster's human extract, see below); the
comparison with the thesis' fixed sentence count is printed too, for reference.

The baseline is the ported code, not the 2016 files: ConceptRank now iterates
words in sorted order, so its baseline differs slightly from the thesis
summaries (ROUGE-1 R 0.540 against 0.546).

```sh
uv run python results/fixes/<fix>.py
```

Needs the raw corpus in `data/raw/CSTNews/` (see [data/README.md](../../data/README.md)).

## Summary

Main comparison, both sides on the word budget (diffs over ROUGE-1/2 recall
and F):

| Fix | Script | LexRank | ConceptRank |
|---|---|---|---|
| Keep hyphenated words | `hyphens.py` | +0.011 to +0.018, p ≤ 0.033 on all 4 metrics | +0.008 to +0.014, p ≤ 0.017 on all 4 metrics |
| Titles not ranked as sentences | `titles.py` | +0.027 to +0.037, p ≤ 0.004 on all 4 metrics | +0.010 to +0.019, p ≤ 0.047 on all 4 metrics |
| Corpus sentence segmentation (both without titles) | `segmentation.py` | −0.003 to +0.002, not significant | −0.008 to −0.005, not significant |
| WIVES weights as in the Java original (ConceptRank only) | `wives.py` | — | −0.018 to −0.008, not significant |
| Portuguese stemmer and stop words | `portuguese.py` | +0.013 to +0.020, not significant | +0.003 to +0.004, not significant |

The word budget itself, against the thesis' fixed sentence count:

| Fix | Script | LexRank | ConceptRank |
|---|---|---|---|
| Word budget from the human extract | `length.py` | ROUGE-1 F +0.028 (p = 0.007); others +0.011 to +0.026, not significant | ROUGE-1 F +0.036 (p < 0.001); others +0.008 to +0.024, not significant |

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

That table uses the thesis' fixed sentence count. With both sides on the word
budget (LexRank 34 and ConceptRank 22 summaries changed):

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.549 | 0.560 | +0.011 | 20 / 9 | 0.027 |
| LexRank | ROUGE-2 R | 0.328 | 0.345 | +0.018 | 19 / 7 | 0.026 |
| LexRank | ROUGE-1 F | 0.549 | 0.560 | +0.011 | 21 / 11 | 0.033 |
| LexRank | ROUGE-2 F | 0.328 | 0.345 | +0.018 | 20 / 12 | 0.032 |
| ConceptRank | ROUGE-1 R | 0.563 | 0.571 | +0.008 | 14 / 7 | 0.013 |
| ConceptRank | ROUGE-2 R | 0.345 | 0.359 | +0.014 | 14 / 3 | 0.009 |
| ConceptRank | ROUGE-1 F | 0.563 | 0.571 | +0.008 | 14 / 8 | 0.017 |
| ConceptRank | ROUGE-2 F | 0.345 | 0.358 | +0.014 | 14 / 5 | 0.009 |

Keeping hyphenated words helps both systems. With a fixed sentence count the
gain is consistent only for ConceptRank; with equal length it is significant on
every metric for both.

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

With both sides on the word budget (see above), so that length is equal:

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.549 | 0.563 | +0.014 | 26 / 23 | 0.251 |
| LexRank | ROUGE-2 R | 0.328 | 0.348 | +0.020 | 26 / 22 | 0.338 |
| LexRank | ROUGE-1 F | 0.549 | 0.563 | +0.013 | 26 / 23 | 0.280 |
| LexRank | ROUGE-2 F | 0.328 | 0.348 | +0.020 | 27 / 22 | 0.342 |
| ConceptRank | ROUGE-1 R | 0.563 | 0.567 | +0.004 | 22 / 23 | 0.773 |
| ConceptRank | ROUGE-2 R | 0.345 | 0.349 | +0.003 | 24 / 20 | 0.825 |
| ConceptRank | ROUGE-1 F | 0.563 | 0.567 | +0.004 | 22 / 24 | 0.789 |
| ConceptRank | ROUGE-2 F | 0.345 | 0.348 | +0.004 | 25 / 21 | 0.772 |

The earlier drop came from length. With equal length, Portuguese stemming and
stop words lean positive for LexRank and make no difference for ConceptRank,
but neither change is significant over 50 clusters.

## Titles not ranked as sentences

The thesis built `original.txt` from every file in `Textos-fonte`, including
the `*_titulo.txt` files. Those hold the headline, sometimes a subheadline, and
in some clusters hundreds of padding spaces. Headlines have no full stop, so
they were glued to the first sentence of the next text. The variant removes the
content of every title file from `original.txt`, keeping order and joins
otherwise identical. C29 and C47 each have two texts with the same title; both
copies are removed.

With a fixed sentence count the variant's summaries are shorter (LexRank 176.8
→ 157.8 words, ConceptRank 189.3 → 176.3), so recall drops while F rises. With
both sides on the word budget (LexRank 46 and ConceptRank 44 summaries
changed):

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.549 | 0.576 | +0.027 | 30 / 14 | 0.001 |
| LexRank | ROUGE-2 R | 0.328 | 0.365 | +0.037 | 28 / 16 | 0.004 |
| LexRank | ROUGE-1 F | 0.549 | 0.577 | +0.028 | 32 / 13 | 0.001 |
| LexRank | ROUGE-2 F | 0.328 | 0.365 | +0.037 | 29 / 16 | 0.003 |
| ConceptRank | ROUGE-1 R | 0.563 | 0.573 | +0.010 | 26 / 12 | 0.036 |
| ConceptRank | ROUGE-2 R | 0.345 | 0.364 | +0.019 | 25 / 16 | 0.047 |
| ConceptRank | ROUGE-1 F | 0.563 | 0.573 | +0.011 | 28 / 13 | 0.031 |
| ConceptRank | ROUGE-2 F | 0.345 | 0.364 | +0.019 | 27 / 16 | 0.040 |

Removing titles helps both systems on all metrics, LexRank more than
ConceptRank; without titles the two are almost level (ROUGE-1 R 0.576 and
0.573). The script also prints the fixed-sentence-count comparison.

## Corpus sentence segmentation

The thesis split sentences with sumy's tokenizer (NLTK punkt, English model).
The corpus ships its own segmentation in "Textos-fonte segmentados", which
`conceptrank.corpus` loads; those files are also a revised copy of the texts
(datelines such as "RIO -", a few quotes and full stops fixed). Since that
segmentation leaves titles out, both sides here use text without titles, so
only segmentation changes. punkt finds 2225 sentences in the 50 clusters, the
corpus segmentation 2081. Both sides on the word budget; LexRank and
ConceptRank 49 summaries changed.

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank | ROUGE-1 R | 0.576 | 0.573 | -0.003 | 21 / 22 | 0.772 |
| LexRank | ROUGE-2 R | 0.365 | 0.366 | +0.001 | 21 / 22 | 0.655 |
| LexRank | ROUGE-1 F | 0.577 | 0.574 | -0.002 | 22 / 22 | 0.870 |
| LexRank | ROUGE-2 F | 0.365 | 0.367 | +0.002 | 22 / 23 | 0.773 |
| ConceptRank | ROUGE-1 R | 0.573 | 0.567 | -0.006 | 9 / 21 | 0.057 |
| ConceptRank | ROUGE-2 R | 0.364 | 0.356 | -0.008 | 14 / 21 | 0.461 |
| ConceptRank | ROUGE-1 F | 0.573 | 0.568 | -0.005 | 14 / 23 | 0.102 |
| ConceptRank | ROUGE-2 F | 0.364 | 0.356 | -0.008 | 19 / 22 | 0.496 |

Segmentation makes no measurable difference. The corpus segmentation is still
the cleaner input, but ROUGE does not tell the two apart.

## WIVES weights as in the Java original

ConceptRank's similarity was ported from the WIVES similarity (Loh et al.),
`docs/reference/wives_similarity.java`. There, each word the two sentences
share is weighted by its weight in each sentence, a value between 0 and 1.
The thesis port used the word's length (`len(term)`) as a running maximum
instead, with the minimum stuck at 0. The variant, `WivesSummarizer`, follows
the Java formula with the normalized term frequency (tf / max tf in the
sentence) as the weight, since the Java class that defined the weight is not
in the repository. It also counts distinct words in the denominator, as the
Java bag of words did. Only ConceptRank changes; both sides on the word budget;
all 50 summaries changed.

| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| ConceptRank | ROUGE-1 R | 0.563 | 0.554 | -0.009 | 22 / 27 | 0.547 |
| ConceptRank | ROUGE-2 R | 0.345 | 0.327 | -0.018 | 22 / 26 | 0.415 |
| ConceptRank | ROUGE-1 F | 0.563 | 0.555 | -0.008 | 22 / 28 | 0.566 |
| ConceptRank | ROUGE-2 F | 0.345 | 0.327 | -0.018 | 22 / 27 | 0.423 |

The fixed ConceptRank against LexRank, both on the word budget:

| Comparison | Metric | LexRank | ConceptRank (fixed) | Diff | ConceptRank better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| LexRank vs ConceptRank | ROUGE-1 R | 0.549 | 0.554 | +0.005 | 28 / 22 | 0.566 |
| LexRank vs ConceptRank | ROUGE-2 R | 0.328 | 0.327 | -0.000 | 25 / 24 | 0.846 |
| LexRank vs ConceptRank | ROUGE-1 F | 0.549 | 0.555 | +0.005 | 28 / 22 | 0.559 |
| LexRank vs ConceptRank | ROUGE-2 F | 0.328 | 0.327 | -0.000 | 25 / 24 | 0.854 |

Fixing the weights does not help: the thesis port did slightly, not
significantly, better, and the fixed ConceptRank is level with LexRank. With
term-frequency weights most words in a sentence weigh 1, so WIVES behaves much
like a Jaccard overlap of stemmed words, close to LexRank's cosine. Note that
the "concepts" were always stemmed words: the rule-based categorization of
Loh et al. described in the thesis (cue terms, synonyms, weighted rules) was
never implemented.
