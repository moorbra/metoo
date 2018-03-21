library(tidytext)

if (!exists("tasktokenize")){
    tasktokenize <- T
        task_tokenize <- function(tweets, stopwordsfilepath) {
            tweet_tokens <- tokenize(tweets)
            tweet_tokens <- removestopwords(tweet_tokens, stopwordsfilepath)
            return(tweet_tokens)
        }

        tokenize <- function(tweets) {
            return(tweets %>% unnest_tokens(word, tweet))
        }

        removestopwords <- function(tokens, stopwordsfilepath) {
            custom_stop_words <- read_csv(stopwordsfilepath)
            data(stop_words)

            merged_stop_words <- bind_rows(custom_stop_words, stop_words)
            
            nostopwords <- tokens %>%
                anti_join(merged_stop_words)

            return(nostopwords)
        }       
}