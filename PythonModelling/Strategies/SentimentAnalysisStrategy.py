class SentimentAnalysisStrategy:
    def __init__(self):
        self._text_column = "tweet"
        self._sentiment_column = "sentiment"

    @property
    def text_column(self):
        return self._text_column

    @text_column.setter
    def text_column(self, value):
        self._text_column = value

    @property
    def sentiment_column(self):
        return self._text_column

    @sentiment_column.setter
    def sentiment_column(self, value):
        self._text_column = value        