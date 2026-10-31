"""The "thesis2016" tokenizer must reproduce the ROUGE scores of the thesis.

Scores the archived summaries the way src/rouge.ipynb did (reference read as
UTF-8, every summary as Latin-1) and compares with the archived rouge_*.txt.
"""

import ast
from pathlib import Path

import pytest

from conceptrank.evaluation import score

ARCHIVE = Path(__file__).parents[1] / "archive" / "experiments_2016"
SYSTEMS = {
    "lexrank": ("lexrank_summ.txt", "rouge_lexrank.txt"),
    "concept": ("concept_summ.txt", "rouge_concept.txt"),
    "CSTSumm": ("sumario_automatico_CSTSumm.txt", "rouge_CSTSUmm.txt"),
}
MEASURES = {"recall": "recall", "precision": "precision", "f_score": "fmeasure"}


def params():
    out = []
    for system in SYSTEMS:
        for cluster_dir in sorted(ARCHIVE.iterdir()):
            cluster_id = cluster_dir.name.split("_")[0]
            marks = []
            if system == "lexrank" and cluster_id == "C49":
                marks.append(pytest.mark.xfail(
                    reason="the summary file got extra text after it was scored", strict=True,
                ))
            out.append(pytest.param(system, cluster_dir, id=f"{system}-{cluster_id}", marks=marks))
    return out


@pytest.mark.parametrize("system,cluster_dir", params())
def test_reproduces_thesis_scores(system, cluster_dir):
    summary_file, rouge_file = SYSTEMS[system]
    expected = ast.literal_eval((cluster_dir / rouge_file).read_text())
    reference = (cluster_dir / "extrato_humano.txt").read_bytes().decode("utf-8")
    summary = (cluster_dir / summary_file).read_bytes().decode("latin-1")
    scores = score(summary, reference, "thesis2016")
    for n in "1234":
        for measure, attr in MEASURES.items():
            actual = getattr(scores[f"rouge{n}"], attr)
            # ROUGE-1.5.5 printed 5 decimals, sometimes rounding down
            assert actual == pytest.approx(expected[f"rouge_{n}_{measure}"], abs=2e-5)
