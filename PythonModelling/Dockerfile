FROM python

RUN mkdir models
COPY install.py models
WORKDIR models

RUN pip install --upgrade gensim \
    && pip install --upgrade numpy \
    && pip install --upgrade scipy \
    && pip install --upgrade Pyro4 \
    && pip install --upgrade nltk \
    && pip install --upgrade pandas \
    && pip install --upgrade pprintpp \
    && pip install --upgrade ggplot \
    && python install.py

CMD ["bash"]