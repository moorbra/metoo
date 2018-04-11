library(tidytext)

if (!exists("tasktokenize")){
    tasktokenize <- T
        task_tokenize <- function(tweets, stopwordsfilepath, stopwordspath, synonymfilepath) {
            tweet_tokens <- tokenize(tweets)
            tweet_tokens <- removestopwords(tweet_tokens, stopwordsfilepath)
            tweet_tokens <- replacesynonyms(tweet_tokens, synonymfilepath)
            return(tweet_tokens)
        }

        tokenize <- function(tweets) {
            return(tweets %>% unnest_tokens(word, tweet))
        }

        removestopwords <- function(tokens, stopwordsfilepath) {
            if(!file.exists(stopwordsfilepath)) {
                return(tokens)
            }

            custom_stop_words <- read_csv(stopwordsfilepath)
            data(stop_words)
            merged_stop_words <- bind_rows(custom_stop_words, stop_words)            
            nostopwords <- tokens %>%
                anti_join(merged_stop_words)

            return(nostopwords)
        }   

        replacesynonyms <- function(tweet_tokens, synonymfilepath) {
            if(!file.exists(synonymfilepath)) {
                return(tweet_tokens)
            }

            synonyms <- read_csv(synonymfilepath)
            tweet_tokens <- tweet_tokens %>%
                            left_join(synonyms) %>%
                            mutate(originalword = word) %>%
                            mutate(word = ifelse(is.na(replacement), word, replacement)) %>%
                            select(-replacement)
            
            return(tweet_tokens)
        }    
}