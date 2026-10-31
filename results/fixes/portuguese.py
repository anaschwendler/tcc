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

from common import changed_summaries, print_comparison, references, score_all, summarize_all

if __name__ == "__main__":
    refs = references()
    baseline_summaries = summarize_all()
    baseline = score_all(baseline_summaries, refs)
    variants = {
        "NLTK stop words": summarize_all(language="portuguese", tokenizer_language="english",
                                         stop_words=stopwords.words("portuguese")),
        "sumy list": summarize_all(language="portuguese", tokenizer_language="english"),
    }
    for name, summaries in variants.items():
        print(f"\n### Variant: {name}\n")
        print("Summaries changed:", changed_summaries(baseline_summaries, summaries), "\n")
        print_comparison(baseline, score_all(summaries, refs))
