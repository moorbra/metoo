library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)
library(ggplot2)
library(ggforce)

if (!exists("loaddatatask")){
    loaddatatask <- T

        task_loaddata <- function(datafilepath, filepattern, scrub = scrubtweet_default) {
            scrubtweet <<- scrub
            return(loadTweets(datafilepath, filepattern))
        }

        task_tweet_post_histogram <- function(tweets, save) {
            tweet_post_count <- tweets %>%
                                count(group = paste(month(date), day(date), year(date), sep="/"), hour = hour(date))

            groups <- tweet_post_count %>% group_by(group) %>% summarize(count=n())
            number_pages <- nrow(groups)
            
            print("Generating histogram plots ....")
            for(page in 1:number_pages) {
                print(paste("Plot", page, "of", number_pages, sep=" "))
                plot <- plot_tweet_histogram(tweet_post_count, page)
                save(plot, paste("posthistogram_", page, ".png", sep = ""))
            }
            print("Done")            
        }

        plot_tweet_histogram <- function(tweet_post_count, page = 1) {
            visualization <- ggplot(tweet_post_count, aes(hour, n, fill = group)) +
                             geom_col(show.legend = FALSE) +
                             facet_wrap_paginate(~ group, page = page, nrow = 1, ncol = 1, scales = "free_x")     

            return(visualization)                       
        }

        loadtweetfile <- function(datafile) {
            tweets <- read_csv(datafile)
            tweets <- tweets %>%
                    mutate(origtweet = tweet) %>%
                    mutate(tweet = scrubtweet(tweet)) #%>%
                    #mutate(date = mdy_hm(date))

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