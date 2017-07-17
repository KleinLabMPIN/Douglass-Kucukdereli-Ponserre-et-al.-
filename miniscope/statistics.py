import pandas as pd
import numpy as np
import scipy.stats as stat

def stdCalc(mice, dataList):
    """
        Calculate the standard deviation for each cell.
    """
    stdList = pd.DataFrame()
    for mus, sess in mice:
        stdList = stdList.append(pd.DataFrame({'Std':dataList[mus].std().values}, index=dataList[mus].columns))
    return stdList

def getStats(boutMeans, choice, parameter, p_val=0.05):
    """
        'Mean', 'Max', 'Auc'
    """
    stats = pd.DataFrame()
    cellNames = boutMeans['Cell'].drop_duplicates().values
    for cell in cellNames:
        x = boutMeans.pivot_table(index='Event', columns='Cell', values='Baseline_'+str(parameter))[cell]
        y = boutMeans.pivot_table(index='Event', columns='Cell', values='Bout_'+str(parameter))[cell]

        T_wilc, p_wilc = stat.wilcoxon(x, y)
        T_rank, p_rank = stat.ranksums(x, y)

        if y.mean() > x.mean():
            PInd = 1 * np.absolute((y.mean() - x.mean()) / (y.mean() + x.mean()))
        elif y.mean() < x.mean():
            PInd = -1 * np.absolute((y.mean() - x.mean()) / (y.mean() + x.mean()))
        elif y.mean() == x.mean():
            PInd = 0

        temp = pd.DataFrame()
        temp['Cell'] = [cell]
        temp['Wilcoxon'] = [p_wilc]
        temp['Ranksum'] = [p_rank]
        temp['PInd'] = [PInd]
        temp['Baseline_'+str(parameter)] = [x.mean()]
        temp['Bout_'+str(parameter)] = [y.mean()]

        if p_wilc < p_val:
            temp['Wilcoxon Result'] = ['*']
        else:
            temp['Wilcoxon Result'] = ['ns']
        if p_rank < p_val:
            temp['Ranksum Result'] = ['*']
        else:
            temp['Ranksum Result'] = ['ns']

        if choice == 'Wilcoxon':
            p = p_wilc
        elif choice == 'Ranksum':
            p = p_rank

        if PInd > 0.0:
            temp['Preference'] = ['Positive']
            if p < p_val:
                temp['Class'] = ['Up']
            else:
                temp['Class'] = ['None']
        elif PInd < 0:
            temp['Preference'] = ['Negative']
            if p < p_val:
                temp['Class'] = ['Down']
            else:
                temp['Class'] = ['None']
        elif PInd == 0:
            if p < p_val:
                temp['Class'] = ['None']
            else:
                temp['Class'] = ['None']

        stats = stats.append(temp)
    stats = stats.reset_index(drop=True)

    upPercent = len(stats[stats['Class'] == 'Up']['Class'])*1.0 / len(stats['Class']) * 100.0
    downPercent = len(stats[stats['Class'] == 'Down']['Class'])*1.0 / len(stats['Class']) * 100.0
    nanPercent = len(stats[stats['Class'] == 'None']['Class'])*1.0 / len(stats['Class']) * 100.0

    percentages = pd.DataFrame({'Up' : [upPercent], 'Down' : [downPercent], 'None' : [nanPercent]}, index=['Percentage (%)'])

    stats.set_index('Cell', drop=True, inplace=True)

    return stats, percentages

def getBoutMeans(mice, boutsData, behType, trials, base, fs):
    """
        Use this one for fixed length baseline.
    """
    # Get the cell names
    cellNames = boutsData['Cell'].drop_duplicates().values

    # Calculate the bout and baseline means
    boutMeans = pd.DataFrame()
    for i, cell in enumerate(cellNames):
        boutDF = pd.DataFrame()

        # Calculate mean, max and auc for baseline
        baseline = boutsData.reset_index(drop=True).pivot_table(index=['Event'], columns=['Cell', 'New_Time'], values='Fluoro')[cell].T.loc[base:0.00]
        baselineMean = baseline.mean(axis=0).values
        boutDF['Baseline_Mean'] = baselineMean

        baselineMax = baseline.max().values
        boutDF['Baseline_Max'] = baselineMax

        baselineAuc = np.array([])
        for j in np.arange(trials[0], trials[1]+1):
            baselineAucVal = np.trapz(baseline[j], dx=fs)
            baselineAuc = np.append(baselineAuc, baselineAucVal)
        boutDF['Baseline_Auc'] = baselineAuc

        # Calculate mean, max and auc for bout
        bout = boutsData.reset_index(drop=True).pivot_table(index=['Event'], columns=['Cell', 'New_Time'], values='Fluoro')[cell].T.loc[0.00:]
        boutMean = bout.mean(axis=0).values
        boutDF['Bout_Mean'] = boutMean

        boutMax = bout.max().values
        boutDF['Bout_Max'] = boutMax

        boutAuc = np.array([])
        for i in np.arange(trials[0], trials[1]+1):
            boutAucVal = np.trapz(bout[i].dropna(), dx=fs)
            boutAuc = np.append(boutAuc, boutAucVal)
        boutDF['Bout_Auc'] = boutAuc

        boutDF['Cell'] = cell
        boutDF['Event'] = np.arange(trials[0], trials[1]+1)
        boutMeans = boutMeans.append(boutDF)

    return boutMeans

