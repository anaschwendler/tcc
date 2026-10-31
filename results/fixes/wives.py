"""Fix: ConceptRank with the WIVES similarity as in the Java original.

Only ConceptRank changes.
Baseline: ConceptSummarizer, the thesis port, which weights common words by
their length (len(term)) as a running maximum.
Variant: WivesSummarizer, which weights each common word by its normalized
term frequency in each sentence (see src/conceptrank/concept.py).

Also compares the fixed ConceptRank with LexRank, both on the word budget.

    uv run python results/fixes/wives.py
"""

from conceptrank.concept import ConceptSummarizer, WivesSummarizer
from conceptrank.lexrank import LexRankSummarizer

from common import compare, reference_word_counts, references, summarize_all

if __name__ == "__main__":
    refs = references()
    budgets = reference_word_counts(refs)
    legacy = summarize_all(word_budgets=budgets, systems={"ConceptRank": ConceptSummarizer})
    wives = summarize_all(word_budgets=budgets, systems={"ConceptRank": WivesSummarizer})
    compare("Both with the word budget", legacy, wives, refs)

    lexrank = summarize_all(word_budgets=budgets, systems={"LexRank": LexRankSummarizer})
    compare("LexRank (baseline) vs fixed ConceptRank (variant), word budget",
            {"LexRank vs ConceptRank": lexrank["LexRank"]},
            {"LexRank vs ConceptRank": wives["ConceptRank"]}, refs)
