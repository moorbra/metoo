sapply(list.files(pattern="[.]r$", path="../../modellingscripts", full.names=TRUE), source);

scrubtweet <- function(tweet) {
    patterns <- c("[@]\\w+[ ,.:]?|[?_#.]{2,}|&amp;|[\"]|http[s?]://\\w+.\\w+[/\\w+]{0,}|^RT")
    tweet <- str_replace_all(tweet, patterns, "")
    tweet <- str_replace_all(tweet, "[ ]{2,}|[.]|\\n|[.]{3}"," ")
    tweet <- str_replace_all(tweet, "^[ ]{1,}|[ ]{1,}$","")
    tweet <- str_replace_all(tweet, "['`]", "'")
    tweet <- str_replace_all(tweet, "[Ff]eb[.][ ]14", "Feb14")
    return (tweet)
}

analysis_pipeline(
    datapath = file.path("data"),
    outputpath = file.path("analysis"),
    customstopwordspath = file.path("custom_stop_words.txt"),
    synonymfilepath = file.path("synonyms.txt"),
    outputprefix = "marchlives",
    scrubtweet = scrubtweet,
    numbertopics = 20,
    termspertopic = 15,
    topiccolumns = 2,
    topicrows = 2,
    minimumtermcount = 3000,
    includesentiment = TRUE,
    includetopicmodel = TRUE,
    includetermfrequency = TRUE,
    includetweetposthistogram = TRUE,
    sentimentrows = 4,
    sentimentcolumns = 1,
    histogramrows = 2,
    histogramcolumns = 2,
    distincttweets = FALSE
)

zip_analysis(file.path("analysis"), "marchlives")

