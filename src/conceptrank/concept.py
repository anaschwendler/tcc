"""ConceptRank: sentence similarity is the WIVES similarity (Loh et al.).

Ported from ConceptSummarizer in src/ConceptRank.ipynb, which in turn was
ported from docs/reference/wives_similarity.java.

Known deviation from the Java original, kept on purpose so results match the
thesis: the Java code weights each common word by its weight in each of the
two documents, while this port uses the word length (len(term)) as a running
maximum, and wordWeightMin never leaves 0. See results/legacy/README.md.

Because of that running maximum, the score depends on the order in which
common_words is iterated. Python 3 randomizes string hashing, so summaries
change between runs unless PYTHONHASHSEED is fixed.
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
        for term in common_words:
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
