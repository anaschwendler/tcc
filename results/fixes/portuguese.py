"""Fix: Portuguese stemmer and stop words.

Baseline: English Snowball stemmer and sumy's English stop words, as in the
thesis.
Variant: Portuguese Snowball stemmer and NLTK's Portuguese stop words. Sentence
and word splitting stay English, so only stemming and stop words change.

sumy's own Portuguese list is not used: 36 of its 195 entries are stored as
literal escapes ("n\\xe3o" instead of "não"), so common words such as "não",
"já" and "são" would not be removed. The "sumy list" variant shows its effect.

    uv run python -c "import nltk; nltk.download('stopwords')"
    uv run python results/fixes/portuguese.py
"""

from nltk.corpus import stopwords

from common import (changed_summaries, print_comparison, reference_word_counts, references,
                    score_all, summarize_all)

PORTUGUESE = {"language": "portuguese", "tokenizer_language": "english"}


def compare(title, baseline_summaries, variant_summaries, refs):
    print(f"\n### {title}\n")
    print("Summaries changed:", changed_summaries(baseline_summaries, variant_summaries), "\n")
    print_comparison(score_all(baseline_summaries, refs), score_all(variant_summaries, refs))


if __name__ == "__main__":
    refs = references()
    nltk_stop_words = stopwords.words("portuguese")
    baseline = summarize_all()
    compare("NLTK stop words", baseline,
            summarize_all(**PORTUGUESE, stop_words=nltk_stop_words), refs)
    compare("sumy list", baseline, summarize_all(**PORTUGUESE), refs)

    # With a fixed sentence count the Portuguese variant picks shorter
    # sentences, so compare again with both sides on the same word budget.
    budgets = reference_word_counts(refs)
    compare("NLTK stop words, both with the word budget",
            summarize_all(word_budgets=budgets),
            summarize_all(word_budgets=budgets, **PORTUGUESE, stop_words=nltk_stop_words), refs)
