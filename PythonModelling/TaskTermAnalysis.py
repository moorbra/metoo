from Task import Task
import pandas as pd

class TaskTermAnalysis(Task):
    def compute_term_frequency(self, tokens_data_frame):
        term_frequencies = pd.DataFrame(tokens_data_frame["token"].value_counts().reset_index())
        term_frequencies.columns = ["term", "count"]
        return term_frequencies

    def plot_term_frequency(self, term_frequency_data_frame, minimum_occurrances=500):            
        sorted_filtered = term_frequency_data_frame.query(f"count>{minimum_occurrances}").sort_values(by=["count"])
        plot = sorted_filtered.plot(kind="barh", figsize=(14,7))
        plot.set_yticklabels(sorted_filtered.term)
        return plot
                