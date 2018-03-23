library(tidyr)
library(tidytext)
library(ggplot2)
library(lubridate)

if (!exists("sentimentanalysistext")){
    sentimentanalysistext <- T

    task_sentimentanalysis <- function(tokens) {
        tweet_sentiment <- tokens %>%
            inner_join(get_sentiments("bing")) %>%
            count(group = day(date), index = hour(date), sentiment) %>%
            spread(sentiment, n, fill = 0) %>%
            mutate(sentiment = positive - negative)

        return(tweet_sentiment)
    }

    task_visualizesentiment <- function(tweet_sentiment) {
        visualization <- ggplot(tweet_sentiment, aes(index, sentiment, fill = group)) +
            geom_col(show.legend = FALSE) #+
            #facet_wrap(~ group, ncol = 2, scales = "free_x")
        
        return(visualization)
    }
}