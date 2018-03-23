sapply(list.files(pattern="[.]r$", path="../../modellingscripts", full.names=TRUE), source);

scrubtweet <- function(tweet) {
    patterns <- c("[@]\\w+[ ,.:]?|\\n|[?_#.]{2,}|&amp;|[\"]|http[s?]://\\w+.\\w+[/\\w+]{0,}|^RT|[#2]{0,1}[Mm][Ee][Tt][Oo]{2}[_]{0,1}")
    tweet <- str_replace_all(tweet, patterns, "")
    tweet <- str_replace_all(tweet, "[ ]{2,}"," ")
    tweet <- str_replace_all(tweet, "^[ ]{1,}|[ ]{1,}$","")
    return (tweet)
}

analysis_pipeline(
    file.path("data"),
    file.path("analysis"),
    "metoo",
    scrubtweet
)