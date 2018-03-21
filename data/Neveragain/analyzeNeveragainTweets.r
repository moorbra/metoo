source("../../modellingscripts/taskloaddata.r")
source("../../modellingscripts/tasktokenize.r")
source("../../modellingscripts/tasktermanalysis.r")
source("../../modellingscripts/taskldatopicmodelling.r")

analysis_pipeline <- function() {
    datapath <- "data"
    outputpath <<- "analysis"
    
    # Load the tweets
    metoo_tweets <- task_loaddata(datapath, ".csv", scrubtweet)
    save_output(metoo_tweets, "tweets.csv")
    
    # Tokenize
    metoo_tweets_tokens <- task_tokenize(metoo_tweets, file.path("custom_stop_words.txt"))
    save_output(metoo_tweets_tokens, "tokens.csv")
    
    # Compute term frequency
    metoo_tweet_term_frequency <- task_computetermfrequency(metoo_tweets_tokens)
    save_output(metoo_tweet_term_frequency, "term_frequency.csv")
    metoo_term_frequency_plot <- task_plottermfrequency(metoo_tweet_term_frequency, 1500)        
    save_visualization(metoo_term_frequency_plot, "term_frequency.png")
    
    # Create a topic model
    metoo_ldatopicmodel <- task_extracttopics(metoo_tweets_tokens, 6, save_output)
    metoo_topics_visualization <- task_visualizetopics(metoo_ldatopicmodel, 20)    
    save_visualization(metoo_topics_visualization, "topic_model.png")
}

save_output <- function(data, filename) {
    write.csv(data, file.path(outputpath, paste("neveragain_tweet_", filename)))
}

save_visualization <- function(plot, name) {
    ggsave(file.path(outputpath, paste("neveragain_tweet_", name)), plot = plot)
}

scrubtweet <- function(tweet) {
    patterns <- c("[@]\\w+[ ,.:]?|\\n|[?_#.]{2,}|&amp;|[\"]|http[s?]://\\w+.\\w+[/\\w+]{0,}|^RT")
    tweet <- str_replace_all(tweet, patterns, "")
    tweet <- str_replace_all(tweet, "[ ]{2,}"," ")
    tweet <- str_replace_all(tweet, "^[ ]{1,}|[ ]{1,}$","")
    return (tweet)
}

analysis_pipeline()