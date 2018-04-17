import pandas as pd
import os

class Task:
    def save_data_frame(self, dataframe, path, filename, index = False):
        dataframe.to_csv(os.path.join(path, filename), index=index)
