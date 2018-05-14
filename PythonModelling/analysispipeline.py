import matplotlib
matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import logging
from TaskLoadData import TaskLoadData
from TaskTokenize import TaskTokenize
from TaskLdaModel import TaskLdaModel
from TaskLsiModel import TaskLsiModel
from TaskTermAnalysis import TaskTermAnalysis
from TaskSentimentAnalysis import TaskSentimentAnalysis
from Strategies.LDAStrategy import LDAStrategy
from Strategies.TokenizationStrategy import TokenizationStrategy
from Strategies.SentimentAnalysisStrategy import SentimentAnalysisStrategy
from pprintpp import pprint as pp
import re
import os

root_path = "../data/altonsterling"
data_file_path = f"{root_path}/data"
analysis_file_path = f"{root_path}/analysis"

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', 
    level=logging.INFO)

logger = logging.getLogger()

fileHandler = logging.FileHandler(filename=f"{analysis_file_path}/tweet_analysis.log", mode='w')
fileHandler.terminator = "\r\n"
fileHandler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
logger.addHandler(fileHandler)    

removeRegex = re.compile(r"[@]\w+[ ,.:]?|[?_#.]{2,}|&amp;|[\"]|http[s?]://\w+.\w+[/\w+]{0,}|^RT|^[ ]{1,}|[ ]{1,}$|_{2,}", re.IGNORECASE)
removeLineBreaks = re.compile(r"\n|\r\n|\r", re.IGNORECASE)
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

# Load the data
load_data = TaskLoadData(scrub_function = scrub_tweet, data_path=data_file_path)
tweets_data_frame = load_data.load_data(text_column="tweet")
load_data.save_data_frame(tweets_data_frame, analysis_file_path, "tweets.csv")

# Perform sentiment analysis
sentiment_analysis_strategy = SentimentAnalysisStrategy()
sentiment_analysis = TaskSentimentAnalysis(sentiment_analysis_strategy)
sentiment = sentiment_analysis.compute_sentiment(tweets_data_frame)
aggregate_sentiment = sentiment_analysis.compute_aggregrate_sentiment(tweets_data_frame)
sentiment_analysis.save_data_frame(aggregate_sentiment, analysis_file_path, "tweet_sentiment.csv")

# Tokenize the data
tokenization_strategy = TokenizationStrategy()
tokenization_strategy.minimum_term_frequency = 2
tokenization_strategy.custom_stop_words_file = os.path.join(f"{root_path}/custom_stop_words.txt")
tokenization_strategy.synonyms_file = os.path.join(f"{root_path}/synonyms.txt")
tokenizer = TaskTokenize(tokenization_strategy)
tokenized_tweets = tokenizer.tokenize_tweets(tweets_data_frame=tweets_data_frame, text_column="tweet")
tokenizer.save_data_frame(tokenized_tweets, analysis_file_path, "tokenized_tweets.csv")
tokenizer.save_data_frame(tokenizer.token_frequencies,analysis_file_path, "token_frequencies.csv")
tokenizer.save_data_frame(tokenizer.infrequent_tokens, analysis_file_path, "infrequent_tokens.csv")
tokenizer.save_data_frame(tokenizer.documents_without_tokens, analysis_file_path, "documents_without_tokens.csv")

# LDA Model
lda_strategy = LDAStrategy()
lda_strategy.number_passes = 2
lda_strategy.number_terms = 15
lda_strategy.number_topics = 100
lda_strategy.minimum_document_topic_probability = .65
lda_strategy.minimum_term_topic_probability = .05
lda_strategy.eval_model_every = None
lda_strategy.update_model_every = 1
lda_strategy.chunksize = 500
lda_strategy.training_iterations = 50000
lda_strategy.tokens_column = "tokens"
lda_strategy.text_column = "tweet"
ldamodel = TaskLdaModel(lda_strategy)
ldamodel.create_model(tokenized_tweets)
ldatopics = ldamodel.get_topics()
ldamodel.save_data_frame(ldatopics, analysis_file_path, "lda_topics.csv")
document_topics = ldamodel.get_document_topics()
ldamodel.save_data_frame(document_topics, analysis_file_path, "lda_document_topics.csv")
topic_count = ldamodel.count_document_topic_occurances(document_topics_data_frame=document_topics)
ldamodel.save_data_frame(topic_count, analysis_file_path, "lda_topicdocument_count.csv")
ldamodel.calculate_topic_coherence()