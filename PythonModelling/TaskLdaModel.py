from Task import Task
from TopicModel import TopicModel
from gensim.models import LdaModel
from gensim.models import CoherenceModel
from gensim.models.phrases import Phrases, Phraser
from Strategies import LDAStrategy
import pandas as pd

class TaskLdaModel(TopicModel, Task):

    def __init__(self, lda_strategy):
        TopicModel.__init__(self, lda_strategy)
        Task.__init__(self)
        self._texts = None

    def create_model(self, documents_data_frame):
        self.logger.info("Creating LDA topic model.")
        self._texts = documents_data_frame[self.strategy.tokens_column].tolist()
        self.logger.info(f"Adding {len(self._texts)} documents to corpus.")
        self._texts = self.__add_bigrams(self._texts)
        self.logger.info("Creating dictionary from texts.")
        self.dictionary = self.create_dictionary(self._texts)
        self.logger.info("Creating corpus from texts and dictionary.")
        self.corpus = self.create_corpus(self._texts, self.dictionary)
        self.logger.info("Creating topic model.")
        self.__log_strategy()
        self.model = LdaModel(self.corpus, 
            id2word = self.dictionary, 
            num_topics = self.strategy.number_topics, 
            passes = self.strategy.number_passes, 
            random_state = self.strategy.random_state_seed, 
            eval_every = self.strategy.eval_model_every,
            chunksize = self.strategy.chunksize,
            update_every = self.strategy.update_model_every,
            iterations = self.strategy.training_iterations,
            alpha=self.strategy.alpha,
            eta=self.strategy.eta)

    def __log_strategy(self):
        self.logger.info("Model strategy.")
        self.logger.info(f"Number passes {self.strategy.number_passes}.")
        self.logger.info(f"Chunk size {self.strategy.chunksize}.")
        self.logger.info(f"Training iterations {self.strategy.training_iterations}.")
        self.logger.info(f"Number topics {self.strategy.number_topics}.")

    def __add_bigrams(self, tokenized_documents):
        self.logger.info("Adding bigrams.")
        phrases = Phrases(tokenized_documents, min_count=self.strategy.phrases_min_count)
        bigram = Phraser(phrases)
        for idx in range(len(tokenized_documents)):
            for token in bigram[tokenized_documents[idx]]:
                if '_' in token:
                    # Token is a bigram, add to document.
                    tokenized_documents[idx].append(token)
        return tokenized_documents 


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
            texts = self._texts,
            dictionary = self.dictionary,
            coherence = 'c_v')
        topic_coherence = coherence_model.get_coherence()
        self.logger.info(f"Aggregate topic coherence: {topic_coherence}")
        per_topic_coherence = coherence_model.get_coherence_per_topic()
        [self.logger.info(f"Topic {i} coherence {tc}.") for i ,tc in enumerate(per_topic_coherence)]
        return { "topic_coherence": topic_coherence, "per_topic_coherence": per_topic_coherence}