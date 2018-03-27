FROM r-base

WORKDIR /home/docker
RUN apt-get update \
    && apt-get -y install libxml2-dev \
    && apt-get -y install libgsl0-dev \
    && apt-get -y install libudunits2-dev \
    && Rscript -e "install.packages('R.utils')" \
    && Rscript -e "install.packages('tidyverse')" \
    && Rscript -e "install.packages('tidytext')" \
    && Rscript -e "install.packages('tm')" \
    && Rscript -e "install.packages('topicmodels')" \
    && Rscript -e "install.packages('ggforce')" \
    && Rscript -e "install.packages('twitteR')"