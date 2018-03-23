library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)
library(ggplot2)

if (!exists("loaddatatask")){
    loaddatatask <- T

        task_loaddata <- function(datafilepath, filepattern, scrub = scrubtweet_default) {
            scrubtweet <<- scrub
            return(loadTweets(datafilepath, filepattern))
        }

        task_tweet_post_histogram <- function(tweets) {
            tweet_post_count <- tweets %>%
                                count(group = paste(month.abb[month(date)], "-", year(date), sep = ""), day = day(date), hour = hour(date))

            visualization <- ggplot(tweet_post_count, aes(hour, n, fill = day)) +
                             geom_col(show.legend = TRUE) +
                             facet_wrap(~ group, ncol = 1, scales = "free_x")     

            return(visualization)                       
        }

        loadtweetfile <- function(datafile) {
            tweets <- read_csv(datafile)
            tweets <- tweets %>%
                    mutate(origtweet = tweet) %>%
                    mutate(tweet = scrubtweet(tweet)) %>%
                    mutate(date = mdy_hm(date))

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