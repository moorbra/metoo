from Task import Task
import pandas as pd
from Strategies import TokenizationStrategy
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from pprintpp import pprint as pp
import itertools

class TaskTokenize(Task):

    def __init__(self, tokenization_strategy):
        self._strategy = tokenization_strategy
        self._tokenizer = TweetTokenizer(strip_handles=self._strategy.strip_handles, reduce_len=self._strategy.reduce_length)        
        self._stop_words = None
        self._synonyms = {}
        self._term_frequencies = None
        self._infrequent_terms = None

    @property
    def stop_words(self):
        return self._stop_words

    @property
    def synonyms(self):
        return self._synonyms

    @property
    def term_frequencies(self):
        return self._term_frequencies 

    @property
    def infrequent_terms(self):
        return self._infrequent_terms

    def tokenize_tweets(self, tweets_data_frame, text_column="tweet"):
        self.__create_stop_words()
        self.__create_synonyms()
        tokens = tweets_data_frame[text_column].apply(lambda t: self.__tokenize_tweet(t))
        self._term_frequencies = self.__compute_term_frequencies(tokens)
        tokens = self.__remove_infrequent_tokens(tokens, self._term_frequencies)
        return tweets_data_frame.assign(tokens = tokens)

    def __remove_infrequent_tokens(self, tokens, term_frequencies):
        if(self._strategy.minimum_term_frequency > 1):            
            self._infrequent_terms = self.__get_infrequent_terms(term_frequencies)
            inf = set(self._infrequent_terms["token"])
            tokens = [list(filter(lambda x: x not in inf, row[1])) for row in tokens.iteritems()]

        return tokens

    def __get_infrequent_terms(self, term_frequencies):
        return term_frequencies.query(f"count<={self._strategy.minimum_term_frequency}").sort_values(by=["count"])

    def __compute_term_frequencies(self, tokens):
        pivoted_tokens = [row[1] for row in tokens.iteritems() if len(row[1]) > 0]        
        concatenated_tokens = pd.DataFrame(list(itertools.chain(*pivoted_tokens)))
        term_counts = concatenated_tokens[0].value_counts().reset_index()
        term_counts.columns = ["token", "count"]
        return term_counts

    def __create_synonyms(self):
        if(self._strategy.synonyms_file):
            synonyms = pd.read_csv(self._strategy.synonyms_file)
            self._synonyms = dict(synonyms[["word", "replacement"]].values)

    def __create_stop_words(self):        
        nltk_english_stop_words = self.__load_nltk_english_stopwords()
        custom_stop_words = self.__load_custom_stop_words()
        merged_stop_words = pd.concat([nltk_english_stop_words, custom_stop_words])
        self._stop_words = merged_stop_words["word"].tolist()

    def __load_nltk_english_stopwords(self):
        stop_words = pd.DataFrame(stopwords.words('english'))
        stop_words.columns = ["word"]
        return stop_words

    def __load_custom_stop_words(self):
        if(self._strategy._custom_stop_words_file):
            return pd.read_csv(self._strategy.custom_stop_words_file)

        return pd.DataFrame()

    def __tokenize_tweet(self, tweet):
        tokens = self._tokenizer.tokenize(tweet)
        tokens = self.__apply_synonyms(tokens)
        tokens = self.__remove_stop_words(tokens)
        tokens = self.__remove_too_short_tokens(tokens)        
        return tokens

    def __remove_too_short_tokens(self, tokens):
        return [t for t in tokens if len(t) >= self._strategy.minimum_term_length]
    
    def __remove_stop_words(self, tokens):     
        return [t for t in tokens if t not in self._stop_words]   

    def __apply_synonyms(self, tokens):
        return [self._synonyms.get(t,t) for t in tokens]