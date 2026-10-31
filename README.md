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
- [ ] Rewrite corpus ingestion and ROUGE evaluation for Portuguese
- [ ] Fix the known methodological issues, one at a time, measuring each
  - [ ] Keep hyphenated words: re-run with the current tokenizer and compare
        ROUGE against the 2016 summaries (same evaluator for both)
- [ ] Re-run the analysis with baselines and significance tests

## Results (2016, under review)

Mean ROUGE over the 50 CSTNews clusters, scored against the human extracts:

| System | ROUGE-1 R | ROUGE-2 R | ROUGE-3 R | ROUGE-SU4 F |
|---|---|---|---|---|
| LexRank | 0.755 | 0.645 | 0.476 | 0.739 |
| **ConceptRank** | **0.774** | **0.664** | **0.502** | 0.740 |
| CSTSumm | 0.699 | 0.604 | 0.465 | **0.745** |

These are the numbers reported in the thesis. They are kept unchanged in
[results/legacy/](results/legacy/) as the baseline for the refactor, together
with standard deviations, the analyses by text length and type-token ratio,
and a list of known issues in how they were produced. The differences between
systems have not been tested for significance.

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
where to download CSTNews and where to put it. The processed texts, generated
summaries and ROUGE scores for all 50 clusters are already in
`output/experiments/`, so you can browse them without the corpus.

To summarize every cluster the way the thesis did, and to check the result
against the 2016 summaries:

```sh
uv run python -m conceptrank.summarize lexrank output/experiments runs/lexrank
uv run python -m conceptrank.summarize concept output/experiments runs/concept
uv run pytest
```

The original notebooks and scripts are kept in `archive/`. They are Python 2
code and do not run as-is.

## Repository layout

```
├── src/conceptrank/
│   ├── graph.py              # sentence graph and power method
│   ├── lexrank.py            # LexRank similarity (TF-IDF cosine)
│   ├── concept.py            # ConceptRank similarity (WIVES)
│   └── summarize.py          # summarize all clusters as in the thesis
├── tests/                    # regression tests against the 2016 summaries
├── data/README.md            # how to get CSTNews
├── output/experiments/       # per-cluster texts, summaries and ROUGE scores
├── results/legacy/           # thesis results, frozen
├── docs/
│   ├── background.md         # theoretical background
│   └── reference/            # original WIVES similarity (Java)
└── archive/                  # original notebooks, scripts and C1 prototype
```

## Background

[docs/background.md](docs/background.md) covers the theory behind the work:
automatic summarization, graph-based centrality, conceptual similarity, ROUGE
and the CSTNews corpus.

## Author

Ana Schwendler
