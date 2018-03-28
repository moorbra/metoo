library(tidyr)
library(tidytext)
library(ggplot2)
library(lubridate)

if (!exists("sentimentanalysistext")){
    sentimentanalysistext <- T

    task_sentimentanalysis <- function(tokens) {
        tweet_sentiment <- tokens %>%
            inner_join(get_sentiments("bing")) %>%
            count(group = paste(paste(month(date), day(date), year(date), sep="/"), hour(date), sep =  " H:"), index = minute(date), sentiment) %>%
            spread(sentiment, n, fill = 0) %>%
            mutate(avgsentiment = round(positive / (positive + negative) - negative / (positive + negative), 2)) %>%
            mutate(sentiment = positive - negative)

        return(tweet_sentiment)
    }

    task_visualizesentiment <- function(tweet_sentiment, rows = 1, columns = 1, save) {
        number_pages <- ceiling(length(tweet_sentiment) / (rows * columns))
        for(page in 1:number_pages) {
            plot <- plot_sentiment(tweet_sentiment, page, rows, columns)
            save(plot, paste("sentimentvisualization_", page, ".png", sep = ""))
        }
    }

    plot_sentiment <- function(tweet_sentiment, page = 1, rows = 1, columns = 1) {
        visualization <- ggplot(tweet_sentiment, aes(index, sentiment, fill = group)) +
            geom_col(show.legend = FALSE) +
            labs(x = "minute") +
            facet_wrap_paginate(~group, scales = "free_x", ncol = columns, nrow = rows, page = page)
        
        return(visualization)        
    }
}