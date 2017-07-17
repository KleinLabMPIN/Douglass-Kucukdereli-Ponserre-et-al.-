import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colr

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colr.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def plotMean(mean, sem, time, eventType):
    plt.style.use('classic')
    # Set the font dictionaries (for plot title and axis titles)
    font = {'sans-serif' : 'Arial',
            'weight' : 'normal',
            'size'   : 18}
    plt.rc('font', **font)

    fig = plt.figure(figsize=(4,3), facecolor="w", dpi= 150)
    ax = plt.subplot(111)

    line = 1.5
    colors = ('#BCBEC0', '#0070C0', '#BCBEC0', '#0070C0')

    ## labels
    ax.set_xlabel("Time (sec)")
    ax.set_ylabel("dF/F (%)")
    #ax.set_title("Aligned to event::Update the title", fontsize= 12)

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_top()
    ax.get_yaxis().tick_left()

    ## adjust the spines and ticks
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_linewidth(line)
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_linewidth(line)
    ax.spines['bottom'].set_position(('outward', 10))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ## decorate the axes
    ax.tick_params(axis='y', color= '#000000', width= line, direction='out', length= 8, which='major', pad=10)
    ax.tick_params(axis='x', color= '#000000', width= line, direction='out', length= 8, which='major', pad=12)

    ax.fill_between(time, mean+sem, mean-sem, facecolor=colors[0], linewidth=0, alpha=1.0, zorder=-5)
    cat, = ax.plot(time, mean, colors[1], label=eventType)
    #ax.fill_between(time, meanstart+semstart, meanstart-semstart, facecolor=colors[1], linewidth=0, alpha=0.3, zorder=-5)
    #cat1, = ax.plot(time, meanstart, colors[1], label='Start')
    #ax.fill_between(time, meancontact+semcontact, meancontact-semcontact, facecolor=colors[0], linewidth=0, alpha=0.3, zorder=-5)
    #cat2, = ax.plot(time, meancontact, colors[0], label='Contact')

    ax.plot([0, 0],[-1, 5], 'gray', linestyle='--', linewidth=line*1.2, alpha=0.7, zorder=-56)
    ax.text(0, 5, eventType)
    #ax.set_ylim([-1., 2.])

    if False:
        ## add the legend
        ax.legend([cat1, cat2], ['Start', 'Contact'])
        handles, labels = ax.get_legend_handles_labels()
        legend = plt.legend(loc= 'upper left', fontsize= 18, handles=handles, handlelength= 1.2, handleheight= 0.8, handletextpad= 0.5, frameon= False)

    #plt.tight_layout()
    return fig, ax

