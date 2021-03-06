from gensim import corpora, models, similarities
import pandas as pd
from Strategies import AnalysisStrategy

class TopicModel:
    def __init__(self, analysisStrategy):
        self._strategy = analysisStrategy
        self._model = None
        self._corpus = None
        self._dictionary = None

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
    def dictionary(self):
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        self._dictionary = value

    @property
    def strategy(self):
        return self._strategy

    def create_model(self, documents_data_frame):
        return

    def create_tfidf_model(self, corpus):
        return models.TfidfModel(corpus)

    def get_topics(self):
        #topics = [self.__get_term_from_topic(topic[0], topic[1]) for topic in self._model.print_topics(self.strategy.number_topics, self.strategy.number_terms)]        
        topics = self._model.print_topics(self.strategy.number_topics, self.strategy.number_terms)
        topics = pd.DataFrame(topics)
        topics.columns = ["id", "topic"]
        return pd.DataFrame(topics)

    def __get_term_from_topic(self, topic_id, topic):
        return pd.DataFrame([{"id": topic_id + 1, "term": term.split("*")[1].replace('"',""), "weight": term.split("*")[0]} for term in topic.split(" + ")])
    
    def create_dictionary(self, document_tokens_list):
        dictionary = corpora.Dictionary(document_tokens_list)
        dictionary.filter_extremes(no_below=self.strategy.token_frequency_not_below, no_above=self.strategy.token_frequency_not_above_percent)
        return dictionary
    
    def create_corpus(self, document_tokens_list, dictionary):
        return [dictionary.doc2bow(token_list) for token_list in document_tokens_list]
        
    def plot_topics(self, topics_data_frame):
        return 
