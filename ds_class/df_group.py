import numpy as np
import pandas


class DfGroup:
    def __init__(self, df: pandas.DataFrame):
        self.df_grouped = df

    def group_df(self, ncourse, start, stop, step):
        bins = np.arange(start, stop + step, step)
        labels = bins[:-1] + step / 2
        categories = pandas.cut(self.df_grouped[ncourse], bins, right=False, labels=labels)
        self.df_grouped = self.df_grouped.groupby(categories)
