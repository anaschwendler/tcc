"""Re-score the 2016 summaries as the thesis did and at word level.

Needs the raw corpus in data/raw/CSTNews/ (for the untagged reference) and the
analysis dependency group (scipy):

    uv run python results/legacy/rescore.py
"""

import statistics
from pathlib import Path

from scipy.stats import wilcoxon

from conceptrank.corpus import load_corpus, read_text
from conceptrank.evaluation import reference_text, score

ARCHIVE = Path(__file__).parents[2] / "archive" / "experiments_2016"
SYSTEMS = {
    "LexRank": "lexrank_summ.txt",
    "ConceptRank": "concept_summ.txt",
    "CSTSumm": "sumario_automatico_CSTSumm.txt",
}
COLUMNS = [("rouge1", "recall"), ("rouge2", "recall"), ("rouge3", "recall"),
           ("rouge1", "fmeasure"), ("rouge2", "fmeasure")]
PAIRS = [("ConceptRank", "LexRank"), ("ConceptRank", "CSTSumm")]


def score_all(folders, references, tokenizer):
    return {
        system: {cid: score(read_text(folders[cid] / filename), references[cid], tokenizer)
                 for cid in references}
        for system, filename in SYSTEMS.items()
    }


def print_report(title, scores):
    print(f"\n### {title}\n")
    print("| System | ROUGE-1 R | ROUGE-2 R | ROUGE-3 R | ROUGE-1 F | ROUGE-2 F |")
    print("|---|---|---|---|---|---|")
    for system, per_cluster in scores.items():
        means = [statistics.mean(getattr(s[metric], attr) for s in per_cluster.values())
                 for metric, attr in COLUMNS]
        print(f"| {system} | " + " | ".join(f"{m:.3f}" for m in means) + " |")
    print("\n| Comparison (recall) | Mean diff | Wins | Wilcoxon p |")
    print("|---|---|---|---|")
    for a, b in PAIRS:
        for metric in ("rouge1", "rouge2"):
            x = [scores[a][cid][metric].recall for cid in scores[a]]
            y = [scores[b][cid][metric].recall for cid in scores[a]]
            wins = sum(p > q for p, q in zip(x, y))
            p_value = wilcoxon(x, y).pvalue
            diff = statistics.mean(x) - statistics.mean(y)
            print(f"| {a} vs {b}, {metric} | {diff:+.3f} | {wins}/50 | {p_value:.3f} |")


def main():
    corpus = {c.id: c for c in load_corpus()}
    folders = {d.name.split("_")[0]: d for d in ARCHIVE.iterdir()}
    tagged = {cid: read_text(folders[cid] / "extrato_humano.txt") for cid in corpus}
    clean = {cid: reference_text(cluster) for cid, cluster in corpus.items()}
    print_report("As in the thesis (character n-grams, tagged reference)",
                 score_all(folders, tagged, "thesis2016"))
    print_report("Word level (Portuguese tokenizer, untagged reference)",
                 score_all(folders, clean, "portuguese"))


if __name__ == "__main__":
    main()
