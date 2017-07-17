import numpy as np
import pandas as pd
from imagingIO import get_fs

def find_nearest(array,value):
    """
    Find the nearest value in a given array.
    """

    ind = (np.abs(array-value)).argmin()

    return ind, array[ind]

def find_events(data, time, events):
    """
    Find the nearest value in the time index.
    """

    events_ind = []
    for i, event in enumerate(events):
        ind, nearest = find_nearest(time['Time (s)'], event)
        events_ind.append(ind)

    return events_ind

def getEvents(mice, eventList, eventType, trials):
    """
    """
    eventdf = pd.DataFrame()
    events = pd.DataFrame()
    for mus, sess in mice:
        tempdf = eventList[mus][eventType].dropna()
        #eventdf = pd.DataFrame({eventType : tempdf[trials[0]-1:trials[1]].values}, tempdf.index)
        eventdf[eventType] = tempdf[trials[0]-1:trials[1]].values
        eventdf['Mouse'] = mus
        eventdf['Trial'] = np.arange(trials[0],trials[1]+1)
        events = events.append(eventdf)

    return events.pivot_table(index='Trial', columns='Mouse', values=eventType)
