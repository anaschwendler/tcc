"""Redundancy removal with Maximal Marginal Relevance (MMR).

Same setting as results/fixes/all_fixes.py. Baseline: LexRank and ConceptRank
(WIVES weights) taking sentences by centrality. Variant: the same systems with
MMR, lambda = 0.7, each using its own similarity to measure redundancy. Lambda
was fixed before looking at results; the sweep at the end uses the same 50
clusters it reports on, so it is for reference only.

    uv run python results/analysis/mmr.py
"""

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "fixes"))

from all_fixes import corrected_summaries, print_pairs  # noqa: E402
from baselines import lead_summary  # noqa: E402
from common import compare, reference_word_counts, references, score_all  # noqa: E402

from conceptrank.concept import WivesSummarizer  # noqa: E402
from conceptrank.corpus import load_corpus  # noqa: E402
from conceptrank.lexrank import LexRankSummarizer  # noqa: E402

MMR_LAMBDA = 0.7
SWEEP = (0.5, 0.6, 0.8, 0.9)
SYSTEMS = {"LexRank": LexRankSummarizer, "ConceptRank": WivesSummarizer}


def without_cstsumm(summaries):
    return {s: per for s, per in summaries.items() if s != "CSTSumm"}


if __name__ == "__main__":
    corpus = load_corpus()
    refs = references()
    budgets = reference_word_counts(refs)

    plain = without_cstsumm(corrected_summaries(corpus, budgets, systems=SYSTEMS))
    mmr = without_cstsumm(corrected_summaries(corpus, budgets, systems=SYSTEMS, mmr_lambda=MMR_LAMBDA))
    compare(f"MMR (lambda = {MMR_LAMBDA}) against selection by centrality", plain, mmr, refs)

    print(f"\n### MMR (lambda = {MMR_LAMBDA}) against Lead")
    scores = score_all({**{f"{s} + MMR": per for s, per in mmr.items()},
                        "Lead": {c.id: lead_summary(c, budgets[c.id]) for c in corpus}}, refs)
    print_pairs(scores, [("LexRank + MMR", "Lead"), ("ConceptRank + MMR", "Lead")])

    print("\n### Lambda sweep (reference only, ROUGE-1 R / ROUGE-2 R)\n")
    print("| Lambda | LexRank | ConceptRank |")
    print("|---|---|---|")
    for mmr_lambda in SWEEP:
        swept = score_all(without_cstsumm(corrected_summaries(corpus, budgets, systems=SYSTEMS,
                                                              mmr_lambda=mmr_lambda)), refs)
        cells = [" / ".join(f"{statistics.mean(s[m].recall for s in swept[system].values()):.3f}"
                            for m in ("rouge1", "rouge2")) for system in SYSTEMS]
        print(f"| {mmr_lambda} | " + " | ".join(cells) + " |")
