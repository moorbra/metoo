sapply(list.files(pattern="[.]r$", path="../../modellingscripts", full.names=TRUE), source);

scrubtweet <- function(tweet) {
    patterns <- c("[@]\\w+[ ,.:]?|\\n|[?_#.]{2,}|&amp;|[\"]|http[s?]://\\w+.\\w+[/\\w+]{0,}|^RT")
    tweet <- str_replace_all(tweet, patterns, "")
    tweet <- str_replace_all(tweet, "[ ]{2,}"," ")
    tweet <- str_replace_all(tweet, "^[ ]{1,}|[ ]{1,}$","")
    return (tweet)
}

analysis_pipeline(
    file.path("data"),
    file.path("analysis"),
    "neveragain",
    scrubtweet
)

