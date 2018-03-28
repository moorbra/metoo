library(twitteR)
library(dplyr)
library(lubridate)

# Change the next four lines based on your own consumer_key, consume_secret, access_token, and access_secret. 
consumer_key <- "NzA2a09uXVo3YqIXqHP4AgX9s"
consumer_secret <- "ibtaRGJ2dQNT6aWQOKQ53aYPO7t62Xa2cYMFDPLkRvVDeAMa9p"
access_token <- "171349116-MXV8Ap3H2tJsjqRNJrMmDudVAehd3LfJfXIabN9K"
access_secret <- "hssmpWn7tsSLh52C34JnpkHT6q65bgcnUf3UtJNbbJ0K4"

setup_twitter_oauth(consumer_key, consumer_secret, access_token, access_secret)


tweets <- searchTwitter(
    "#marchforourlives", 
    n=100000, 
    lang="en", 
    since="2018-02-13", 
    retryOnRateLimit=30,
    resultType="mixed")

# Transform tweets list into a data frame
tweets.df <- twListToDF(tweets)

#print(tweets.df)
tweets.df <- tweets.df %>%
             mutate(id = row_number()) %>%
             mutate(tweet = text) %>%
             mutate(date = created) %>%
             select(id, tweet, date, screenName, retweetCount, isRetweet, retweeted, favoriteCount)
write.csv(tweets.df, "marchforourlives.csv", row.names = FALSE)
