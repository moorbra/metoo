library(lubridate)
library(ggplot2)
library(dplyr)
library(readr)
library(tidytext)
library(stringr)
library(tidyr)
library(tm)
library(topicmodels)
source("util.r")

tweets <- loadtweets("../data/Metoo_Feb262018.csv")

# Tokenize the tweets.
tokenized_tweets <- tokenize(tweets)

# Remove stop words
tokenized_tweets <- removestopwords(tokenized_tweets)

tweet_words <- tokenized_tweets %>%
               count(tweet, word, sort = TRUE) %>%
               ungroup()

tweet_words
tweet_sparse_matrix <- tweet_words %>%
                       cast_dtm(tweet, word, n)
tweet_sparse_matrix

tweets_lda <- LDA(tweet_sparse_matrix, k = 10, control = list(seed = 1234))

tweets_topics <- tidy(tweets_lda, matrix = "beta")
tweets_topics

tweets_top_terms <- tweets_topics %>%
    group_by(topic) %>%
    top_n(10, beta) %>%
    ungroup() %>%
    arrange(topic, -beta)

tweets_top_terms %>%
    mutate(term = reorder(term, beta)) %>%
    ggplot(aes(term, beta, fill = factor(topic))) +
    geom_col(show.legend = FALSE) +
    facet_wrap(~ topic, scales = "free", ncol = 2) +
    coord_flip()

# total_words <- tweet_words %>%
#                #group_by(tweet) %>%
#                summarize(total = sum(n))

# tweet_words <- tweet_words %>%
#                mutate(total = total_words)

# tweet_words <- left_join(tweet_words, total_words)

# tweet_words <- tweet_words %>%
#                bind_tf_idf(word, tweet, n)

# tweet_words %>%
#     select(-total) %>%
#     filter(n >= 5)
#     #arrange(desc(tf_idf))




# freq_by_rank <- tweet_words %>%
#                 group_by(tweet) %>%
#                 mutate(rank = row_number(),
#                         `term frequency` = n / total)

#freq_by_rank %>% filter(tweet == 2201)

# freq_by_rank %>%
#     filter(tweet >= 1 & tweet <= 500) %>%
#     ggplot(aes(rank, `term frequency`, color = tweet)) +
#     geom_line(size = 1.1, alpha = 0.8, show.legend = FALSE) +
#     scale_x_log10() +
#     scale_y_log10()

# Count the frequent terms
#countterms(tokenized_tweets)
#termfrequencyplot <- plottermfrequency(tokenized_tweets, 200)
#ggsave("../data/metoo_term_frequencies.png", plot = termfrequencyplot)

# Sentiment analysis
#joywords <- get_sentiments("nrc") %>%
#    filter(sentiment == "negative")

# Get the top 'joy' words
#tokenized_tweets %>%
#    inner_join(joywords) %>%
#    count(word, sort = TRUE)

# tweet_sentiment <- tokenized_tweets %>%
#     inner_join(get_sentiments("bing")) %>%
#     count(didx, date, sentiment) %>%
#     spread(sentiment, n, fill = 0) %>%
#     mutate(sentiment = positive - negative)

# tweet_sentiment

# ggplot(tweet_sentiment, aes(date, sentiment)) +
#     geom_col(show.legend = TRUE) #+
    #facet_wrap(~didx, ncol = 2, scales = "free_x")