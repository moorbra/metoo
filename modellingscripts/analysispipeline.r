if (!exists("analysispipeline")){
    analysispipeline <- T
    
    analysis_pipeline <- function(datapath, outputpath, outputprefix, 
        scrubtweet = scrubscrubtweet_default, 
        customstopwordspath = "", synonymfilepath = "",
        numbertopics = 5, termspertopic = 10, topiccolumns = 1, topicrows = 1,
        minimumtermcount = 500,
        includesentiment = TRUE, includetopicmodel = TRUE, 
        includetermfrequency = TRUE) {
        
        datapath <- datapath
        outputpath <<- outputpath
        outputprefix <<- outputprefix
        
        # Load the tweets
        print("Loading tweets ..... ")
        tweets <- task_loaddata(datapath, ".csv", scrubtweet)
        save_output(tweets, "tweets.csv")
        tweet_post_histogram <- task_tweet_post_histogram(tweets)
        save_visualization(tweet_post_histogram, "post_histogram.png")
        print("Done")
        
        # Tokenize
        print("Tokenizing tweets ..... ")
        tweets_tokens <- task_tokenize(tweets, customstopwordspath, stopwordspath, synonymfilepath)
        save_output(tweets_tokens, "tokens.csv")
        print("Done")

        if(includesentiment) {
            print("Analyzing for sentiment ..... ")
            performsentimentanalysis(tweets_tokens)
            print("Done")
        }

        if(includetermfrequency) {
            print("Counting term frequency ..... ")
            computetermfrequency(tweets_tokens, minimumtermcount)
            print("Done")
        }
        
        if(includetopicmodel) {
            print("Creating topic model ..... ")
            createldatopicmodel(tweets_tokens, numbertopics, termspertopic, topicrows, topiccolumns)
            print("Done")
        }
    }

    performsentimentanalysis <- function(tweets_tokens) {
        sentiment <- task_sentimentanalysis(tweets_tokens)
        save_output(sentiment, "sentiment.csv")
        sentiment_visualization <- task_visualizesentiment(sentiment)
        save_visualization(sentiment_visualization, "sentiment.png")
    }

    computetermfrequency <- function(tweets_tokens, minimumtermcount) {
        term_frequency <- task_computetermfrequency(tweets_tokens)
        save_output(term_frequency, "term_frequency.csv")
        term_frequency_plot <- task_plottermfrequency(term_frequency, minimumtermcount)
        save_visualization(term_frequency_plot, "term_frequency.png")
    }

    createldatopicmodel <- function(tweets_tokens, numbertopics, termspertopic, topicrows, topiccolumns) {
        ldatopicmodel <- task_extracttopics(tweets_tokens, numbertopics, save_output)
        topics_visualization <- task_visualizetopics(ldatopicmodel, 
            top_n_terms = termspertopic, 
            rows = topicrows, 
            columns = topiccolumns, 
            save = save_visualization)
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