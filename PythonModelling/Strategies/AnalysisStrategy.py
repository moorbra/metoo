class AnalysisStrategy:
    def __init__(self):
        self._number_topics = 10
        self._number_terms = 10
        self._tokens_column = "tokens"
        self._text_column = "text"
        self._token_frequency_not_below = 20
        self._token_frequency_not_above_percent = .5

    @property
    def token_frequency_not_above_percent(self):
        return self._token_frequency_not_above_percent

    @token_frequency_not_above_percent.setter
    def token_frequency_not_above_percent(self, value):
        self._token_frequency_not_above_percent = value        

    @property
    def token_frequency_not_below(self):
        return self._token_frequency_not_below

    @token_frequency_not_below.setter
    def token_frequency_not_below(self, value):
        self._token_frequency_not_below = value        

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

    @property
    def tokens_column(self):
        return self._tokens_column

    @tokens_column.setter
    def tokens_column(self, value):
        self._tokens_column = value

    @property
    def text_column(self):
        return self._text_column

    @text_column.setter
    def text_column(self, value):
        self._text_column = value                