import pandas


class DfFilter:
    def __init__(self, df: pandas.DataFrame):
        self.df_filtered = df

    def first_filter(self):
        # фильтрация пустых строк
        self.df_filtered.dropna(inplace=True, axis=0, how="all")
        # фильтрация дубликатов
        self.df_filtered.drop_duplicates(inplace=True, keep='first')

    def general_filter(self, w_mode, start, stop):
        self.df_filtered = self.df_filtered[(start < self.df_filtered[w_mode]) & (self.df_filtered[w_mode] < stop)]
