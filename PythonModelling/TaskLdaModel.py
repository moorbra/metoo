from Task import Task
from TopicModel import TopicModel
from gensim.models import LdaModel
from Strategies import LDAStrategy
import pandas as pd

class TaskLdaModel(TopicModel, Task):

    def __init__(self, lda_strategy):
        super().__init__(lda_strategy)

    def create_model(self, documents_data_frame):        
        dictionary = self.create_dictionary(documents_data_frame[self.strategy.tokens_column])
        self.corpus = self.create_corpus(documents_data_frame[self.strategy.tokens_column], dictionary)
        self.model = LdaModel(self.corpus, id2word = dictionary, num_topics = self.strategy.number_topics, passes = self.strategy.number_passes)

    def get_document_topics(self):
        document_topics = [
            { 
                "docid": t['docid'], 
                "prominantTopicId": t['topics'][0][0],
                "prominantTopicProbability": t['topics'][0][1],
                "topics":t['topics']
            }
            for t in
            [
                { 
                    "docid":i,
                    "topics":self.model.get_document_topics(bow=t, per_word_topics=False, minimum_probability=self.strategy.minimum_probability)
                } 
                for (i,t) in enumerate(self.corpus)
            ] if len(t['topics']) > 0
        ]
        return pd.DataFrame(document_topics)

    def count_topic_occurances(self, document_topics_data_frame, include_topic_terms=True):
        df = document_topics_data_frame.groupby(['prominantTopicId']).size().reset_index(name='count')
        df.columns = ["TopicId", "Count"]
        if include_topic_terms:
            df["Terms"] = df["TopicId"].apply(lambda t: self.model.print_topic(t, self.strategy.number_terms))

        return df

