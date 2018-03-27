library(topicmodels)
library(tm)
library(ggforce)

if (!exists("taskldatopicmodelling")){
    taskldatopicmodelling <- T

    task_extracttopics <- function(tokens, k,  save = saveoutput_default) { 
        number_topcs <<- k
        wordcount <- counttweetwords(tokens)
        save(wordcount, "word_count.csv")
        dtm <- documenttermmatrix(wordcount)
        lda <- LDA(dtm, k = number_topcs, control = list(seed = 1234))
        topics <- tidy(lda, matrix = "beta")
        save(topics, "topics.csv")
        return(topics)
    }

    task_visualizetopics <- function(topics, top_n_terms, rows = 1, columns = 1, save) {
        top_terms <- topic_top_terms(topics, top_n_terms)
        plots <- plot_top_terms(top_terms, rows = rows, columns = columns, save = save)
        return(plots)
    }

    plot_top_terms <- function(top_terms, page = 1, rows = 1, columns = 1, save) {
        number_pages <- ceiling(number_topcs / (rows * columns))
        for(page in 1:number_pages) {
            plot <- plot_top_terms_page(top_terms, page, rows, columns)
            save(plot, paste("topicsvisualization_", page, ".png", sep = ""))
        }
    }

    plot_top_terms_page <- function(top_terms, page = 1, rows = 1, columns = 1) {
        plot <- top_terms %>%
                mutate(term = reorder(term, beta)) %>%                
                ggplot(aes(term, beta, fill = factor(topic))) +
                geom_col(show.legend = FALSE) +
                facet_wrap_paginate(~topic, scales = "free", ncol = columns, nrow = rows, page = page) +
                coord_flip()        
        return(plot)   
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