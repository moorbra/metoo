library(topicmodels)
library(tm)

if (!exists("taskldatopicmodelling")){
    taskldatopicmodelling <- T

    task_extracttopics <- function(tokens, k,  save = saveoutput_default) {
        wordcount <- counttweetwords(tokens)
        save(wordcount, "word_count.csv")
        dtm <- documenttermmatrix(wordcount)
        lda <- LDA(dtm, k = k, control = list(seed = 1234))
        topics <- tidy(lda, matrix = "beta")
        save(topics, "topics.csv")        

        return(topics)
    }

    task_visualizetopics <- function(topics, top_n_terms) {
        top_terms <- topic_top_terms(topics, top_n_terms)
        plot <- plot_top_terms(top_terms)
        return(plot)
    }

    plot_top_terms <- function(top_terms) {
        plot <- top_terms %>%
                mutate(term = reorder(term, beta)) %>%
                ggplot(aes(term, beta, fill = factor(topic))) +
                geom_col(show.legend = FALSE) +
                facet_wrap(~ topic, scales = "free", ncol = 2) +
                coord_flip()        
    }

    topic_top_terms <- function(topics, top_n_terms) {
        tweets_top_terms <- topics %>%
                            group_by(topic) %>%
                            top_n(top_n_terms, beta) %>%
                            ungroup() %>%
                            arrange(topic, -beta)
        return(tweets_top_terms)
    }


    saveoutput_default <- function(outputpath, wordcount, topics) {
    }

    counttweetwords <- function(tokens) {
        tweet_words <- tokens %>%
                       count(id, word, sort = TRUE) %>%
                       ungroup()
        return(tweet_words)
    }

    documenttermmatrix <- function(wordcount) {
        return(wordcount %>% 
               cast_dtm(id, word, n))
    }
}