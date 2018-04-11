from TopicModel import TopicModel
from gensim.models import LdaModel

class TaskLdaModel(TopicModel):

    def __init__(self, number_topics = 10, number_terms = 10, number_passes = 50):
        super().__init__(number_topics, number_terms)
        self._number_passes = number_passes

    def create_model(self, tokenized_tweets):        
        dictionary = self.create_dictionary(tokenized_tweets)
        corpus = self.create_corpus(tokenized_tweets, dictionary)
        self.model = LdaModel(corpus, id2word = dictionary, num_topics = self._number_topics, passes = self._number_passes)

