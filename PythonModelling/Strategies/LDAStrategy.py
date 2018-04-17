from Strategies.AnalysisStrategy import AnalysisStrategy

class LDAStrategy(AnalysisStrategy):
    def __init__(self):
        self._number_passes = 50
        self._minimum_probability = .5

    @property
    def number_passes(self):
        return self._number_passes

    @number_passes.setter
    def number_passes(self, value):
        self._number_passes = value

    @property
    def minimum_probability(self):
        return self._minimum_probability

    @minimum_probability.setter
    def minimum_probability(self, value):
        self._minimum_probability = value        