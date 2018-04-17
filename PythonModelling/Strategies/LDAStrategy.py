from Strategies.AnalysisStrategy import AnalysisStrategy

class LDAStrategy(AnalysisStrategy):
    def __init__(self):
        self._number_passes = 50

    @property
    def number_passes(self):
        return self._number_passes

    @number_passes.setter
    def number_passes(self, value):
        self._number_passes = value