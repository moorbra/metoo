library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(lubridate)

if (!exists("loaddatatask")){
    loaddatatask <- T

        task_loaddata <- function(datafilepath, filepattern, scrub = scrubtweet_default) {
            scrubtweet <<- scrub
            return(loadTweets(datafilepath, filepattern))
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