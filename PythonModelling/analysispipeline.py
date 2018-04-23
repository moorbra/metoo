import matplotlib
matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import logging
from TaskLoadData import TaskLoadData
from TaskTokenize import TaskTokenize
from TaskLdaModel import TaskLdaModel
from TaskLsiModel import TaskLsiModel
from TaskTermAnalysis import TaskTermAnalysis
from Strategies.LDAStrategy import LDAStrategy
from Strategies.TokenizationStrategy import TokenizationStrategy
from pprintpp import pprint as pp
import re
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

removeRegex = re.compile(r"[@]\w+[ ,.:]?|[?_#.]{2,}|&amp;|[\"]|http[s?]://\w+.\w+[/\w+]{0,}|^RT|^[ ]{1,}|[ ]{1,}$", re.IGNORECASE)
removeLineBreaks = re.compile(r"\n", re.IGNORECASE)
reduceSpaces = re.compile(r"[ ]{2,}", re.IGNORECASE)
removeInvalidCharacters = re.compile(r"[^\u0000-\u007F]", re.IGNORECASE)
removeleadingspace = re.compile(r"^[ ]{1,}")

def scrub_tweet(tweet):
    tweet = removeRegex.sub("", tweet)
    tweet = removeLineBreaks.sub(" ", tweet)
    tweet = reduceSpaces.sub(" ", tweet)
    tweet = removeInvalidCharacters.sub("", tweet)
    tweet = removeleadingspace.sub("", tweet)
    return tweet

data_file_path = "../data/dre/data"
analysis_file_path = "../data/dre/analysis"

# Load the data
load_data = TaskLoadData(scrub_function = scrub_tweet, data_path=data_file_path)
tweets_data_frame = load_data.load_data(text_column="tweet")
load_data.save_data_frame(tweets_data_frame, analysis_file_path, "tweets.csv")

# Tokenize the data
pp("Tokenizing")
tokenization_strategy = TokenizationStrategy()
tokenization_strategy.custom_stop_words_file = os.path.join("../data/dre/custom_stop_words.txt")
#tokenization_strategy.synonyms_file = os.path.join("../data/dre/synonyms.txt")
tokenizer = TaskTokenize(tokenization_strategy)
tokenized_tweets = tokenizer.tokenize_tweets(tweets_data_frame=tweets_data_frame, text_column="tweet")
tokenizer.save_data_frame(tokenized_tweets, analysis_file_path, "tokenized_tweets.csv")
pp("Finished Tokenizing")

# Analyze the tokens
pivoted_tokens = tokenizer.pivot_tokens(tokenized_tweets, analysis_file_path, "tweet_tokens.csv")
tokenizer.save_data_frame(pivoted_tokens, analysis_file_path, "pivoted_tokens.csv")
termanalyzer = TaskTermAnalysis()
term_frequencies = termanalyzer.compute_term_frequency(pivoted_tokens)
plot = termanalyzer.plot_term_frequency(term_frequencies, 600)
plot.get_figure().savefig(os.path.join(analysis_file_path, "termfrequency.png"))

# LDA Model
pp("LDA Model")
lda_strategy = LDAStrategy()
lda_strategy.number_passes = 500
lda_strategy.number_terms = 20
lda_strategy.number_topics = 20
lda_strategy.minimum_document_topic_probability = .90
lda_strategy.minimum_term_topic_probability = .05
lda_strategy.tokens_column = "tokens"
lda_strategy.text_column = "tweet"
ldamodel = TaskLdaModel(lda_strategy)
ldamodel.create_model(tokenized_tweets)
ldatopics = ldamodel.get_topics()
ldamodel.save_data_frame(ldatopics, analysis_file_path, "lda_topics.csv")
document_topics = ldamodel.get_document_topics()
ldamodel.save_data_frame(document_topics, analysis_file_path, "lda_document_topics.csv")
topic_count = ldamodel.count_document_topic_occurances(document_topics_data_frame=document_topics)
#pp(topic_count)
ldamodel.save_data_frame(topic_count, analysis_file_path, "lda_topicdocument_count.csv")
term_topics = ldamodel.get_term_topics()
ldamodel.save_data_frame(term_topics, analysis_file_path, "lda_term_topics.csv")

# LSI Model
# lsimodel = TaskLsiModel(number_topics=20, number_terms=5)
# lsimodel.create_model(tokenized_tweets["tokens"]) 
# lsitopics = lsimodel.get_topics()
# lsimodel.save_data_frame(lsitopics, analysis_file_path, "lsi_topics.csv")
# topics_plot = lsimodel.plot_topics(lsitopics)