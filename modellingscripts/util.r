if (!exists("util_R")){
 util_R <- T

    loadtweets <- function(datafile) {
        tweets <- read_csv(datafile)
        tweets <- tweets %>%
                mutate(date = mdy_hm(date)) %>%
                mutate(didx = hour(date))

        return(tweets)
    }

    tokenize <- function(tweets) {
        return(tweets %>% unnest_tokens(word, text))
    }

    removestopwords <- function(tokens) {
        custom_stop_words <- read_csv("custom_stop_words.txt")
        data(stop_words)

        merged_stop_words <- bind_rows(custom_stop_words, stop_words)

        nostopwords <- tokens %>%
            anti_join(merged_stop_words)

        return(nostopwords)
    }

    countterms <- function(tokens) {
        return(tokens %>% count(word, sort = TRUE))
    }

    plottermfrequency <- function(tokens, top) {
        countterms(tokens) %>%
        filter(n > top) %>%
        mutate(word = reorder(word, n)) %>%
        ggplot(aes(word, n)) +
        geom_col() +
        xlab(NULL) +
        coord_flip()
    }
}