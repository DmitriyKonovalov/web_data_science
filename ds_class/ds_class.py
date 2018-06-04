import os

import pandas as pd

from ds_class.calculate import Calculate
from ds_class.df_filter import DfFilter
from ds_class.df_group import DfGroup
from ds_class.graphs import Graphs


class DataScienceRun():
    def __init__(self, analysis_args, output_dir):
        self.analysis_args = analysis_args
        self.output_dir = output_dir

    def data_science_execute(self):
        args = self.analysis_args
        output = self.output_dir
        df = DfFilter(pd.read_csv(args['file_data'], sep=';', index_col="Timestamp"))

        df.first_filter()
        df.general_filter(args['ws'], args['ws_start'], args['ws_stop'])
        df.general_filter(args['wd'], args['wd_start'], args['wd_stop'])
        df.df_filtered["AD_1"] = Calculate.ad(df.df_filtered)
        filtered_file = "{}_filtered.csv".format(args['name'])

        pd.DataFrame.to_csv(df.df_filtered, os.path.join(output, filtered_file))
        df_group = DfGroup(df.df_filtered)
        df_group.group_df(args['wd'], args['wd_start'], args['wd_stop'], args['wd_step'])
        df_group.df_grouped = df_group.df_grouped.mean()
        group_file = "{}_group.csv".format(args['name'])

        pd.DataFrame.to_csv(df_group.df_grouped, os.path.join(output, group_file))

        graph = Graphs(df.df_filtered, df_group.df_grouped)
        graph.wind_rose(args['wd'], args['wd_step'], os.path.join(output, '{}_wd_rose.png'.format(args['name'])))
        graph.hist(args['ws'], os.path.join(output, '{}_hist.png'.format(args['name'])))
        graph.time("AD_1", os.path.join(output, '{}_time.png'.format(args['name'])))
        graph.ws_wd(args['wd'], args['ws'], os.path.join(output, '{}_ws_wd.png'.format(args['name'])))
