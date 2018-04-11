import logging
from TaskLoadData import TaskLoadData
from TaskTokenize import TaskTokenize
from TaskLdaModel import TaskLdaModel
from TaskLsiModel import TaskLsiModel
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

load_data = TaskLoadData(scrub_function = scrub_tweet, data_path=data_file_path)
tweets_data_frame = load_data.load_data(text_column="tweet")
tweets_data_frame.to_csv(os.path.join(analysis_file_path,"tweets.csv"))

custom_stop_words = set(['-', ':', '.', '?', ' ', '*', ',', '%', '#', '|', '!', 'ht', 'htt', 'https', 'https://', '>', '<', '(', ')'])
tokenizer = TaskTokenize(custom_stop_words=custom_stop_words)
tokenized_tweets = tokenizer.tokenize_tweets(tweets_data_frame, text_column="tweet")
tokenized_tweets.to_csv(os.path.join(analysis_file_path, "tokenized_tweets.csv"))
#pp(tokenized_tweets)
tokenizer.save_tokens(tokenized_tweets, analysis_file_path, "tweet_tokens.csv")



# ldamodel = TaskLdaModel(number_topics = 20, number_passes = 50, number_terms=5)
# ldamodel.create_model(tokenized_tweets)
# ldatopics = ldamodel.get_topics()
# ldatopics.to_csv(os.path.join(analysis_file_path, "lda_topics.csv"))

# lsimodel = TaskLsiModel(number_topics=20, number_terms=5)
# lsimodel.create_model(tokenized_tweets)
# lsitopics = lsimodel.get_topics()
# lsitopics.to_csv(os.path.join(analysis_file_path, "lsi_topics.csv"))