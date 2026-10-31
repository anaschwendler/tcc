# Legacy results (2017)

These are the results reported in the thesis, frozen as they were on
2017-07-07. They are kept as a baseline: every fix made during the refactor
should be measured against these numbers. **Do not regenerate or edit them.**

## How they were produced

1. `src/read_archives.py` and `src/extract_files.py` copied source texts, human
   extracts and CSTSumm summaries from CSTNews into `output/experiments/`.
2. `src/BetaRank.ipynb` (LexRank) and `src/ConceptRank.ipynb` wrote
   `lexrank_summ.txt` and `concept_summ.txt` for each cluster, with the
   number of sentences taken from the CSTSumm summary.
3. `src/rouge.ipynb` scored each summary against `extrato_humano.txt` with
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
exactly one `output/experiments/<cluster>/rouge_*.txt` file.

## Summary (mean ± std over 50 clusters)

| System | ROUGE-1 R | ROUGE-2 R | ROUGE-3 R | ROUGE-SU4 F |
|---|---|---|---|---|
| LexRank | 0.7546 ± 0.1863 | 0.6452 ± 0.1443 | 0.4757 ± 0.1229 | 0.7390 ± 0.0875 |
| ConceptRank | 0.7744 ± 0.1830 | 0.6640 ± 0.1513 | 0.5016 ± 0.1351 | 0.7401 ± 0.0885 |
| CSTSumm | 0.6987 ± 0.1680 | 0.6043 ± 0.1207 | 0.4646 ± 0.1005 | 0.7453 ± 0.0837 |

## Known issues

These are known from reading the code and have not yet been measured:

- Stemmer and stop words are English (`LANGUAGE = "english"`).
- Hyphenated words ("segunda-feira", "porta-voz", "vice-presidente") were
  dropped by the tokenizer, so they never counted towards similarity (see
  below).
- All system summaries were decoded as Latin-1 before scoring, although most
  are UTF-8; the reference was decoded as UTF-8.
- Sentences in the generated summaries are joined with no separator.
- Summary length is `count('.')` in the CSTSumm summary.
- ConceptRank uses word length (`len(term)`) as the concept weight instead of
  the per-document term weight of the original WIVES similarity
  (`docs/reference/wives_similarity.java`).
- No redundancy removal across source texts.
- The text-length and type-token analyses filter with `<=` thresholds, so each
  bar is cumulative rather than a bin.
- No statistical significance test is present in the code.
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

## Reproducing the summaries

The summaries in `output/experiments/` were generated in October 2016
(ConceptRank on the 3rd, LexRank on the 9th), with Python 2.7. The library
versions were not recorded; the latest releases at the time were
**sumy 0.4.1** and **nltk 3.2.1**.

Running `conceptrank.summarize lexrank` (the ported code) under sumy 0.4.1 and
nltk 3.2.1 reproduces all 50 LexRank summaries. With the versions in
`uv.lock` it reproduces only 24, for these reasons:

| Cause | Clusters | Detail |
|---|---|---|
| sumy word filter | 47 | sumy 0.4.1 kept only tokens made of letters (`^[^\W\d_]+$`), dropping every hyphenated word. Later versions keep them. |
| nltk word tokenizer | C45, C50 | Words in single quotes (`'seduzir'`) kept the quote attached in nltk 3.2.1 and were then dropped by the filter; current nltk splits the quote off. |
| File not closed | C49 | The 2016 file ends with a duplicated `pública."`, left over from a file handle that was never closed. The summary text is the same. |

Sentence splitting, stop words and stemming are identical between the two
sets of versions.

ConceptRank cannot be reproduced the same way: its similarity depends on the
iteration order of a set of words, which was fixed (but arbitrary) in
Python 2 and is randomized per run in Python 3. See
`src/conceptrank/concept.py`.
