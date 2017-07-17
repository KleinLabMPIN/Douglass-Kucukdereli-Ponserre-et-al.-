import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter, freqz
from imagingIO import get_fs

def dffCalc(mice, dataList, lowest=False):
    """
    """
    dFFList = {}
    for mus, sess in mice:
        data = dataList[mus]

        if lowest:
            # F0 from the lowest <lowest>% of the trace
            t_half = data.index.max() * (lowest / 100) * 0.5
            minPoint = data.idxmin(axis= 0)
            dFF = pd.DataFrame()
            for i, m in enumerate(minPoint):
                F0 = data[data.columns[i]].loc[m-t_half : m+t_half].mean(axis= 0)
                dFF[data.columns[i]] = (data[data.columns[i]] - F0) / F0 * 100
        else:
            # Calculate the dFF
            F0 = data.mean(axis= 0)
            dFF = ((data - F0) / F0) * 100

        # Put each dataframe into the new dict
        dFFList[mus] = dFF

    return dFFList

def low_pass(data, cutoff, fs, order):
    """
    """
    # set the butterworth filter
    nyq = 0.5 * (1./fs)
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # filter the data
    filtData = lfilter(b, a, data)

    return filtData

def filtData(mice, dataList, cutoff, order=4):
    """
    """
    filtList = {}
    for mus, sess in mice:
        data = dataList[mus]

        fs =  get_fs(data.index)

        for cell in data.columns:
            filtData = low_pass(data[cell], cutoff, fs, order)
            data[cell] = filtData
        filtList[mus] = data

    return filtList

def smoothData(mice, dataList, window=1):
    """
    """
    smoothList = {}
    for mus, sess in mice:
        data = dataList[mus]

        smoothData = data.rolling(window=window).mean()
        smoothList[mus] = smoothData.dropna()

    return smoothList

def normData(mice, dataList):
    """
    """
    normList = {}
    for mus, sess in mice:
        data = dataList[mus]

        normData = (data - data.min()) / (data.max() - data.min())
        normList[mus] = normData

    return normList
