library(tidytext)

if (!exists("tasktokenize")){
    tasktokenize <- T
        task_tokenize <- function(tweets) {
            tweet_tokens <- tokenize(tweets)
            tweet_tokens <- removestopwords(tweet_tokens)
            return(tweet_tokens)
        }

        tokenize <- function(tweets) {
            return(tweets %>% unnest_tokens(word, tweet))
        }

        removestopwords <- function(tokens) {
            custom_stop_words <- read_csv("../data/MeToo/data/custom_stop_words.txt")
            data(stop_words)

            merged_stop_words <- bind_rows(custom_stop_words, stop_words)
            
            nostopwords <- tokens %>%
                anti_join(merged_stop_words)

            return(nostopwords)
        }       
}