class TokenizationStrategy:
    def __init__(self):
        self._use_stemmer = False
        self._strip_handles = False
        self._reduce_length = False
        self._minimum_term_length = 2
        self._custom_stop_words_file = ""
        self._synonyms_file = ""
        self._minimum_term_frequency = 1

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

    @property
    def custom_stop_words_file(self):
        return self._custom_stop_words_file

    @custom_stop_words_file.setter
    def custom_stop_words_file(self, value):
        self._custom_stop_words_file = value        

    @property
    def synonyms_file(self):
        return self._synonyms_file

    @synonyms_file.setter
    def synonyms_file(self, value):
        self._synonyms_file = value

    @property
    def minimum_term_frequency(self):
        return self._minimum_term_frequency

    @minimum_term_frequency.setter
    def minimum_term_frequency(self, value):
        self._minimum_term_frequency = value        