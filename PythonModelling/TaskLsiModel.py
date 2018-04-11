from TopicModel import TopicModel
from gensim.models import LsiModel

class TaskLsiModel(TopicModel):

    def create_model(self, tokenized_tweets):        
        dictionary = self.create_dictionary(tokenized_tweets)
        corpus = self.create_corpus(tokenized_tweets, dictionary)
        self.model = LsiModel(corpus, id2word = dictionary, num_topics = self._number_topics)

