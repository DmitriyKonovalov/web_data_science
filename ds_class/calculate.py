import numpy as np


class Calculate:
    R0 = 287.05
    P0 = 100
    Rw = 461.5
    K0 = 273.15
    const1 = 0.0000205
    const2 = 0.0631846
    TEMP = 'TEMP_1'
    BP = 'BP_1'
    RH = 'RH_1'

    @staticmethod
    def pw(temp):
        return Calculate.const1 * np.exp(Calculate.const2 * (temp + Calculate.K0))

    @staticmethod
    def ad(df):
        return (1 / (df[Calculate.TEMP] + Calculate.K0) * ((df[Calculate.BP] * Calculate.P0) / Calculate.R0 -
                                                           (df[Calculate.RH] * Calculate.pw(df[Calculate.TEMP])) /
                                                           Calculate.P0 * (1 / Calculate.R0 - 1 / Calculate.Rw)))
