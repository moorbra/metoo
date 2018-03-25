if (!exists("analysispipeline")){
    analysispipeline <- T
    
    analysis_pipeline <- function(datapath, outputpath, outputprefix, 
        scrubtweet = scrubscrubtweet_default,
        numbertopics = 5, termspertopic = 10, topiccolumns = 1, topicrows = 1,
        minimumtermcount = 500) {
        
        datapath <- datapath
        outputpath <<- outputpath
        outputprefix <<- outputprefix
        
        # Load the tweets
        tweets <- task_loaddata(datapath, ".csv", scrubtweet)
        save_output(tweets, "tweets.csv")
        tweet_post_histogram <- task_tweet_post_histogram(tweets)
        #save_output(tweet_post_histogram, "histogram.csv")
        save_visualization(tweet_post_histogram, "post_histogram.png")
        
        # Tokenize
        tweets_tokens <- task_tokenize(tweets, file.path("custom_stop_words.txt"))
        save_output(tweets_tokens, "tokens.csv")
        
        # Perform sentiment analysis
        sentiment <- task_sentimentanalysis(tweets_tokens)
        save_output(sentiment, "sentiment.csv")
        sentiment_visualization <- task_visualizesentiment(sentiment)
        save_visualization(sentiment_visualization, "sentiment.png")

        # Compute term frequency
        term_frequency <- task_computetermfrequency(tweets_tokens)
        save_output(term_frequency, "term_frequency.csv")
        term_frequency_plot <- task_plottermfrequency(term_frequency, minimumtermcount)
        save_visualization(term_frequency_plot, "term_frequency.png")
        
        # Create a topic model
        ldatopicmodel <- task_extracttopics(tweets_tokens, numbertopics, save_output)
        topics_visualization <- task_visualizetopics(ldatopicmodel, top_n_terms = termspertopic, rows = 1, columns = 2, save = save_visualization)
    }

    save_output <- function(data, filename) {
        write.csv(data, file.path(outputpath, paste(outputprefix, "_tweet_", filename, sep = "")))
    }

    save_visualization <- function(plot, name) {
        ggsave(file.path(outputpath, paste(outputprefix, "_tweet_", name, sep = "")), plot = plot)
    }

    scrubtweet_default <- function(tweet) {
        return (tweet)
    }
}