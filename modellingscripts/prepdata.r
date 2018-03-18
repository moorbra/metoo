library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)

loadtweets <- function(datafile) {
    tweets <- read_csv(datafile)
    tweets <- tweets %>%
            mutate(origtweet = tweet) %>%
            mutate(tweet = scrubtweet(tweet)) %>%
            mutate(date = mdy_hm(date))

    return(tweets)
}

scrubtweet <- function(tweet) {
    patterns <- c("([@]\\w+)[ ,.]?|\\n|[?_#.]{2,}|&amp;|[\"]|http[s?]://\\w+.\\w+[/\\w+]?")    
    tweet <- str_replace_all(tweet, patterns, "")               
    return (tweet)
}

febtweets <- loadtweets("../data/Metoo_Feb262018.csv")
mar06tweets <- loadtweets("../data/MeToo_March062018.csv")
mar08tweets <- loadtweets("../data/MeToo_March082018.csv")
mar10tweets <- loadtweets("../data/Metoo0310_2017.csv")
tweets = bind_rows(febtweets, mar06tweets, mar08tweets, mar10tweets)

tweets

write.csv(tweets, file="../data/Metoo_scrubbed.csv")