def plotHeat(eventsData, eventType, base, duration, trials, fs, vlim=False):
    #C = np.loadtxt("J:\\Hakan Kucukdereli\\Miniscope_Behaviour_MPIN\\scripts\\analysis\\colormaps\\dusk.txt")
    #cm = colr.ListedColormap(C/255.0)
    #C_r = np.flipud(C)
    #cm_r = colr.ListedColormap(C_r/255.0)

    heatData = eventsData.pivot_table(index=['Event'], columns='New_Time', aggfunc=np.mean)
    heatData['Fluoro'].columns
    heatData.mean(axis=1)

    plt.style.use('classic')
    # Set the font dictionaries (for plot title and axis titles)
    font = {'sans-serif' : 'Arial',
            'weight' : 'normal',
            'size'   : 18}
    plt.rc('font', **font)

    fig = plt.figure(figsize=(6,5), facecolor="w", dpi= 150)
    ax = plt.subplot(111)

    line = 1.5
    colors = ('#BCBEC0', '#0070C0', '#BCBEC0', '#0070C0')

    cmap = plt.get_cmap('PiYG_r')
    cmap(np.linspace(0.3, 0.55, 100))

    #if vlim:
    #plt.pcolor(heatData, cmap=plt.cm.PiYG_r, linewidth=line, linestyle='solid', vmin=vlim[0], vmax=vlim[1])
    ##cmap = plt.get_cmap('PiYG_r')e
    ##new_cmap = truncate_colormap(cmap, 0.5, 0.8)
    plt.pcolor(heatData, cmap=plt.cm.hot, linewidth=line, linestyle='solid', vmin=vlim[0], vmax=vlim[1])
    #else:
        #plt.pcolor(heatData, cmap=plt.cm.PiYG_r, linewidth=line, linestyle='solid')
    ax.invert_yaxis()
    cbar = plt.colorbar(ax=ax)
    cbar.set_label("Normalized dF/F")

    ## labels
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Trial #')
    ax.set_title(eventType)

    ## decorate the axes
    #ax.tick_params(axis='y', color= '#000000', width= line, direction='in', length= 4, which='major', pad=10)
    #ax.tick_params(axis='x', color= '#000000', width= line, direction='in', length= 4, which='major', pad=12)
    time_ax = np.arange(base, duration+0.001, 5.0)
    ax.set_xticks(np.linspace(0, (-base+duration)/fs, len(time_ax)))
    ax.set_xticklabels(time_ax)
    ax.set_yticks(np.linspace(trials[0]-0.5, trials[1]-0.5, 2))
    ax.set_yticklabels(np.linspace(trials[0], trials[1], 2, dtype=int))

    ax.plot([-base/fs, -base/fs], list(ax.get_ylim()), 'w', linestyle='--', linewidth=line*1.2, alpha=1., zorder=111)

    return fig, ax

def plotTrials(trialMeans, time, base, duration, eventType, trials, f):
    # Plot the trial means
    plt.style.use('classic')
    # Set the font dictionaries (for plot title and axis titles)
    font = {'sans-serif' : 'Arial',
            'weight' : 'normal',
            'size'   : 18}
    plt.rc('font', **font)
    fig = plt.figure(figsize=(4,8), facecolor="w", dpi= 150)
    ax = plt.subplot(111)

    line = 1.5
    colors = ('#BCBEC0', '#0070C0', '#BCBEC0', '#0070C0')

    x_offset = np.arange(0.0, trials[1]*f, f)
    y_offset = np.arange(0.0, trials[1]*f, f)

    ax.set_ylabel('dF/F (%)')
    ax.set_xlabel('Time (s)')
    ax.set_title(eventType)

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_top()
    ax.get_yaxis().tick_left()

    ## adjust the spines and ticks
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_linewidth(line)
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_linewidth(line)
    ax.spines['bottom'].set_position(('outward', 10))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ## decorate the axes
    ax.tick_params(axis='y', color= '#000000', width= line, direction='out', length= 8, which='major', pad=10)
    ax.tick_params(axis='x', color= '#000000', width= line, direction='out', length= 8, which='major', pad=12)

    for i, trial in enumerate(range(trials[0], trials[1]+1)):
        df = trialMeans[trialMeans['Trial'] == trial]

        line = 1.5
        colors = ('#BCBEC0', '#0070C0', '#BCBEC0', '#0070C0')

        ax.fill_between(time, df['Mean']+df['Sem']-y_offset[i], df['Mean']-df['Sem']-y_offset[i], facecolor=colors[1], linewidth=0, alpha=0.3, zorder=-5)
        cat, = ax.plot(time, df['Mean']-y_offset[i], colors[1], label=eventType)
        ax.text(base-2, -y_offset[i]+1,'trial_'+str(i+1), fontsize=12)

    ax.set_xlim(base-5, duration)
    ax.plot([0, 0], [10, -35], 'gray', linestyle='--', linewidth=line, alpha=0.7)

    return fig, ax

