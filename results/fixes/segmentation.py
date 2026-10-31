"""Fix: use the corpus' own sentence segmentation.

Both sides leave titles out, so that only segmentation changes (titles.py
measures removing them).
Baseline: original.txt without titles, split into sentences by sumy's
tokenizer (NLTK punkt, English model), as in the thesis.
Variant: the sentences of "Textos-fonte segmentados", loaded by
conceptrank.corpus. Those files are also a revised copy of the texts: they
add datelines ("RIO -") and fix a few quotes and full stops.

    uv run python results/fixes/segmentation.py
"""

from conceptrank.corpus import load_corpus

from common import compare, reference_word_counts, references, summarize_all
from titles import texts_without_titles

if __name__ == "__main__":
    refs = references()
    texts = texts_without_titles()
    sentences = {c.id: c.sentences for c in load_corpus()}
    budgets = reference_word_counts(refs)
    compare("Both with the word budget", summarize_all(word_budgets=budgets, texts=texts),
            summarize_all(word_budgets=budgets, sentences=sentences), refs)
