from Task import Task
from TopicModel import TopicModel
from gensim.models import LdaModel
from gensim.models import CoherenceModel
from Strategies import LDAStrategy
import pandas as pd

class TaskLdaModel(TopicModel, Task):

    def __init__(self, lda_strategy):
        super().__init__(lda_strategy)
        self._texts = None

    def create_model(self, documents_data_frame):
        self._texts = documents_data_frame[self.strategy.tokens_column]
        self.dictionary = self.create_dictionary(documents_data_frame[self.strategy.tokens_column])
        self.corpus = self.create_corpus(documents_data_frame[self.strategy.tokens_column], self.dictionary)
        self.model = LdaModel(self.corpus, 
            id2word = self.dictionary, 
            num_topics = self.strategy.number_topics, 
            passes = self.strategy.number_passes, 
            random_state = self.strategy.random_state_seed, 
            eval_every = self.strategy.eval_model_every,
            chunksize = self.strategy.chunksize,
            update_every = self.strategy.update_model_every,
            iterations = self.strategy.training_iterations)

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
                    "topics":self.model.get_document_topics(bow=t, per_word_topics=False, minimum_probability=self.strategy.minimum_document_topic_probability)
                } 
                for (i,t) in enumerate(self.corpus)
            ] if len(t['topics']) > 0
        ]
        return pd.DataFrame(document_topics)

    def count_document_topic_occurances(self, document_topics_data_frame, include_topic_terms=True):
        df = document_topics_data_frame.groupby(['prominantTopicId']).size().reset_index(name='Count')
        df.columns = ["TopicId", "Count"]
        if include_topic_terms:
            df["Terms"] = df["TopicId"].apply(lambda t: self.model.print_topic(t, self.strategy.number_terms))
        return df

    def get_term_topics(self):
        term_topics = [ 
            {    
                "term":t["term"],
                "prominantTopicId":t["topics"][0][0],
                "prmoinantTopicProbability":t["topics"][0][1],
                "prominantTopic":self.model.print_topic(t["topics"][0][0], self.strategy.number_terms),
                "topics":t["topics"]
            }            
            for t in
            [
                { 
                    "term": self._dictionary.get(k), 
                    "topics": self.model.get_term_topics(word_id = k, minimum_probability = self.strategy.minimum_term_topic_probability) 
                } 
                for k in self._dictionary.keys()
            ] if len(t['topics']) > 0
        ] 
        return pd.DataFrame(term_topics)

    def calculate_topic_coherence(self):
        coherence_model = CoherenceModel(
            model = self.model,
            #corpus = self.corpus,
            texts = self._texts,
            dictionary = self.dictionary,
            coherence = 'c_v')
        return coherence_model.get_coherence()

    def calculate_per_topic_coherence(self):
        coherence_model = CoherenceModel(
           model = self.model,
            #corpus = self.corpus,
            texts = self._texts,
            dictionary = self.dictionary,
            coherence = 'c_v')
        return coherence_model.get_coherence_per_topic()