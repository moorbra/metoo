from Task import Task
from textblob import TextBlob

class TaskSentimentAnalysis(Task):

    def __init__(self, sentiment_strategy):
        super().__init__()
        self._strategy = sentiment_strategy

    def compute_sentiment(self, tweets_data_frame):
        self.logger.info("Computing sentiment for each document.")
        tweets_data_frame["sentiment"] = tweets_data_frame["tweet"].apply(lambda t: self.__get_tweet_sentiment(t))
        return tweets_data_frame

    def __get_tweet_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        sentiment = 'negative'
        if analysis.sentiment.polarity > 0:
            sentiment = "positive"
        elif analysis.sentiment.polarity == 0:
            sentiment = "neutral"

        return { "sentiment": sentiment, "polarity": analysis.sentiment.polarity }

        