def getBoutMeans_(mice, boutsData, behType, trials, base, fs):
    """
        Use this one for variable length baseline.
    """
    # Get the cell names
    cellNames = boutsData['Cell'].drop_duplicates().values

    # Calculate the bout and baseline means
    boutMeans = pd.DataFrame()
    for i, cell in enumerate(cellNames):
        boutDF = pd.DataFrame()

        # Calculate mean, max and auc for the baseline
        # Calculate mean
        baseInd = boutsData.reset_index(drop=True).pivot_table(index=['Event'], columns=['Cell', 'New_Time'], values='Fluoro')[cell].T.index[0]
        baseline = boutsData.reset_index(drop=True).pivot_table(index=['Event'], columns=['Cell', 'New_Time'], values='Fluoro')[cell].T.loc[baseInd:0.00]
        baselineMean = baseline.mean(axis=0).values
        boutDF['Baseline_Mean'] = baselineMean

        # Calculate max
        baselineMax = baseline.max().values
        boutDF['Baseline_Max'] = baselineMax

        # Calculate auc
        baselineAuc = np.array([])
        for j in np.arange(trials[0], trials[1]+1):
            baselineAucVal = np.trapz(baseline[j].dropna(), dx=fs)
            baselineAuc = np.append(baselineAuc, baselineAucVal)
        boutDF['Baseline_Auc'] = baselineAuc

        # Calculate mean, max and auc for the bout
        # Calculate mean
        bout = boutsData.reset_index(drop=True).pivot_table(index=['Event'], columns=['Cell', 'New_Time'], values='Fluoro')[cell].T.loc[0.00:]
        boutMean = bout.mean(axis=0).values
        boutDF['Bout_Mean'] = boutMean

        # Calculate max
        boutMax = bout.max().values
        boutDF['Bout_Max'] = boutMax

        # Calculate auc
        boutAuc = np.array([])
        for i in np.arange(trials[0], trials[1]+1):
            boutAucVal = np.trapz(bout[i].dropna(), dx=fs)
            boutAuc = np.append(boutAuc, boutAucVal)
        boutDF['Bout_Auc'] = boutAuc

        boutDF['Cell'] = cell
        boutDF['Event'] = np.arange(trials[0], trials[1]+1)
        boutMeans = boutMeans.append(boutDF)

    return boutMeans

def baselineBouts(boutMeans):
    cellNames = boutMeans['Cell'].drop_duplicates()
    boutDF = boutMeans
    for cell in cellNames:
        baseMean = boutMeans[boutMeans['Cell'] == cell]['Baseline_Mean'].mean()
        baseMax = boutMeans[boutMeans['Cell'] == cell]['Baseline_Max'].mean()
        baseAuc = boutMeans[boutMeans['Cell'] == cell]['Baseline_Auc'].mean()

        #boutDF[boutDF['Cell'] == cell]['Baseline_Mean'] = boutDF[boutDF['Cell'] == cell]['Baseline_Mean'] - base
        #boutDF[boutDF['Cell'] == cell]['Bout_Mean'] = boutDF[boutDF['Cell'] == cell]['Bout_Mean'] - base

        boutDF.loc[boutDF['Cell'] == cell, 'Baseline_Mean'] = boutDF.loc[boutDF['Cell'] == cell, 'Baseline_Mean'] - baseMean
        boutDF.loc[boutDF['Cell'] == cell, 'Baseline_Max'] = boutDF.loc[boutDF['Cell'] == cell, 'Baseline_Max'] - baseMax
        boutDF.loc[boutDF['Cell'] == cell, 'Baseline_Auc'] = boutDF.loc[boutDF['Cell'] == cell, 'Baseline_Auc'] - baseAuc

    return boutDF
