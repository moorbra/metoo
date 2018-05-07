from Task import Task
from textblob import TextBlob

class TaskSentimentAnalysis(Task):

    def __init__(self, sentiment_strategy):
        super().__init__()
        self._strategy = sentiment_strategy

    def compute_sentiment(self, documents_data_frame):
        self.logger.info("Computing sentiment for each document.")
        documents_data_frame["raw_sentiment"] = documents_data_frame[self._strategy.text_column].apply(lambda t: self.__get_tweet_sentiment(t))
        documents_data_frame["sentiment"] = documents_data_frame["raw_sentiment"].apply(lambda t : t.get("sentiment"))
        documents_data_frame["polarity"] = documents_data_frame["raw_sentiment"].apply(lambda t : t.get("polarity"))
        documents_data_frame.drop(columns=['raw_sentiment'])
        return documents_data_frame

    def compute_aggregrate_sentiment(self, documents_data_frame):
        self.logger.info("Aggregating sentiment for corpus.")
        return documents_data_frame.groupby(['sentiment'])['sentiment', 'polarity'].agg(['count', 'mean', 'median', 'std', 'var', 'min', 'max'])
        #return documents_data_frame[['sentiment','ploarity']]
        # sentiments = dict(documents_data_frame[self._strategy.sentiment_column])
        # sentiments = [sentiments[k] for k,v in sentiments]
        # return sentiments

    def __get_tweet_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        sentiment = 'negative'
        if analysis.sentiment.polarity > 0:
            sentiment = "positive"
        elif analysis.sentiment.polarity == 0:
            sentiment = "neutral"

        return { "sentiment": sentiment, "polarity": analysis.sentiment.polarity }

        
