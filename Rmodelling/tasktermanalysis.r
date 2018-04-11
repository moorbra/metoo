library(ggplot2)

if (!exists("tasktermanalysis")){
    tasktermanalysis <- T
        task_computetermfrequency <- function(tokens) {
            return(tokens %>% count(word, sort = TRUE))
        }

        task_plottermfrequency <- function(termfrequnecies, top) {
            termfrequnecies %>%
            filter(n > top) %>%
            mutate(word = reorder(word, n)) %>%
            ggplot(aes(word, n)) +
            geom_col() +
            xlab(NULL) +
            coord_flip()
        }         
}