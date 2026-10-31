"""Shared code for the fix experiments in this folder.

Each experiment summarizes every cluster twice with the ported thesis code:
once as the baseline and once with a single change, then scores both with
word-level ROUGE (Portuguese tokenizer) against the untagged human extract and
compares them with paired Wilcoxon tests.

Needs the raw corpus in data/raw/CSTNews/ and the analysis group (scipy).
"""

import statistics
from pathlib import Path

from scipy.stats import wilcoxon

from conceptrank.concept import ConceptSummarizer
from conceptrank.corpus import load_corpus
from conceptrank.evaluation import PortugueseTokenizer, reference_text, score
from conceptrank.lexrank import LexRankSummarizer
from conceptrank.summarize import summarize_cluster

ARCHIVE = Path(__file__).parents[2] / "archive" / "experiments_2016"
SYSTEMS = {"LexRank": LexRankSummarizer, "ConceptRank": ConceptSummarizer}
METRICS = [("rouge1", "recall"), ("rouge2", "recall"), ("rouge1", "fmeasure"), ("rouge2", "fmeasure")]


def references():
    return {c.id: reference_text(c) for c in load_corpus()}


def summarize_all(word_budgets=None, texts=None, **options):
    """{system: {cluster_id: summary}} for every archived cluster.

    `word_budgets` and `texts` map cluster id to that cluster's word budget
    and input text."""
    clusters = {d.name.split("_")[0]: d for d in sorted(ARCHIVE.iterdir())}

    def per_cluster(cid):
        extra = {}
        if word_budgets is not None:
            extra["word_budget"] = word_budgets[cid]
        if texts is not None:
            extra["text"] = texts[cid]
        return extra

    return {
        system: {cid: summarize_cluster(d, cls, **options, **per_cluster(cid)) for cid, d in clusters.items()}
        for system, cls in SYSTEMS.items()
    }


def reference_word_counts(refs):
    return {cid: len(text.split()) for cid, text in refs.items()}


def mean_words(texts):
    """Mean length in ROUGE tokens of {cluster_id: text}."""
    tokenizer = PortugueseTokenizer()
    return round(statistics.mean(len(tokenizer.tokenize(t)) for t in texts.values()), 1)


def score_all(summaries, refs):
    return {
        system: {cid: score(text, refs[cid]) for cid, text in per_cluster.items()}
        for system, per_cluster in summaries.items()
    }


def _p_value(x, y):
    if all(a == b for a, b in zip(x, y)):
        return 1.0
    return wilcoxon(x, y).pvalue


def print_comparison(baseline, variant):
    print("| System | Metric | Baseline | Variant | Diff | Better / worse | Wilcoxon p |")
    print("|---|---|---|---|---|---|---|")
    for system in baseline:
        for metric, attr in METRICS:
            x = [getattr(baseline[system][cid][metric], attr) for cid in baseline[system]]
            y = [getattr(variant[system][cid][metric], attr) for cid in baseline[system]]
            better = sum(b > a for a, b in zip(x, y))
            worse = sum(b < a for a, b in zip(x, y))
            label = f"{metric.replace('rouge', 'ROUGE-')} {'R' if attr == 'recall' else 'F'}"
            print(f"| {system} | {label} | {statistics.mean(x):.3f} | {statistics.mean(y):.3f} | "
                  f"{statistics.mean(y) - statistics.mean(x):+.3f} | {better} / {worse} | {_p_value(x, y):.3f} |")


def changed_summaries(baseline, variant):
    return {system: sum(baseline[system][cid] != variant[system][cid] for cid in baseline[system])
            for system in baseline}
