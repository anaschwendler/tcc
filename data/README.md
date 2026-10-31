# Data

## CSTNews corpus

All experiments use **CSTNews**, a corpus of 50 clusters of Brazilian Portuguese
news texts (2–3 source texts per cluster, 140 texts in total) with human
multi-document summaries and discourse annotations (RST and CST).

- Download page (NILC / ICMC-USP): <https://sites.icmc.usp.br/taspardo/sucinto/cstnews.html>
- References:
  - Aleixo, P. and Pardo, T. A. S. (2008). CSTNews: um córpus de textos
    jornalísticos anotados segundo a teoria discursiva multidocumento CST.
  - Cardoso, P. C. F. et al. (2011). CSTNews – a discourse-annotated corpus for
    single and multi-document summarization of news texts in Brazilian
    Portuguese. [PDF](http://conteudo.icmc.usp.br/pessoas/taspardo/rst2011-cardosoetal1.pdf)

The corpus is distributed by NILC for research use; check the download page for
the current terms. It is not part of the current tree.

## Where to put the raw corpus

Unpack it into `data/raw/CSTNews/` (git-ignored), one folder per cluster:

```
data/raw/CSTNews/
└── C1_Mundo_AviaoCongo/
    ├── Textos-fonte/                 # source texts, plus a *_titulo.txt per text
    ├── Textos-fonte segmentados/     # one sentence per line
    └── Sumarios/
        ├── *_extrato_humano.txt
        ├── *_sumario_automatico_CSTSumm.txt
        └── ...                       # human abstracts and other summaries
```

The copy used for the thesis is in the git history (commit `79eb0ab`, 2016) and
can be restored with:

```sh
mkdir -p data/raw/CSTNews
git archive 79eb0ab experiments | tar -x -C data/raw/CSTNews --strip-components=1
```

### Running the legacy extraction scripts

`archive/extract_files.py` and `archive/read_archives.py` still read from
`experiments/` relative to the current directory and write to `output/`. To
run them, link the corpus there and run them from the repository root:

```sh
ln -s data/raw/CSTNews experiments
python archive/read_archives.py   # -> output/experiments/<cluster>/original.txt
python archive/extract_files.py   # -> extrato_humano.txt, sumario_automatico_CSTSumm.txt
```

## Thesis data: `archive/experiments_2016/<cluster>/`

What those scripts and the notebooks produced in 2016, kept as it was:

| File | Content |
|---|---|
| `original.txt` | Every file in `Textos-fonte/` concatenated, titles included, with no separator |
| `extrato_humano.txt` | Human extract, the reference used for ROUGE |
| `sumario_automatico_CSTSumm.txt` | CSTSumm summary, from the corpus |
| `lexrank_summ.txt` | LexRank summary (`archive/BetaRank.ipynb`) |
| `concept_summ.txt` | ConceptRank summary (`archive/ConceptRank.ipynb`) |
| `rouge_*.txt` | ROUGE scores per system, stored as a Python `dict` literal |

Known quirks:

- Encoding is UTF-8, except `sumario_automatico_CSTSumm.txt` in C12, C34, C36
  and C39, which is Latin-1.
- `original.txt` mixes CRLF and LF line endings.
- Generated summaries have sentences joined with no space or newline.
- 13 cluster folders carry a ` - concordanciaRST` / ` - concordanciaCST` suffix
  (with spaces) taken from the corpus folder names.
