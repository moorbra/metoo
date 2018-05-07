import pandas as pd
import logging
import os

class Task:
    def __init__(self):
        self._logger = logging.getLogger('analysis')

    @property
    def logger(self):
        return self._logger

    def save_data_frame(self, dataframe, path, filename, index = False):
        dataframe.to_csv(os.path.join(path, filename), index=index)
