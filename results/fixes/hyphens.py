"""Fix: keep hyphenated words ("segunda-feira", "porta-voz").

Baseline: LegacyTokenizer, the sumy 0.4.1 word filter used in the thesis.
Variant: sumy's current Tokenizer, which keeps hyphenated words.

    uv run python results/fixes/hyphens.py
"""

from sumy.nlp.tokenizers import Tokenizer

from common import compare, reference_word_counts, references, summarize_all

if __name__ == "__main__":
    refs = references()
    compare("Fixed sentence count", summarize_all(), summarize_all(tokenizer_cls=Tokenizer), refs)
    budgets = reference_word_counts(refs)
    compare("Both with the word budget", summarize_all(word_budgets=budgets),
            summarize_all(word_budgets=budgets, tokenizer_cls=Tokenizer), refs)
