from Strategies.AnalysisStrategy import AnalysisStrategy

class LDAStrategy(AnalysisStrategy):
    def __init__(self):
        super().__init__()
        self._number_passes = 50
        self._minimum_document_topic_probability = .5
        self._minimum_term_topic_probability = .5
        self._random_state_seed = 1234
        self._eval_model_every = None
        self._chunksize = 2000
        self._update_model_every = 1
        self._training_iterations = 50
        self._eta = 'auto'
        self._alpha = 'auto'
        self._phrases_min_count = 20

    @property
    def phrases_min_count(self):
        return self._phrases_min_count

    @phrases_min_count.setter
    def phrases_min_count(self, value):
        self._phrases_min_count = value

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    @property
    def eta(self):
        return self._eta

    @eta.setter
    def training_iterations(self, value):
        self._eta = value

    @property
    def training_iterations(self):
        return self._training_iterations

    @training_iterations.setter
    def training_iterations(self, value):
        self._training_iterations = value

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

    @property
    def eval_model_every(self):
        return self._eval_model_every

    @eval_model_every.setter
    def eval_model_every(self, value):
        self._eval_model_every = value         

    @property
    def chunksize(self):
        return self._chunksize

    @chunksize.setter
    def chunksize(self, value):
        self._chunksize = value

    @property
    def update_model_every(self):
        return self._update_model_every

    @update_model_every.setter
    def update_model_every(self, value):
        self._update_model_every = value        