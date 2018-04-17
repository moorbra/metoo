class AnalysisStrategy:
    def __init__(self):
        self._number_topics = 10
        self._number_terms = 10

    @property
    def number_topics(self):
        return self._number_topics

    @number_topics.setter
    def number_topics(self, value):
        self._number_topics = value

    @property
    def number_terms(self):
        return self._number_terms

    @number_terms.setter
    def number_terms(self, value):
        self._number_terms = value        