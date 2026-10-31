# Legacy results (2017)

These are the results reported in the thesis, frozen as they were on
2017-07-07. They are kept as a baseline: every fix made during the refactor
should be measured against these numbers. **Do not regenerate or edit them.**

> **These scores are character n-gram overlaps, not word-level ROUGE.** The
> scoring code handed plain strings to a function that expected lists of
> sentences, so ROUGE-1 compared letters and ROUGE-2 pairs of letters. See
> [Re-scored at word level](#re-scored-at-word-level) for what the same
> summaries score with standard ROUGE.

## How they were produced

1. `archive/read_archives.py` and `archive/extract_files.py` copied source texts, human
   extracts and CSTSumm summaries from CSTNews into `archive/experiments_2016/`.
2. `archive/BetaRank.ipynb` (LexRank) and `archive/ConceptRank.ipynb` wrote
   `lexrank_summ.txt` and `concept_summ.txt` for each cluster, with the
   number of sentences taken from the CSTSumm summary.
3. `archive/rouge.ipynb` scored each summary against `extrato_humano.txt` with
   `pyrouge` (ROUGE-1.5.5, Python 2) and wrote `rouge_*.txt`.
4. `results_by_n_words.ipynb` collected the `rouge_*.txt` files into the CSVs
   and plotted the analyses by text length and type-token ratio.
5. `barchartexample.ipynb` read the CSVs and plotted the mean ± std bars in
   `average-total.png`.

## Files

| File | Content |
|---|---|
| `lexrank_results.csv`, `concept_results.csv`, `CSTSumm_results.csv` | ROUGE-1/2/3/4/SU4 precision, recall and F per cluster |
| `average-total.png`, `rouge2-recall.png`, `rouge3-*.png` | Figures used in the top-level README |
| `results_by_n_words.ipynb` | Analysis notebook (see known issues) |
| `barchartexample.ipynb` | Mean ± std bar chart (`average-total.png`) |

The CSVs have no cluster column. Row *i* is the same cluster in all three
files (rows follow `os.walk` order: C16, C6, C29, C20, …). Every row matches
exactly one `archive/experiments_2016/<cluster>/rouge_*.txt` file.

## Summary as reported (character n-grams; mean ± std over 50 clusters)

| System | ROUGE-1 R | ROUGE-2 R | ROUGE-3 R | ROUGE-SU4 F |
|---|---|---|---|---|
| LexRank | 0.7546 ± 0.1863 | 0.6452 ± 0.1443 | 0.4757 ± 0.1229 | 0.7390 ± 0.0875 |
| ConceptRank | 0.7744 ± 0.1830 | 0.6640 ± 0.1513 | 0.5016 ± 0.1351 | 0.7401 ± 0.0885 |
| CSTSumm | 0.6987 ± 0.1680 | 0.6043 ± 0.1207 | 0.4646 ± 0.1005 | 0.7453 ± 0.0837 |

## Known issues

Unless noted, these come from reading the code and have not been measured.

- **ROUGE was computed on characters.** `rouge.ipynb` called
  `Rouge155.score_summary(summary_text, {'A': reference_text})` from
  [andersjo/pyrouge](https://github.com/andersjo/pyrouge). That function
  expects each text as a list of sentences and writes one ROUGE "sentence" per
  item, so iterating over a string wrote one character per sentence.
  ROUGE-1.5.5 then kept only `[a-z0-9]`. *Measured:* the `thesis2016`
  tokenizer in `src/conceptrank/evaluation.py` reproduces 149 of the 150
  archived scores within 2e-5 (`tests/test_thesis_rouge.py`); the exception is
  C49 (see below).
- Stemmer and stop words are English (`LANGUAGE = "english"`).
- Hyphenated words ("segunda-feira", "porta-voz", "vice-presidente") were
  dropped by the tokenizer, so they never counted towards similarity (see
  below).
- All system summaries were decoded as Latin-1 before scoring, although most
  are UTF-8; the reference was decoded as UTF-8. *Measured:* no effect, since
  the scorer dropped every non-ASCII character anyway.
- Sentences in the generated summaries are joined with no separator.
- In 49 of the 50 references (`extrato_humano.txt`), every sentence still
  ended with its source tag (`<D1_C1_Folha; p1-s1>`), so tokens such as "D1",
  "Folha" and "p1" counted as reference words for every system. Only C31 had
  the tags removed.
- Summary length is `count('.')` in the CSTSumm summary.
- ConceptRank uses word length (`len(term)`) as the concept weight instead of
  the per-document term weight of the original WIVES similarity
  (`docs/reference/wives_similarity.java`).
- No redundancy removal across source texts.
- `original.txt` includes each text's `*_titulo.txt`, so titles were ranked as
  sentences.
- The text-length and type-token analyses filter with `<=` thresholds, so each
  bar is cumulative rather than a bin.
- No statistical significance test is present in the code (see the Wilcoxon
  tests below).
- The notebook does not run top to bottom: `df_text_leg` is used but not
  defined (its definition is in commits `2ab0e35` and `7400d92`).
- Both notebooks are Python 2 and depend on cells run out of order; the
  figures have not been regenerated since 2017.
- `average-total.png` has wrong x-axis labels for 13 of its 15 metrics:
  labels follow the CSV column order, but bar heights follow Python 2 `dict`
  order. The heights are correct means, and the three systems share the same
  order, so comparisons within a bar group hold. For example, the bars
  labelled `rouge_2_recall` are ROUGE-4 recall, and those labelled
  `rouge_4_f_score` are ROUGE-2 recall. Only `rouge_1_recall` and
  `rouge_su4_recall` are labelled correctly. Use the table above instead.

## Re-scored at word level

The same 2016 summaries, unchanged, scored twice with
`results/legacy/rescore.py`: once the way the thesis did, and once with
standard word-level ROUGE (Portuguese tokenizer that keeps accents, human
extract without the source tags, via `conceptrank.corpus`). Means over the 50
clusters; Wilcoxon signed-rank tests are paired by cluster. ROUGE-SU4 is not
available in rouge-score.

### As in the thesis (character n-grams, tagged reference)

| System | ROUGE-1 R | ROUGE-2 R | ROUGE-3 R | ROUGE-1 F | ROUGE-2 F |
|---|---|---|---|---|---|
| LexRank | 0.755 | 0.645 | 0.476 | 0.791 | 0.679 |
| ConceptRank | 0.774 | 0.664 | 0.502 | 0.790 | 0.678 |
| CSTSumm | 0.699 | 0.604 | 0.465 | 0.791 | 0.689 |

| Comparison (recall) | Mean diff | Wins | Wilcoxon p |
|---|---|---|---|
| ConceptRank vs LexRank, rouge1 | +0.020 | 33/50 | 0.034 |
| ConceptRank vs LexRank, rouge2 | +0.019 | 34/50 | 0.041 |
| ConceptRank vs CSTSumm, rouge1 | +0.076 | 38/50 | 0.000 |
| ConceptRank vs CSTSumm, rouge2 | +0.060 | 36/50 | 0.000 |

### Word level (Portuguese tokenizer, untagged reference)

| System | ROUGE-1 R | ROUGE-2 R | ROUGE-3 R | ROUGE-1 F | ROUGE-2 F |
|---|---|---|---|---|---|
| LexRank | 0.523 | 0.315 | 0.258 | 0.521 | 0.316 |
| ConceptRank | 0.546 | 0.351 | 0.297 | 0.529 | 0.340 |
| CSTSumm | 0.522 | 0.358 | 0.315 | 0.566 | 0.392 |

| Comparison (recall) | Mean diff | Wins | Wilcoxon p |
|---|---|---|---|
| ConceptRank vs LexRank, rouge1 | +0.023 | 29/50 | 0.167 |
| ConceptRank vs LexRank, rouge2 | +0.036 | 28/50 | 0.204 |
| ConceptRank vs CSTSumm, rouge1 | +0.024 | 28/50 | 0.181 |
| ConceptRank vs CSTSumm, rouge2 | -0.007 | 22/50 | 0.709 |

At word level ConceptRank still has higher mean recall than LexRank, but the
difference is not significant over 50 clusters, and its advantage over CSTSumm
disappears; CSTSumm has the best F-scores. These are the 2016 summaries, with
the other issues above still in them (English stemmer, titles as sentences,
dropped hyphenated words), so the fixes in the refactor may move these numbers
either way.

## Reproducing the summaries

The summaries in `archive/experiments_2016/` were generated in October 2016
(ConceptRank on the 3rd, LexRank on the 9th), with Python 2.7. The library
versions were not recorded; the latest releases at the time were
**sumy 0.4.1** and **nltk 3.2.1**.

Running `conceptrank.summarize lexrank` (the ported code) under sumy 0.4.1 and
nltk 3.2.1 reproduces 49 of the 50 LexRank summaries byte for byte, and the
text of the 50th (C49, see below). With the versions in `uv.lock` only 24 are
identical; the other 26 differ for these reasons:

| Cause | Clusters | Detail |
|---|---|---|
| sumy word filter | 23 | sumy 0.4.1 kept only tokens made of letters (`^[^\W\d_]+$`), dropping every hyphenated word. Later versions keep them. |
| nltk word tokenizer | C45, C50 | Words in single quotes (`'seduzir'`) kept the quote attached in nltk 3.2.1 and were then dropped by the filter; current nltk splits the quote off. |
| File not closed | C49 | The 2016 file ends with a duplicated `pública."`, left over from a file handle that was never closed. The summary text is the same. |

Sentence splitting, stop words and stemming are identical between the two
sets of versions.

ConceptRank cannot be reproduced the same way: its similarity depends on the
iteration order of a set of words, which was fixed (but arbitrary) in
Python 2 and is randomized per run in Python 3. The ported code now iterates
in sorted order, so it is deterministic, but only 8 of the 50 summaries match
2016. See `src/conceptrank/concept.py`.
