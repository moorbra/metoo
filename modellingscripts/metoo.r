library(lubridate)
library(ggplot2)
library(dplyr)
library(readr)
library(tidytext)
library(stringr)
library(tidyr)
source("util.r")

tweets <- loadtweets("../data/Metoo_Feb262018.csv")

# Tokenize the tweets.
tokenized_tweets <- tokenize(tweets)

# Remove stop words
tokenized_tweets <- removestopwords(tokenized_tweets)

# Count the frequent terms
countterms(tokenized_tweets)
termfrequencyplot <- plottermfrequency(tokenized_tweets, 200)
ggsave("../data/metoo_term_frequencies.png", plot = termfrequencyplot)

# Sentiment analysis
joywords <- get_sentiments("nrc") %>%
    filter(sentiment == "negative")

# Get the top 'joy' words
tokenized_tweets %>%
    inner_join(joywords) %>%
    count(word, sort = TRUE)

tweet_sentiment <- tokenized_tweets %>%
    inner_join(get_sentiments("bing")) %>%
    count(didx, date, sentiment) %>%
    spread(sentiment, n, fill = 0) %>%
    mutate(sentiment = positive - negative)

tweet_sentiment

ggplot(tweet_sentiment, aes(date, sentiment)) +
    geom_col(show.legend = TRUE) #+
    #facet_wrap(~didx, ncol = 2, scales = "free_x")