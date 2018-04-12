import pandas as pd
import os

class Task:
    def save_data_frame(self, dataframe, path, filename, index = False):
        dataframe.to_csv(os.path.join(path, filename), index=index)

    # def save_plot(self, plot, path, filename):
    #     ggsave(file=os.path.join(path, filename), plot = plot)
