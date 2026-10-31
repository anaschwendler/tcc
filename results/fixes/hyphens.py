"""Fix: keep hyphenated words ("segunda-feira", "porta-voz").

Baseline: LegacyTokenizer, the sumy 0.4.1 word filter used in the thesis.
Variant: sumy's current Tokenizer, which keeps hyphenated words.

    uv run python results/fixes/hyphens.py
"""

from sumy.nlp.tokenizers import Tokenizer

from common import changed_summaries, print_comparison, references, score_all, summarize_all

if __name__ == "__main__":
    refs = references()
    baseline = summarize_all()
    variant = summarize_all(tokenizer_cls=Tokenizer)
    print("Summaries changed:", changed_summaries(baseline, variant), "\n")
    print_comparison(score_all(baseline, refs), score_all(variant, refs))
