class TokenizationStrategy:
    def __init__(self):
        self._custom_stop_words = set([])
        self._custom_synonyms = set([])
        self._use_stemmer = False
        self._strip_handles = False
        self._reduce_length = False
        self._minimum_term_length = 2

    @property
    def custom_stop_words(self):
        return self._custom_stop_words

    @custom_stop_words.setter
    def custom_stop_words(self, value):
        self._custom_stop_words = value

    @property
    def custom_synonyms(self):
        return self._custom_synonyms

    @custom_synonyms.setter
    def custom_synonyms(self, value):
        self._custom_synonyms = value

    @property
    def use_stemmer(self):
        return self._use_stemmer

    @use_stemmer.setter
    def use_stemmer(self, value):
        self._use_stemmer = value

    @property
    def strip_handles(self):
        return self._strip_handles

    @strip_handles.setter
    def strip_handles(self, value):
        self._strip_handles = value

    @property
    def reduce_length(self):
        return self._reduce_length

    @reduce_length.setter
    def reduce_length(self, value):
        self._reduce_length = value   

    @property
    def minimum_term_length(self):
        return self._minimum_term_length

    @minimum_term_length.setter
    def minimum_term_length(self, value):
        self._minimum_term_length = value        