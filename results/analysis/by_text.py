"""Does ConceptRank do better on short texts or on texts with a low type-token ratio?

The thesis claimed both, from ROUGE-2 recall by number of words and ROUGE-3
recall by type-token ratio, using cumulative thresholds (<=) and
character-level ROUGE. This redoes them on the corrected pipeline
(results/fixes/all_fixes.py) with:

- terciles: clusters split into three groups of about 17 by each measure,
  with a paired Wilcoxon test inside each group;
- Spearman correlation, over all 50 clusters, between each measure and
  ConceptRank's advantage over LexRank.

Number of words and type-token ratio are computed on the cluster's source
sentences with the ROUGE tokenizer (lowercased, accents kept).

    uv run python results/analysis/by_text.py
"""

import statistics
import sys
from pathlib import Path

from scipy.stats import spearmanr, wilcoxon

sys.path.insert(0, str(Path(__file__).parents[1] / "fixes"))

from conceptrank.corpus import load_corpus  # noqa: E402
from conceptrank.evaluation import PortugueseTokenizer  # noqa: E402

from all_fixes import corrected_summaries  # noqa: E402
from common import reference_word_counts, references, score_all  # noqa: E402

COMPARED = ["ConceptRank", "ConceptRank (thesis similarity)"]
ANALYSES = [("words", "rouge2", "Number of words"), ("type_token", "rouge3", "Type-token ratio")]


def text_measures(cluster):
    tokens = PortugueseTokenizer().tokenize(" ".join(cluster.sentences))
    return {"words": len(tokens), "type_token": len(set(tokens)) / len(tokens)}


def terciles(values):
    """Split cluster ids into three groups by value, lowest first."""
    ordered = sorted(values, key=values.get)
    size = len(ordered) / 3
    return [ordered[round(i * size):round((i + 1) * size)] for i in range(3)]


def p_value(x, y):
    return 1.0 if all(a == b for a, b in zip(x, y)) else wilcoxon(x, y).pvalue


if __name__ == "__main__":
    corpus = load_corpus()
    refs = references()
    scores = score_all(corrected_summaries(corpus, reference_word_counts(refs)), refs)
    measures = {c.id: text_measures(c) for c in corpus}

    words = [measures[c]["words"] for c in refs]
    type_token = [measures[c]["type_token"] for c in refs]
    print(f"Spearman between number of words and type-token ratio: {spearmanr(words, type_token).statistic:+.2f}")

    for measure, metric, title in ANALYSES:
        values = {cid: m[measure] for cid, m in measures.items()}
        print(f"\n### {title}, {metric.replace('rouge', 'ROUGE-')} recall\n")
        print("| Tercile | Range | Clusters | LexRank | " + " | ".join(COMPARED)
              + " | " + " | ".join(f"{c} vs LexRank p" for c in COMPARED) + " |")
        print("|---|---|---|---|" + "---|" * (2 * len(COMPARED)))
        for name, group in zip(("Low", "Middle", "High"), terciles(values)):
            lexrank = [scores["LexRank"][cid][metric].recall for cid in group]
            others = {s: [scores[s][cid][metric].recall for cid in group] for s in COMPARED}
            low, high = min(values[c] for c in group), max(values[c] for c in group)
            value_range = f"{low:.0f}–{high:.0f}" if measure == "words" else f"{low:.3f}–{high:.3f}"
            print(f"| {name} | {value_range} | {len(group)} | {statistics.mean(lexrank):.3f} | "
                  + " | ".join(f"{statistics.mean(v):.3f}" for v in others.values()) + " | "
                  + " | ".join(f"{p_value(v, lexrank):.3f}" for v in others.values()) + " |")

        print()
        for system in COMPARED:
            advantage = [scores[system][cid][metric].recall - scores["LexRank"][cid][metric].recall for cid in refs]
            result = spearmanr([values[c] for c in refs], advantage)
            print(f"Spearman between {measure} and {system}'s advantage over LexRank: "
                  f"{result.statistic:+.2f} (p = {result.pvalue:.3f})")
