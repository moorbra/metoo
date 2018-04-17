from Task import Task
import pandas as pd
from Strategies import TokenizationStrategy
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

class TaskTokenize(Task):

    def __init__(self, tokenization_strategy):
        self._strategy = tokenization_strategy
        self.tokenizer = TweetTokenizer(strip_handles=self._strategy.strip_handles, reduce_len=self._strategy.reduce_length)        
        self._stop_words = None

    @property
    def stop_words(self):
        return self._stop_words

    def tokenize_tweets(self, tweets_data_frame, text_column="tweet"):
        self.__create_stop_words()
        return tweets_data_frame.assign(tokens = tweets_data_frame[text_column].apply(lambda t: self.__tokenize_tweet(t)))

    def pivot_tokens(self, tokenized_tweets, path_to_save, filename):
        pivoted_tokens = [ self.__pivot_tokens(getattr(row, "id"), getattr(row, "tokens")) for row in tokenized_tweets.itertuples()]
        return pd.concat(pivoted_tokens, ignore_index=True)
        

    def __pivot_tokens(self, id, tokens):
        return pd.DataFrame([{ "id": id, "token": token } for token in tokens])

    def __create_stop_words(self):        
        stop_words = set(stopwords.words('english'))
        self._stop_words = stop_words.union(self._strategy.custom_stop_words)

    def __tokenize_tweet(self, tweet):
        tokens = self.tokenizer.tokenize(tweet)
        tokens = self.__remove_stop_words(tokens)
        tokens = self.__apply_synonyms(tokens)
        return tokens

    
    def __remove_stop_words(self, tokens):        
        tokens = [t for t in tokens if not t in self._stop_words]
        return tokens

    def __apply_synonyms(self, tokens):
        return tokens