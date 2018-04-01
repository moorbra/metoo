if (!exists("analysispipeline")){
    analysispipeline <- T
    
    analysis_pipeline <- function(datapath, outputpath, outputprefix, 
        scrubtweet = scrubscrubtweet_default, 
        customstopwordspath = "", synonymfilepath = "",
        numbertopics = 5, termspertopic = 10, topiccolumns = 1, topicrows = 1,
        sentimentrows = 1, sentimentcolumns = 1,
        histogramrows = 1, histogramcolumns = 1,
        minimumtermcount = 500,
        includesentiment = TRUE, includetopicmodel = TRUE, 
        includetermfrequency = TRUE,
        includetweetposthistogram = TRUE) {
        
        datapath <- datapath
        outputpath <<- outputpath
        outputprefix <<- outputprefix
        
        # Load the tweets
        log("Loading tweets ..... ")
        tweets <- task_loaddata(datapath, ".csv", scrubtweet)
        save_output(tweets, "tweets.csv")

        if(includetweetposthistogram) {
            createtweetposthistogram(tweets, histogramrows, histogramcolumns)
        }
        
        log("Tokenizing tweets ..... ")
        tweets_tokens <- task_tokenize(tweets, customstopwordspath, stopwordspath, synonymfilepath)
        save_output(tweets_tokens, "tokens.csv")

        if(includesentiment) {
            log("Analyzing for sentiment ..... ")
            performsentimentanalysis(tweets_tokens, sentimentrows, sentimentcolumns)
        }

        if(includetermfrequency) {
            log("Counting term frequency ..... ")
            computetermfrequency(tweets_tokens, minimumtermcount)
        }
        
        if(includetopicmodel) {
            log("Creating topic model ..... ")
            createldatopicmodel(tweets_tokens, numbertopics, termspertopic, topicrows, topiccolumns)
            log("Finished topic model")
        }
    }

    log <- function(message) {
        print(paste(Sys.time(), message))
    }

    createtweetposthistogram <- function(tweets, rows, columns) {
        task_tweet_post_histogram(tweets, rows, columns, save_visualization)
    }

    performsentimentanalysis <- function(tweets_tokens, sentimentrows, sentimentcolumns) {
        sentiment <- task_sentimentanalysis(tweets_tokens)
        save_output(sentiment, "sentiment.csv")
        task_visualizesentiment(sentiment, sentimentrows, sentimentcolumns, save_visualization)        
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

    zip_analysis <- function(outputpath, outputprefx) {
        files2zip <- dir(path = outputpath, pattern = ".png$|.csv$", full.names = TRUE)
        zip(zipfile = paste(outputpath, paste(outputprefx,format(Sys.time(), "%m%d%Y%H%M%S"), sep = "_"), sep = "/"), files = files2zip)
        file.remove(files2zip)
    }
}