def plotHeatTrials(heatData, eventType, base, duration, trials, fs, figsize=(5,5), seperate=False, vmin=-1.0, vmax=1.0):
    C = np.loadtxt("J:\\Hakan Kucukdereli\\Miniscope_Behaviour_MPIN\\scripts\\analysis\\colormaps\\magenta.txt")
    cm = colr.ListedColormap(C/255.0)
    C_r = np.flipud(C)
    cm_r = colr.ListedColormap(C_r/255.0)
    cmap = plt.get_cmap(cm_r)
    new_cmap = truncate_colormap(cmap, 0.2, 1.0)

    [row, col] = heatData.shape

    vlim=False
    plt.style.use('classic')
    # Set the font dictionaries (for plot title and axis titles)
    font = {'sans-serif' : 'Arial',
            'weight' : 'normal',
            'size'   : 18}
    plt.rc('font', **font)

    fig = plt.figure(figsize=figsize, facecolor="w", dpi= 150)
    ax = plt.subplot(111)

    line = 1.5
    colors = ('#BCBEC0', '#0070C0', '#BCBEC0', '#0070C0')

    plt.pcolor(heatData, cmap=plt.cm.hot, linewidth=line, linestyle='solid', vmin=vmin, vmax=vmax)

    ax.set_yticks(np.linspace(0.5, row-0.5, 2))
    ax.set_yticklabels(np.linspace(1, row, 2, dtype=int))
    ax.set_ylim(0, row)

    ax.invert_yaxis()
    cbar = plt.colorbar(ax=ax)
    cbar.set_label("Normalized dF/F")

    ## labels
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Cell # -or- Trial #')
    ax.set_title(eventType)

    ## decorate the axes
    #ax.tick_params(axis='y', color= '#000000', width= line, direction='in', length= 4, which='major', pad=10)
    #ax.tick_params(axis='x', color= '#000000', width= line, direction='in', length= 4, which='major', pad=12)
    time_ax = np.arange(base, duration+0.001, 5.0)
    ax.set_xticks(np.linspace(0, (-base+duration)/fs, len(time_ax)))
    ax.set_xticklabels(time_ax)

    ax.plot([-base/fs, -base/fs], list(ax.get_ylim()), 'w', linestyle='--', linewidth=line*1.2, alpha=1., zorder=111)

    if seperate:
        for i in np.arange(trials[0], trials[1]):
            ax.plot([0, col],[i*row/trials[1], i*row/trials[1]], 'k', zorder=88)

    return fig, ax

def plotHeatTrialsNoV(heatData, eventType, base, duration, trials, fs, figsize=(5,5), seperate=False):
    [row, col] = heatData.shape

    vlim=False
    plt.style.use('classic')
    # Set the font dictionaries (for plot title and axis titles)
    font = {'sans-serif' : 'Arial',
            'weight' : 'normal',
            'size'   : 18}
    plt.rc('font', **font)

    fig = plt.figure(figsize=figsize, facecolor="w", dpi= 150)
    ax = plt.subplot(111)

    line = 1.5
    colors = ('#BCBEC0', '#0070C0', '#BCBEC0', '#0070C0')

    plt.pcolor(heatData, cmap=plt.cm.hot, linewidth=line, linestyle='solid')

    ax.set_yticks(np.linspace(0.5, row-0.5, 2))
    ax.set_yticklabels(np.linspace(1, row, 2, dtype=int))
    ax.set_ylim(0, row)

    ax.invert_yaxis()
    cbar = plt.colorbar(ax=ax)
    cbar.set_label("Normalized dF/F")

    ## labels
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Cell # -or- Trial #')
    ax.set_title(eventType)

    ## decorate the axes
    #ax.tick_params(axis='y', color= '#000000', width= line, direction='in', length= 4, which='major', pad=10)
    #ax.tick_params(axis='x', color= '#000000', width= line, direction='in', length= 4, which='major', pad=12)
    time_ax = np.arange(base, duration+0.001, 5.0)
    ax.set_xticks(np.linspace(0, (-base+duration)/fs, len(time_ax)))
    ax.set_xticklabels(time_ax)

    ax.plot([-base/fs, -base/fs], list(ax.get_ylim()), 'w', linestyle='--', linewidth=line*1.2, alpha=1., zorder=111)

    if seperate:
        for i in np.arange(trials[0], trials[1]):
            ax.plot([0, col],[i*row/trials[1], i*row/trials[1]], 'k', zorder=88)

    return fig, ax
