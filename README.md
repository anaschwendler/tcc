# ConceptRank

**Graph-based conceptual centrality as salience in extractive text summarization**

ConceptRank is an extractive multi-document summarizer for Brazilian
Portuguese news. It builds the same sentence graph as
[LexRank](https://doi.org/10.1613/jair.1523)
(Erkan and Radev, 2004) and ranks sentences by centrality, but measures how
similar two sentences are with a conceptual similarity (Loh et al.) instead of
TF-IDF cosine. The aim is to be less sensitive to typos, synonyms and spelling
variants.

This is the code of my undergraduate thesis (TCC), evaluated on the
[CSTNews](data/README.md) corpus against LexRank and
[CSTSumm](http://seer.ufrgs.br/index.php/rita/article/view/RITA-VOL23-NR1-183/37492)
with [ROUGE](http://anthology.aclweb.org/W/W04/W04-1013.pdf).

## Status

The thesis was finished in 2016 and the code was written to meet a deadline:
notebooks, Python 2 and hard-coded paths. It is now being refactored into a
reproducible pipeline:

- [x] Clean up the repository and freeze the original results
- [x] Python 3 project managed with uv
- [x] Move the summarizers from notebooks into the `conceptrank` package
- [x] Rewrite corpus ingestion and ROUGE evaluation for Portuguese
- [ ] Fix the known methodological issues, one at a time, measuring each
  - [ ] Keep hyphenated words: re-run with the current tokenizer and compare
        ROUGE against the 2016 summaries (same evaluator for both)
- [ ] Re-run the analysis with baselines and significance tests

## Results (2016 summaries, under review)

The thesis reported ROUGE-1 recall of 0.774 for ConceptRank against 0.755 for
LexRank and 0.699 for CSTSumm. While refactoring it turned out that those
scores were computed on **characters** rather than words, because of how the
scoring library was called. Re-scoring the same 2016 summaries with standard
word-level ROUGE against the CSTNews human extracts (means over 50 clusters):

| System | ROUGE-1 R | ROUGE-2 R | ROUGE-1 F | ROUGE-2 F |
|---|---|---|---|---|
| LexRank | 0.523 | 0.315 | 0.521 | 0.316 |
| ConceptRank | **0.546** | 0.351 | 0.529 | 0.340 |
| CSTSumm | 0.522 | **0.358** | **0.566** | **0.392** |

ConceptRank keeps a higher mean recall than LexRank, but the difference is not
statistically significant (Wilcoxon p = 0.17 for ROUGE-1, 0.20 for ROUGE-2),
and CSTSumm has the best F-scores. These summaries still carry other known
issues that the refactor will fix and measure one at a time.
[results/legacy/](results/legacy/) has the original numbers, the full
comparison and the list of issues.

## Running locally

You need [git](https://git-scm.com/) and [uv](https://docs.astral.sh/uv/).
uv installs Python 3.12 and every dependency at the versions pinned in
`uv.lock`.

```sh
git clone https://github.com/anaschwendler/tcc.git
cd tcc
uv sync --all-groups
uv run python -c "import nltk; nltk.download('punkt_tab')"
```

The raw corpus is not included. [data/README.md](data/README.md) explains
where to get CSTNews and where to put it. The processed texts, summaries and
ROUGE scores from the thesis, for all 50 clusters, are in
`archive/experiments_2016/`, so you can browse them without the corpus.

To summarize every cluster the way the thesis did, and to check the result
against the 2016 summaries:

```sh
uv run python -m conceptrank.summarize lexrank archive/experiments_2016 runs/lexrank
uv run python -m conceptrank.summarize concept archive/experiments_2016 runs/concept
uv run pytest
```

The original notebooks and scripts are kept in `archive/`. They are Python 2
code and do not run as-is.

## Repository layout

```
├── src/conceptrank/
│   ├── corpus.py             # load the raw CSTNews corpus
│   ├── graph.py              # sentence graph and power method
│   ├── lexrank.py            # LexRank similarity (TF-IDF cosine)
│   ├── concept.py            # ConceptRank similarity (WIVES)
│   ├── summarize.py          # summarize all clusters as in the thesis
│   └── evaluation.py         # ROUGE with a Portuguese tokenizer
├── tests/                    # regression tests against the 2016 summaries
├── data/README.md            # how to get CSTNews
├── results/legacy/           # thesis results, frozen
├── docs/
│   ├── background.md         # theoretical background
│   └── reference/            # original WIVES similarity (Java)
└── archive/
    ├── experiments_2016/     # per-cluster texts, summaries and ROUGE (2016)
    └── ...                   # original notebooks, scripts and C1 prototype
```

## Background

[docs/background.md](docs/background.md) covers the theory behind the work:
automatic summarization, graph-based centrality, conceptual similarity, ROUGE
and the CSTNews corpus.

## Author

Ana Schwendler
