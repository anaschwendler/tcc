# ConceptRank

[![tests](https://github.com/anaschwendler/tcc/actions/workflows/tests.yml/badge.svg)](https://github.com/anaschwendler/tcc/actions/workflows/tests.yml)

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
- [x] Fix the known methodological issues, one at a time, measuring each
      ([results/fixes/](results/fixes/))
  - [x] Keep hyphenated words
  - [x] Word budget from the human extract
  - [x] Portuguese stemmer and stop words
  - [x] Titles not ranked as sentences
  - [x] Corpus sentence segmentation
  - [x] WIVES weights as in the Java original
  - [x] All fixes together
- [x] Re-run the analysis with baselines and significance tests
      ([results/analysis/](results/analysis/))
  - [x] Lead and random baselines
  - [x] Redundancy removal (MMR)
  - [x] Results by text length and type-token ratio

## Results

Corrected pipeline on the 50 CSTNews clusters, scored with word-level ROUGE
against the human extracts (means; every summary cut to the length of the
human extract):

| System | ROUGE-1 R | ROUGE-2 R | ROUGE-1 F | ROUGE-2 F |
|---|---|---|---|---|
| LexRank | 0.569 | 0.364 | 0.570 | 0.365 |
| ConceptRank | 0.579 | 0.376 | 0.579 | 0.377 |
| CSTSumm | 0.505 | 0.343 | 0.562 | 0.385 |
| Lead (baseline) | **0.587** | **0.404** | **0.586** | **0.404** |
| Random (baseline) | 0.514 | 0.286 | 0.515 | 0.287 |

ConceptRank is ahead of LexRank by about 0.01, which is not statistically
significant over 50 clusters (Wilcoxon p > 0.8). Both are clearly better than
random sentences (p < 0.001), but neither beats Lead, which takes the opening
sentences of each news text; the gap is not significant either way. CSTSumm's
summaries are shorter than the budget, so its recall is lower; on F-score it is
level with the others. Details in [results/fixes/](results/fixes/README.md) and
[results/analysis/](results/analysis/README.md).

The thesis also claimed that ConceptRank does better on short texts and on
texts with a low type-token ratio; on the corrected pipeline neither holds
(see [results/analysis/](results/analysis/README.md)). Removing redundancy
with MMR made no difference either.

### How this differs from the thesis

The thesis reported ROUGE-1 recall of 0.774 for ConceptRank, 0.755 for LexRank
and 0.699 for CSTSumm. While refactoring it turned out that those scores were
computed on **characters** rather than words, because of how the scoring
library was called. Scored at word level, the 2016 summaries reach 0.546
(ConceptRank), 0.523 (LexRank) and 0.522 (CSTSumm), with no significant
difference between ConceptRank and LexRank
([results/legacy/](results/legacy/README.md)).

The pipeline also had several issues, each fixed and measured on its own in
[results/fixes/](results/fixes/README.md). Removing titles from the input,
keeping hyphenated words and fixing summary length helped; Portuguese stemming,
the corpus' sentence segmentation and the WIVES weights of the original Java
code made no significant difference.

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
