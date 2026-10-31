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

The corpus is distributed by NILC for research use. The raw corpus is **not**
committed to this repository; check the download page for the current terms.

## Where to put the raw corpus

Unpack it into `data/raw/CSTNews/` (git-ignored), one folder per cluster:

```
data/raw/CSTNews/
└── C1_Mundo_AviaoCongo/
    ├── Textos-fonte/                 # source texts
    ├── Textos-fonte segmentados/     # one sentence per line
    └── Sumarios/
        ├── *_extrato_humano.txt
        └── *_sumario_automatico_CSTSumm.txt
```

This is the layout the extraction scripts expect; confirm it against the
archive you download.

### Running the legacy extraction scripts

`archive/extract_files.py` and `archive/read_archives.py` still read from
`experiments/` relative to the current directory. Until they are rewritten,
link the corpus there and run them from the repository root:

```sh
ln -s data/raw/CSTNews experiments
python archive/read_archives.py   # -> output/experiments/<cluster>/original.txt
python archive/extract_files.py   # -> extrato_humano.txt, sumario_automatico_CSTSumm.txt
```

## Processed data: `output/experiments/<cluster>/`

| File | Content |
|---|---|
| `original.txt` | All source texts of the cluster concatenated (no separator between texts) |
| `extrato_humano.txt` | Human extract, the reference used for ROUGE |
| `sumario_automatico_CSTSumm.txt` | CSTSumm summary, from the corpus |
| `lexrank_summ.txt` | LexRank summary (`archive/BetaRank.ipynb`) |
| `concept_summ.txt` | ConceptRank summary (`archive/ConceptRank.ipynb`) |
| `rouge_*.txt` | ROUGE scores per system, stored as a Python `dict` literal |

Known quirks, to be fixed when ingestion is rewritten:

- Encoding is UTF-8, except `sumario_automatico_CSTSumm.txt` in C12, C34, C36
  and C39, which is Latin-1.
- `original.txt` mixes CRLF and LF line endings.
- Generated summaries have sentences joined with no space or newline.
- 13 cluster folders carry a ` - concordanciaRST` / ` - concordanciaCST` suffix
  (with spaces) taken from the corpus folder names.
