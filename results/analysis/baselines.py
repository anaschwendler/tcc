"""Lead and random baselines against the corrected pipeline.

Same setting as results/fixes/all_fixes.py: corpus sentences (no titles), word
budget from the human extract, word-level ROUGE. Random is averaged over 10
seeds per cluster.

    uv run python results/analysis/baselines.py
"""

import statistics
import sys
from pathlib import Path

from rouge_score.scoring import Score

sys.path.insert(0, str(Path(__file__).parents[1] / "fixes"))

from conceptrank.baselines import lead_ratings, random_ratings  # noqa: E402
from conceptrank.corpus import load_corpus  # noqa: E402
from conceptrank.evaluation import score  # noqa: E402
from conceptrank.summarize import select_by_word_budget  # noqa: E402

from all_fixes import corrected_summaries, print_means, print_pairs  # noqa: E402
from common import reference_word_counts, references, score_all  # noqa: E402

RANDOM_SEEDS = range(10)
PAIRS = [
    ("ConceptRank", "Lead"),
    ("LexRank", "Lead"),
    ("ConceptRank", "Random"),
    ("LexRank", "Random"),
    ("Lead", "CSTSumm"),
]


def lead_summary(cluster, budget):
    sources = [source.sentences for source in cluster.sources]
    return " ".join(select_by_word_budget(cluster.sentences, lead_ratings(sources), budget))


def random_summary(cluster, budget, seed):
    ratings = random_ratings(cluster.sentences, seed)
    return " ".join(select_by_word_budget(cluster.sentences, ratings, budget))


def mean_score(scores):
    """Average a list of {metric: Score} into one {metric: Score}."""
    return {
        metric: Score(*(statistics.mean(getattr(s[metric], attr) for s in scores)
                        for attr in ("precision", "recall", "fmeasure")))
        for metric in scores[0]
    }


if __name__ == "__main__":
    corpus = load_corpus()
    refs = references()
    budgets = reference_word_counts(refs)

    summaries = corrected_summaries(corpus, budgets)
    summaries["Lead"] = {c.id: lead_summary(c, budgets[c.id]) for c in corpus}
    scores = score_all(summaries, refs)

    random_runs = {c.id: [random_summary(c, budgets[c.id], seed) for seed in RANDOM_SEEDS] for c in corpus}
    scores["Random"] = {cid: mean_score([score(s, refs[cid]) for s in runs]) for cid, runs in random_runs.items()}
    summaries["Random"] = {cid: runs[0] for cid, runs in random_runs.items()}

    print_means(scores, summaries)
    print_pairs(scores, PAIRS)
