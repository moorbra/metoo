FROM r-base
COPY . /home/docker
WORKDIR /home/docker
RUN Rscript -e "install.packages('tidyverse')" \
    && Rscript -e "install.packages('tidytext')"