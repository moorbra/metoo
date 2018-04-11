import pandas as pd
import os
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

class TaskTokenize:

    def __init__(self, custom_stop_words = []):
        self.tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
        self.__create_stop_words(custom_stop_words = custom_stop_words)

    def tokenize_tweets(self, tweets_data_frame, text_column="tweet"):
        return tweets_data_frame.assign(tokens = tweets_data_frame[text_column].apply(lambda t: self.__tokenize_tweet(t)))

    def save_tokens(self, tokenized_tweets, path_to_save, filename):
        pivoted_tokens = [ self.__pivot_tokens(getattr(row, "id"), getattr(row, "tokens")) for row in tokenized_tweets.itertuples()]
        pivoted_tokens = pd.concat(pivoted_tokens, ignore_index=True)
        pivoted_tokens.to_csv(os.path.join(path_to_save, filename), index = False)

    def __pivot_tokens(self, id, tokens):
        return pd.DataFrame([{ "id": id, "token": token } for token in tokens])

    def __create_stop_words(self, custom_stop_words):        
        stop_words = set(stopwords.words('english'))
        self.stop_words = stop_words.union(custom_stop_words)

    def __tokenize_tweet(self, tweet):
        tokens = self.tokenizer.tokenize(tweet)
        tokens = self.__remove_stop_words(tokens)
        tokens = self.__apply_synonyms(tokens)
        return tokens

    
    def __remove_stop_words(self, tokens):        
        tokens = [t for t in tokens if not t in self.stop_words]
        return tokens

    def __apply_synonyms(self, tokens):
        return tokens