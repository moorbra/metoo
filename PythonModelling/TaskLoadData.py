from Task import Task
import pandas as pd
import re
import os

class TaskLoadData(Task):

    def __init__(self, scrub_function = None, data_path = "", extension_filter = ".csv"):
        self._scrub_function = scrub_function
        self._data_path = data_path
        self._extension_filter = extension_filter

    def load_data(self, text_column = "tweet"):
        documents = self.__load_data_files()
        
        if self._scrub_function is not None:            
            documents[text_column] = documents[text_column].apply(lambda r: self._scrub_function(r))

        return documents

    def __load_data_files(self):
        frames = [self.__load_data_file(entry.path) 
                  for entry in os.scandir(self._data_path) 
                  if entry.is_file() and entry.name.endswith(self._extension_filter)]

        return pd.concat(frames)

    def __load_data_file(self, path):
        documents = pd.read_csv(path, encoding="latin-1")
        documents = documents.assign(originaltweet = lambda r: r.tweet)
        return documents

        

