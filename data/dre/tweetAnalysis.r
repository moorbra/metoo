sapply(list.files(pattern="[.]r$", path="../../RModelling/modellingscripts", full.names=TRUE), source);

scrubtweet <- function(tweet) {
    patterns <- c("[@]\\w+[ ,.:]?|\\n|[?_#.]{2,}|&amp;|[\"]|http[s?]://\\w+.\\w+[/\\w+]{0,}|^RT")
    tweet <- str_replace_all(tweet, patterns, "")
    tweet <- str_replace_all(tweet, "[ ]{2,}"," ")
    tweet <- str_replace_all(tweet, "^[ ]{1,}|[ ]{1,}$","")
    return (tweet)
}

analysis_pipeline(
    datapath = file.path("data"),
    outputpath = file.path("analysis"),
    customstopwordspath = file.path("custom_stop_words.txt"),
    synonymfilepath = file.path("synonyms.txt"),
    outputprefix = "altonsterling",
    scrubtweet = scrubtweet,
    numbertopics = 20,
    termspertopic = 15,
    topiccolumns = 2,
    topicrows = 2,
    minimumtermcount = 50,
    includesentiment = TRUE,
    includetopicmodel = TRUE,
    includetermfrequency = TRUE,
    includetweetposthistogram = TRUE,
    sentimentrows = 4,
    sentimentcolumns = 1,
    histogramrows = 2,
    histogramcolumns = 2    
)

zip_analysis(file.path("analysis"), "marchlives")

