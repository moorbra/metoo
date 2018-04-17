from Task import Task
from TopicModel import TopicModel
from gensim.models import LdaModel
from Strategies import LDAStrategy

class TaskLdaModel(TopicModel, Task):

    def __init__(self, lda_strategy):
        super().__init__(lda_strategy)

    def create_model(self, tokenized_tweets):        
        dictionary = self.create_dictionary(tokenized_tweets)
        self.corpus = self.create_corpus(tokenized_tweets, dictionary)
        self.model = LdaModel(self.corpus, id2word = dictionary, num_topics = self.strategy.number_topics, passes = self.strategy.number_passes)

    def get_document_topics(self):
        return [{"document":t, "topics":self.model.get_document_topics(bow=t, per_word_topics=False, minimum_probability=self.strategy.minimum_probability)} for t in self.corpus]
