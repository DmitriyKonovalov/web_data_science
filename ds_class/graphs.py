import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas


class Graphs:
    def __init__(self, df, avg):
        self.df = pandas.DataFrame(df)
        self.avg = pandas.DataFrame(avg)

    def ws_wd(self, wd, ws, filename):
        plt.figure(figsize=(20, 10), dpi=80)
        plt.title('Wind Speed vs Wind Direction')
        plt.legend(['Wind Speed vs Wind direction'], loc="upper right", bbox_to_anchor=(1.2, 1.05))
        plt.grid(True)
        plt.scatter(self.df[wd], self.df[ws], marker='.', label=ws)
        plt.scatter(self.avg[wd], self.avg[ws], marker='^', label=ws + '_Awg')
        plt.legend()
        plt.savefig(filename)
        plt.close()

    def wind_rose(self, ws, step, filename):
        df = self.df
        fig = plt.figure(figsize=(20, 10), dpi=80)
        bins = np.arange(0, 360, step)
        labels = [item + step / 2 for item in bins]
        categories = pandas.cut(df[ws], bins, right=False, labels=labels[0:-1])
        df = df.groupby(categories).count()
        angles = df.index
        count = df[ws]
        angle = [math.radians(i) for i in angles]
        ax = fig.add_subplot(111, projection='polar')
        ax.plot(angle, count, linewidth=2, label="Wind direction")
        plt.savefig(filename)
        plt.close(fig)

    def hist(self, ws, filename):
        plt.figure(figsize=(20, 10), dpi=80)
        plt.legend(['Histogram'], loc="upper right", bbox_to_anchor=(1.2, 1.05))
        plt.title('Wind Speed Histogram')
        plt.grid(True)
        plt.hist(self.df[ws], label=ws)
        plt.savefig(filename)
        plt.close()

    def time(self, ad, filename):
        plt.figure(figsize=(20, 10), dpi=80)
        plt.title('Air Density vs Daytime')
        plt.grid(True)
        x = pandas.DatetimeIndex(self.df.index).date
        y = self.df[ad]
        plt.plot(x, y)
        plt.savefig(filename)
        plt.close()
