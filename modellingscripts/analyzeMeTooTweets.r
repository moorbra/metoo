source("taskloaddata.r")
source("tasktokenize.r")
source("tasktermanalysis.r")
source("taskldatopicmodelling.r")

analysis_pipeline <- function(outputpath) {
    metoo_tweets <- task_loaddata()
    metoo_tweets_tokens <- task_tokenize(metoo_tweets)
    metoo_tweet_term_frequency <- task_computetermfrequency(metoo_tweets_tokens)
    metoo_term_frequency_plot <- task_plottermfrequency(metoo_tweet_term_frequency, 500)        
    metoo_ldatopicmodel <- task_extracttopics(metoo_tweets_tokens, outputpath)
    metoo_topics_visualization <- task_visualizetopics(metoo_ldatopicmodel, 10)    
    
    save_analysis_visualizations(
        outputpath, 
        metoo_term_frequency_plot,
        metoo_topics_visualization)

    save_analysis_data(
        outputpath,
        metoo_tweets, 
        metoo_tweets_tokens,
        metoo_tweet_term_frequency,
        metoo_tweetwords_count)
}

save_analysis_data <- function(outputpath, tweets, tokens, termfrequency, tweetwordcount) {    
    write.csv(tweets, file.path(outputpath, "scrubbed_tweets.csv"))
    write.csv(tokens, file.path(outputpath, "tweet_tokens.csv"))
    write.csv(termfrequency, file.path(outputpath, "tweet_term_frequency.csv"))
}

save_analysis_visualizations <- function(outputpath, termfrequency, topics) {
    ggsave(file.path(outputpath, "term_frequency_plot.png"), plot = termfrequency)
    ggsave(file.path(outputpath, "topics.png"), plot = topics)
}

analysis_pipeline("../data/MeToo/analysis/")