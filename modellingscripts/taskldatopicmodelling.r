library(topicmodels)
library(tm)

if (!exists("taskldatopicmodelling")){
    taskldatopicmodelling <- T

    task_extracttopics <- function(tokens, outputpath) {
        wordcount <- counttweetwords(tokens)
        dtm <- documenttermmatrix(wordcount)
        lda <- LDA(dtm, k = 10, control = list(seed = 1234))
        topics <- tidy(lda, matrix = "beta")

        saveoutput(outputpath,
            wordcount,
            topics)

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


    saveoutput <- function(outputpath, wordcount, topics) {
        write.csv(wordcount, file.path(outputpath, "tweet_word_count.csv"))
        write.csv(topics, file.path(outputpath, "tweet_topics.csv"))
        # write.csv(documenttermmatrix, file.path(outputpath, "tweet_document_term_matrix.csv"))
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