from Task import Task
import pandas as pd
from Strategies import TokenizationStrategy
from nltk.tokenize import TweetTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from pprintpp import pprint as pp
import itertools

class TaskTokenize(Task):

    def __init__(self, tokenization_strategy):
        super().__init__()
        self._strategy = tokenization_strategy
        self._tokenizer = TweetTokenizer(strip_handles=self._strategy.strip_handles, reduce_len=self._strategy.reduce_length, preserve_case=False)        
        self._stop_words = None
        self._synonyms = {}
        self._token_frequencies = pd.DataFrame()
        self._infrequent_tokens = pd.DataFrame()
        self._documents_without_tokens = pd.DataFrame()
        self._lemmatizer = WordNetLemmatizer()

    @property
    def stop_words(self):
        return self._stop_words

    @property
    def synonyms(self):
        return self._synonyms

    @property
    def token_frequencies(self):
        return self._token_frequencies 

    @property
    def infrequent_tokens(self):
        return self._infrequent_tokens

    @property
    def documents_without_tokens(self):
        return self._documents_without_tokens

    def tokenize_tweets(self, tweets_data_frame, text_column="tweet"):
        self.logger.info("Beginning tokenization.")
        self.__create_stop_words()
        self.__create_synonyms()        
        tokens = self.__get_tokens(tweets_data_frame, text_column)
        self._token_frequencies = self.__compute_token_frequencies(tokens)        
        tokens = self.__remove_infrequent_tokens(tokens, self._token_frequencies)
        tweets_data_frame = self.__assign_tokens(tweets_data_frame, tokens)
        tweets_data_frame = self.__count_tokens_per_document(tweets_data_frame)
        self._find_documents_without_tokens(tweets_data_frame)
        tweets_data_frame = self.__remove_documents_without_tokens(tweets_data_frame)
        return tweets_data_frame

    def __remove_documents_without_tokens(self, documents_data_frame):        
        documents_with_tokens = documents_data_frame.query("tokencount>0")
        self.logger.info(f"Found {len(documents_with_tokens)} documents with tokens.")
        return documents_with_tokens

    def _find_documents_without_tokens(self, documents_data_frame):
        self._documents_without_tokens = documents_data_frame.query("tokencount==0")
        self.logger.info(f"Found {len(self.documents_without_tokens)} documents without tokens.")

    def __count_tokens_per_document(self, documents_data_frame):
        token_counts = documents_data_frame["tokens"].apply(lambda r: len(r))
        return documents_data_frame.assign(tokencount = token_counts)

    def __assign_tokens(self, documents_data_frame, tokens):
        return documents_data_frame.assign(tokens = tokens)

    def __get_tokens(self, documents_data_frame, text_column="tweet"):
        self.logger.info(f"Tokenizing {len(documents_data_frame[text_column])} documents.")
        return documents_data_frame[text_column].apply(lambda t: self.__tokenize_tweet(t))

    def __remove_infrequent_tokens(self, tokens, token_frequencies):
        if(self._strategy.minimum_term_frequency > 1):            
            self._infrequent_tokens = self.__get_infrequent_tokens(token_frequencies)
            self.logger.info(f"Found {len(self._infrequent_tokens)} infrequent tokens.")
            inf = set(self._infrequent_tokens["token"])
            self.logger.info("Removing infrequent tokens from each document.")
            tokens = [list(filter(lambda x: x not in inf, row[1])) for row in tokens.iteritems()]

        return tokens

    def __get_infrequent_tokens(self, token_frequencies):
        self.logger.info("Identifying infrequent tokens.")
        return token_frequencies.query(f"count<={self._strategy.minimum_term_frequency}").sort_values(by=["count"])

    def __compute_token_frequencies(self, tokens):
        self.logger.info("Computing token frequencies")
        pivoted_tokens = [row[1] for row in tokens.iteritems() if len(row[1]) > 0]        
        concatenated_tokens = pd.DataFrame(list(itertools.chain(*pivoted_tokens)))
        term_counts = concatenated_tokens[0].value_counts().reset_index()
        term_counts.columns = ["token", "count"]
        return term_counts

    def __create_synonyms(self):
        if(self._strategy.synonyms_file):
            self.logger.info("Creating synonyms list.")
            synonyms = pd.read_csv(self._strategy.synonyms_file)
            self.logger.info(f"Created {len(synonyms)} synonyms.")
            self._synonyms = dict(synonyms[["word", "replacement"]].values)

    def __create_stop_words(self):       
        self.logger.info("Preparing stop words.") 
        nltk_english_stop_words = self.__load_nltk_english_stopwords()
        custom_stop_words = self.__load_custom_stop_words()
        merged_stop_words = pd.concat([nltk_english_stop_words, custom_stop_words])
        self.logger.info(f"Merged {len(custom_stop_words)} custom stop words with {len(nltk_english_stop_words)} NLTK english stop words. ")        
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
        tokens = self.__lemmatize_tokens(tokens) 
        tokens = self.__remove_too_short_tokens(tokens)               
        return tokens

    def __lemmatize_tokens(self, tokens):
        return [self._lemmatizer.lemmatize(t) for t in tokens]

    def __remove_too_short_tokens(self, tokens):
        return [t for t in tokens if len(t) >= self._strategy.minimum_term_length]
    
    def __remove_stop_words(self, tokens):     
        return [t for t in tokens if t not in self._stop_words]   

    def __apply_synonyms(self, tokens):
        return [self._synonyms.get(t,t) for t in tokens]