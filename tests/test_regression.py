"""The ported summarizers must reproduce the thesis summaries.

Compares against the files in output/experiments/, generated in 2016. See
results/legacy/README.md for why some clusters cannot match.

ConceptRank is not covered: the 2016 output depended on Python 2 set
iteration order, which cannot be reproduced (see src/conceptrank/concept.py).
"""

from pathlib import Path

import pytest

from conceptrank.lexrank import LexRankSummarizer
from conceptrank.summarize import LegacyTokenizer, summarize_cluster

EXPERIMENTS = Path(__file__).parents[1] / "output" / "experiments"
CLUSTERS = sorted(d for d in EXPERIMENTS.iterdir() if (d / "original.txt").exists())

KNOWN_DIFFERENCES = {
    "C45": "nltk 3.2.1 kept single quotes attached to words",
    "C49": "2016 file has a leftover from a handle that was never closed",
    "C50": "nltk 3.2.1 kept single quotes attached to words",
}


def cluster_params():
    params = []
    for cluster_dir in CLUSTERS:
        cluster_id = cluster_dir.name.split("_")[0]
        marks = []
        if cluster_id in KNOWN_DIFFERENCES:
            marks.append(pytest.mark.xfail(reason=KNOWN_DIFFERENCES[cluster_id], strict=True))
        params.append(pytest.param(cluster_dir, id=cluster_id, marks=marks))
    return params


def test_all_clusters_found():
    assert len(CLUSTERS) == 50


@pytest.mark.parametrize("cluster_dir", cluster_params())
def test_lexrank_matches_thesis(cluster_dir):
    expected = (cluster_dir / "lexrank_summ.txt").read_text(encoding="utf-8")
    assert summarize_cluster(cluster_dir, LexRankSummarizer) == expected


def test_legacy_tokenizer_drops_hyphenated_words():
    words = LegacyTokenizer("english").to_words("O porta-voz falou nesta segunda-feira.")
    assert words == ("O", "falou", "nesta")
