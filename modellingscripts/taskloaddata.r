library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)

if (!exists("loaddatatask")){
    loaddatatask <- T

        task_loaddata <- function() {
            return(loadTweets())
        }

        loadtweetfile <- function(datafile) {
            tweets <- read_csv(datafile)
            tweets <- tweets %>%
                    mutate(origtweet = tweet) %>%
                    mutate(tweet = scrubtweet(tweet)) %>%
                    mutate(date = mdy_hm(date))

            return(tweets)
        }

        scrubtweet <- function(tweet) {
            patterns <- c("[@]\\w+[ ,.:]?|\\n|[?_#.]{2,}|&amp;|[\"]|http[s?]://\\w+.\\w+[/\\w+]{0,}|^RT|[#2]{0,1}[Mm][Ee][Tt][Oo]{2}[_]{0,1}")
            tweet <- str_replace_all(tweet, patterns, "")
            tweet <- str_replace_all(tweet, "[ ]{2,}"," ")
            tweet <- str_replace_all(tweet, "^[ ]{1,}|[ ]{1,}$","")
            return (tweet)
        }


        loadTweets <- function() {
            febtweets <- loadtweetfile("../data/MeToo/data/Metoo_Feb262018.csv")
            mar06tweets <- loadtweetfile("../data/MeToo/data/MeToo_March062018.csv")
            mar08tweets <- loadtweetfile("../data/MeToo/data/MeToo_March082018.csv")
            mar10tweets <- loadtweetfile("../data/MeToo/data/Metoo0310_2017.csv")
            tweets = bind_rows(febtweets, mar06tweets, mar08tweets, mar10tweets)
            return(tweets)
        }
}