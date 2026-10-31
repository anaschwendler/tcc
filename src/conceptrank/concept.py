"""ConceptRank: sentence similarity is the WIVES similarity (Loh et al.).

Ported from ConceptSummarizer in archive/ConceptRank.ipynb, which in turn was
ported from docs/reference/wives_similarity.java.

Known deviation from the Java original, kept on purpose so results match the
thesis: the Java code weights each common word by its weight in each of the
two documents, while this port uses the word length (len(term)) as a running
maximum, and wordWeightMin never leaves 0. See results/legacy/README.md.

Because of that running maximum, the score depends on the order in which
common_words is iterated. The thesis ran on Python 2, where that order was
fixed but arbitrary; Python 3 randomizes string hashing, so it changed between
runs. Common words are now iterated in sorted order, which makes the output
deterministic but different from the 2016 summaries.
"""

import math

from conceptrank.graph import GraphSummarizer

EPSILON = 0.0000000000000001


class ConceptSummarizer(GraphSummarizer):
    @staticmethod
    def compute_distance(sentence1, sentence2, tf1, tf2, idf_metrics):
        result = 0

        # identify common words
        common_words = frozenset(sentence1) & frozenset(sentence2)

        if len(sentence1) > len(sentence2):
            maxLen = len(sentence1)
            minLen = len(sentence2)
        else:
            maxLen = len(sentence2)
            minLen = len(sentence1)

        # calculates similarity
        wordWeightMax = 0
        wordWeightMin = 0
        for term in sorted(common_words):
            if wordWeightMax < len(term):
                wordWeightMax = len(term)
            if wordWeightMin > len(term):
                wordWeightMin = len(term)
            negationWordWeightMax = 1 - wordWeightMax
            negationWordWeightMin = 1 - wordWeightMin

            c1 = 1 if wordWeightMin == 0 else wordWeightMax / wordWeightMin
            c2 = 1 if wordWeightMax == 0 else wordWeightMin / wordWeightMax
            c3 = 1 if negationWordWeightMin == 0 else negationWordWeightMax / negationWordWeightMin
            c4 = 1 if negationWordWeightMax == 0 else negationWordWeightMin / negationWordWeightMax

            m1 = min(min(c1, c2), 1)
            m2 = min(min(c3, c4), 1)

            result += 0.5*(m1+m2)

        return math.fabs(result / (minLen + maxLen - len(common_words) + EPSILON))


class WivesSummarizer(GraphSummarizer):
    """ConceptRank with the WIVES similarity as written in the Java original.

    Each common word is weighted by its normalized term frequency in each
    sentence (tf / max tf, so between 0 and 1), which GraphSummarizer already
    computes. The Java class that defined the weight (BagOfWords) is not
    available, so this is an assumption. The denominator counts distinct words,
    as the Java BagOfWords did. The Java code pointed both of its "min" and
    "max" documents at the same one when the two had the same size; the
    formula is symmetric, so this version does not need that distinction.
    """

    @staticmethod
    def compute_distance(sentence1, sentence2, tf1, tf2, idf_metrics):
        words1, words2 = frozenset(sentence1), frozenset(sentence2)
        common_words = words1 & words2

        result = 0.0
        for term in common_words:
            weight1, weight2 = tf1[term], tf2[term]
            negation1, negation2 = 1 - weight1, 1 - weight2

            c1 = 1 if weight1 == 0 else weight2 / weight1
            c2 = 1 if weight2 == 0 else weight1 / weight2
            c3 = 1 if negation1 == 0 else negation2 / negation1
            c4 = 1 if negation2 == 0 else negation1 / negation2

            result += 0.5 * (min(c1, c2, 1) + min(c3, c4, 1))

        return result / (len(words1) + len(words2) - len(common_words) + EPSILON)
