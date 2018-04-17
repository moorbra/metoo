from gensim import corpora, models, similarities
import pandas as pd
from Strategies import AnalysisStrategy

class TopicModel:
    def __init__(self, analysisStrategy):
        self._strategy = analysisStrategy
        self._model = None
        self._corpus = None

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def corpus(self):
        return self._corpus

    @corpus.setter
    def corpus(self, value):
        self._corpus = value

    @property
    def strategy(self):
        return self._strategy


    def create_model(self, tokenized_tweets):
        return

    def create_tfidf_model(self, corpus):
        return models.TfidfModel(corpus)

    def get_topics(self):
        topics = [self.__get_term_from_topic(topic[0], topic[1]) for topic in self._model.print_topics(self._strategy.number_topics, self._strategy.number_terms)]        
        return pd.concat(topics, ignore_index = True)

    def __get_term_from_topic(self, topic_id, topic):
        return pd.DataFrame([{"id": topic_id + 1, "term": term.split("*")[1].replace('"',""), "weight": term.split("*")[0]} for term in topic.split(" + ")])
    
    def create_dictionary(self, tokenized_tweets):
        return corpora.Dictionary(tokenized_tweets)
    
    def create_corpus(self, tokenized_tweets, dictionary):
        return [dictionary.doc2bow(text) for text in tokenized_tweets]
        
    def plot_topics(self, topics_data_frame):
        return 