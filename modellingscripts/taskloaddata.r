library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)
library(ggplot2)
library(ggforce)

if (!exists("loaddatatask")){
    loaddatatask <- T

        task_loaddata <- function(datafilepath, filepattern, scrub = scrubtweet_default, distincttweets = FALSE) {
            scrubtweet <<- scrub
            tweets = loadTweets(datafilepath, filepattern)
            if(distincttweets) {
                return(distinct(tweets, tweet, .keep_all=TRUE))
            }                         
            return(tweets)
        }

        task_tweet_post_histogram <- function(tweets, rows = 1, columns = 1, save) {
            tweet_post_count <- tweets %>%
                                count(group = paste(month(date), day(date), year(date), sep="/"), hour = hour(date))

            groups <- tweet_post_count %>% group_by(group) %>% summarize(count=n())
            number_pages <- ceiling(nrow(groups) / (rows * columns))
            
            for(page in 1:number_pages) {
                print(paste("Generating histogtram plot", page, "of", number_pages, sep=" "))
                plot <- plot_tweet_histogram(tweet_post_count, page, rows, columns)
                save(plot, paste("posthistogram_", page, ".png", sep = ""))
            }
        }

        plot_tweet_histogram <- function(tweet_post_count, page = 1, rows = 1, columns = 1) {
            visualization <- ggplot(tweet_post_count, aes(hour, n, fill = group)) +
                             geom_col(show.legend = FALSE) +
                             labs(x = "Hour", y = "Tweets") +
                             facet_wrap_paginate(~ group, page = page, nrow = rows, ncol = columns, scales = "free_x")     

            return(visualization)                       
        }

        loadtweetfile <- function(datafile) {
            tweets <- read_csv(datafile)
            tweets <- tweets %>%
                    mutate(date = format(date, tz="America/Chicago")) %>%
                    mutate(origtweet = tweet) %>%
                    mutate(tweet = scrubtweet(iconv(tweet, "ASCII", "UTF-8", sub="")))

            return(tweets)
        }

        scrubtweet_default <- function(tweet) {
            return (tweet)
        }


        loadTweets <- function(datafilepath, filepattern) {
            files <- list.files(path=datafilepath, pattern=filepattern)
            data <- lapply(files, function(file) {
                loadtweetfile(file.path(datafilepath, file))
            })
            return(bind_rows(data))
        }
}