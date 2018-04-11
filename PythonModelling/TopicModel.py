from gensim import corpora, models, similarities
import pandas as pd

class TopicModel:
    def __init__(self, number_topics = 10, number_terms = 10):
        self._number_topics = number_topics
        self._number_terms = number_terms

    def create_model(self, tokenized_tweets):
        return

    def get_topics(self):
        topics = [self.__get_term_from_topic(topic[0], topic[1]) for topic in self.model.print_topics(self._number_topics, self._number_terms)]        
        return pd.concat(topics, ignore_index = True)

    def __get_term_from_topic(self, topic_id, topic):
        return pd.DataFrame([{"id": topic_id + 1, "term": term.split("*")[1].replace('"',""), "weight": term.split("*")[0]} for term in topic.split(" + ")])
    
    def create_dictionary(self, tokenized_tweets):
        return corpora.Dictionary(tokenized_tweets)
        #dictionary.save('tweets.dict')
    
    def create_corpus(self, tokenized_tweets, dictionary):
        return [dictionary.doc2bow(text) for text in tokenized_tweets]
        #corpora.MmCorpus.serialize('tweets.mm', self.corpus)    