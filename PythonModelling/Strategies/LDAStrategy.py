from Strategies.AnalysisStrategy import AnalysisStrategy

class LDAStrategy(AnalysisStrategy):
    def __init__(self):
        self._number_passes = 50
        self._minimum_document_topic_probability = .5
        self._minimum_term_topic_probability = .5
        self._random_state_seed = 1234

    @property
    def random_state_seed(self):
        return self._random_state_seed

    @random_state_seed.setter
    def random_state_seed(self, value):
        self._random_state_seed = value

    @property
    def number_passes(self):
        return self._number_passes

    @number_passes.setter
    def number_passes(self, value):
        self._number_passes = value

    @property
    def minimum_document_topic_probability(self):
        return self._minimum_document_topic_probability

    @minimum_document_topic_probability.setter
    def minimum_document_topic_probability(self, value):
        self._minimum_document_topic_probability = value

    @property
    def minimum_term_topic_probability(self):
        return self._minimum_term_topic_probability

    @minimum_term_topic_probability.setter
    def minimum_term_topic_probability(self, value):
        self._minimum_term_topic_probability = value                