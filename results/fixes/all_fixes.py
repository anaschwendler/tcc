"""All fixes together: the corrected pipeline.

- sentences from the corpus segmentation, so titles are left out
- sumy's current tokenizer, which keeps hyphenated words
- Portuguese Snowball stemmer and NLTK's Portuguese stop words
- word budget from the human extract

Systems: LexRank, ConceptRank with the WIVES weights of the Java original,
ConceptRank with the thesis port's similarity, and CSTSumm (the corpus'
summary, cut to the same word budget).

    uv run python results/fixes/all_fixes.py
"""

import statistics

from nltk.corpus import stopwords
from sumy.nlp.tokenizers import Tokenizer

from conceptrank.concept import ConceptSummarizer, WivesSummarizer
from conceptrank.corpus import load_corpus
from conceptrank.lexrank import LexRankSummarizer

from common import METRICS, _p_value, mean_words, reference_word_counts, references, score_all, summarize_all

SYSTEMS = {
    "LexRank": LexRankSummarizer,
    "ConceptRank": WivesSummarizer,
    "ConceptRank (thesis similarity)": ConceptSummarizer,
}
PAIRS = [
    ("ConceptRank", "LexRank"),
    ("ConceptRank (thesis similarity)", "LexRank"),
    ("ConceptRank", "CSTSumm"),
    ("LexRank", "CSTSumm"),
]


def label(metric, attr):
    return f"{metric.replace('rouge', 'ROUGE-')} {'R' if attr == 'recall' else 'F'}"


if __name__ == "__main__":
    corpus = load_corpus()
    refs = references()
    budgets = reference_word_counts(refs)
    summaries = summarize_all(
        word_budgets=budgets,
        sentences={c.id: c.sentences for c in corpus},
        systems=SYSTEMS,
        language="portuguese",
        tokenizer_cls=Tokenizer,
        stop_words=stopwords.words("portuguese"),
    )
    summaries["CSTSumm"] = {c.id: " ".join(c.cstsumm.split()[:budgets[c.id]]) for c in corpus}
    scores = score_all(summaries, refs)

    print("| System | Words | " + " | ".join(label(m, a) for m, a in METRICS) + " |")
    print("|---|---|" + "---|" * len(METRICS))
    for system, per_cluster in scores.items():
        means = [statistics.mean(getattr(s[m], a) for s in per_cluster.values()) for m, a in METRICS]
        print(f"| {system} | {mean_words(summaries[system])} | " + " | ".join(f"{x:.3f}" for x in means) + " |")

    print("\n| Comparison | Metric | Diff | Better / worse | Wilcoxon p |")
    print("|---|---|---|---|---|")
    for a, b in PAIRS:
        for metric, attr in METRICS:
            x = [getattr(scores[a][cid][metric], attr) for cid in refs]
            y = [getattr(scores[b][cid][metric], attr) for cid in refs]
            better = sum(p > q for p, q in zip(x, y))
            worse = sum(p < q for p, q in zip(x, y))
            print(f"| {a} vs {b} | {label(metric, attr)} | {statistics.mean(x) - statistics.mean(y):+.3f} | "
                  f"{better} / {worse} | {_p_value(x, y):.3f} |")
