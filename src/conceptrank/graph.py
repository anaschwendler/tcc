"""Graph-based sentence ranking shared by LexRank and ConceptRank.

Ported from the BetaSummarizer / ConceptSummarizer classes in the legacy
notebooks (archive/BetaRank.ipynb, archive/ConceptRank.ipynb), which were copies of
sumy's LexRank. Behaviour is kept as it was; only the similarity function
differs between subclasses.
"""

import math
from collections import Counter

import numpy
from sumy.summarizers._summarizer import AbstractSummarizer


class GraphSummarizer(AbstractSummarizer):
    threshold = 0.1
    epsilon = 0.1
    _stop_words = frozenset()

    @property
    def stop_words(self):
        return self._stop_words

    @stop_words.setter
    def stop_words(self, words):
        self._stop_words = frozenset(map(self.normalize_word, words))

    def __call__(self, document, sentences_count):
        ratings = self.rate_sentences(document)
        if not ratings:
            return tuple()

        return self._get_best_sentences(document.sentences, sentences_count, ratings)

    def rate_sentences(self, document):
        """{sentence: centrality score}. Repeated sentences share one entry."""
        sentences_words = [self._to_words_set(s) for s in document.sentences]
        if not sentences_words:
            return {}

        tf_metrics = self._compute_tf(sentences_words)
        idf_metrics = self._compute_idf(sentences_words)

        matrix = self._create_matrix(sentences_words, self.threshold, tf_metrics, idf_metrics)
        scores = self.power_method(matrix, self.epsilon)
        return dict(zip(document.sentences, scores))

    def scores_and_similarities(self, document):
        """Centrality score of each sentence and the n×n similarity matrix
        before thresholding, both indexed by sentence position."""
        sentences_words = [self._to_words_set(s) for s in document.sentences]
        tf_metrics = self._compute_tf(sentences_words)
        idf_metrics = self._compute_idf(sentences_words)

        similarities = numpy.array([
            [self.compute_distance(words1, words2, tf1, tf2, idf_metrics)
             for words2, tf2 in zip(sentences_words, tf_metrics)]
            for words1, tf1 in zip(sentences_words, tf_metrics)
        ])
        matrix = self._create_matrix(sentences_words, self.threshold, tf_metrics, idf_metrics)
        return self.power_method(matrix, self.epsilon), similarities

    @staticmethod
    def compute_distance(sentence1, sentence2, tf1, tf2, idf_metrics):
        raise NotImplementedError

    def _to_words_set(self, sentence):
        words = map(self.normalize_word, sentence.words)
        return [self.stem_word(w) for w in words if w not in self._stop_words]

    def _compute_tf(self, sentences):
        tf_values = map(Counter, sentences)

        tf_metrics = []
        for sentence in tf_values:
            metrics = {}
            max_tf = self._find_tf_max(sentence)

            for term, tf in sentence.items():
                metrics[term] = tf / max_tf

            tf_metrics.append(metrics)

        return tf_metrics

    @staticmethod
    def _find_tf_max(terms):
        return max(terms.values()) if terms else 1

    @staticmethod
    def _compute_idf(sentences):
        idf_metrics = {}
        sentences_count = len(sentences)

        for sentence in sentences:
            for term in sentence:
                if term not in idf_metrics:
                    n_j = sum(1 for s in sentences if term in s)
                    idf_metrics[term] = math.log(sentences_count / (1 + n_j))

        return idf_metrics

    def _create_matrix(self, sentences, threshold, tf_metrics, idf_metrics):
        """
        Creates matrix of shape |sentences|×|sentences|.
        """
        sentences_count = len(sentences)
        matrix = numpy.zeros((sentences_count, sentences_count))
        degrees = numpy.zeros((sentences_count, ))

        for row, (sentence1, tf1) in enumerate(zip(sentences, tf_metrics)):
            for col, (sentence2, tf2) in enumerate(zip(sentences, tf_metrics)):
                matrix[row, col] = self.compute_distance(sentence1, sentence2, tf1, tf2, idf_metrics)

                if matrix[row, col] > threshold:
                    matrix[row, col] = 1.0
                    degrees[row] += 1
                else:
                    matrix[row, col] = 0

        for row in range(sentences_count):
            for col in range(sentences_count):
                if degrees[row] == 0:
                    degrees[row] = 1

                matrix[row][col] = matrix[row][col] / degrees[row]

        return matrix

    @staticmethod
    def power_method(matrix, epsilon):
        transposed_matrix = matrix.T
        sentences_count = len(matrix)
        p_vector = numpy.array([1.0 / sentences_count] * sentences_count)
        lambda_val = 1.0

        while lambda_val > epsilon:
            next_p = numpy.dot(transposed_matrix, p_vector)
            lambda_val = numpy.linalg.norm(numpy.subtract(next_p, p_vector))
            p_vector = next_p

        return p_vector
