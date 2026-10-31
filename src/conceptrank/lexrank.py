"""LexRank: sentence similarity is the TF-IDF cosine.

Erkan and Radev (2004), Graph-based Centrality as Salience in Text
Summarization. Ported from BetaSummarizer in archive/BetaRank.ipynb.
"""

import math

from conceptrank.graph import GraphSummarizer


class LexRankSummarizer(GraphSummarizer):
    @staticmethod
    def compute_distance(sentence1, sentence2, tf1, tf2, idf_metrics):
        common_words = frozenset(sentence1) & frozenset(sentence2)

        numerator = 0.0
        for term in common_words:
            numerator += tf1[term]*tf2[term] * idf_metrics[term]**2

        denominator1 = sum((tf1[t]*idf_metrics[t])**2 for t in sentence1)
        denominator2 = sum((tf2[t]*idf_metrics[t])**2 for t in sentence2)

        if denominator1 > 0 and denominator2 > 0:
            return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))
        else:
            return 0.0
