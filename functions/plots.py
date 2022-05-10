####################################################################
##### modules ######################################################
####################################################################

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from matplotlib.dates import MonthLocator, YearLocator, DateFormatter
from math import ceil, floor, trunc, log
from pandas.tseries.offsets import MonthBegin, MonthEnd
from scipy.stats import gmean

####################################################################
##### helper functions #############################################
####################################################################

def ticker_rounder(tick_min, tick_max, ticker_interval=1):
    tick_min = floor(tick_min/ticker_interval)*ticker_interval
    tick_max = ceil(tick_max/ticker_interval)*ticker_interval
    return tick_min, tick_max

####################################################################
##### plot functions ###############################################
####################################################################

def plot_timeseries(df
                    ,title=""
                    ,xlabel=""
                    ,ylabel=""
                    ,plot_var_mean=[]
                    ,plot_avg_year=[]
                    ,plot_latest_val=[]
                    ,plot_diff=False
                    ,fontsize=12
                    ,figsize=(18,8)
                    ,scale_factor=1
                    ):
    
    """
    inputs:
        - df:
            - (1) a pandas dataframe
            - (2) where the index is a date/datetime object and
            - (3) all columns will be ploted.
        - plot_var_mean:
            - (1) a list of columns names
            - (2) for each variable in this list, the average value of variable will be plotted.
        - plot_avg_year:
            - (1) a list of columns names
            - (2) for each variable in this list, its average value for each year will be plotted.
        - plot_diff:
            - (1) a Boolean
            - (2) if True, it will validate if there are only two series
            - (3) and then plot the difference between them (first minus second).
    
    outputs:
        - This function plots a timeseries graph with all series passed in the input df.
    """
    ####################################################
    
    # quality
    assert plot_latest_val==[] or len(plot_latest_val)==df.shape[1]
    
    # scale factor
    df = df*scale_factor
    
    # Build Image
    fig = plt.figure(figsize=figsize)
    ax = plt.axes()
    cmap = plt.get_cmap('Accent')

    # plot variables
    c=-1
    for var in df.columns:
        c+=1
        color=cmap(c)
        ax.plot(df.index
                ,df[var]
                ,label=var
                ,color=color
               )
        
        # plot var mean
        if var in plot_var_mean:
            vector_ones = np.ones(df.shape[0])
            var_mean = df[[var]].mean()[0]
            ax.plot(df.index
                    ,vector_ones*var_mean
                    ,linestyle=':'
                    ,color=color)
    
        # plot avgs
        if var in plot_avg_year:
            for year in df.index.year.unique():
                df_sup=df[df.index.year==year]
                mean = df_sup[[var]].mean()[0]
                ax.plot(df_sup.index
                        ,np.ones(len(df_sup.index))*mean
                        ,color=color
                        ,linestyle=':')
                ax.text(df_sup.index[0]
                        ,mean
                        ,round(mean,2)
                        ,size=fontsize
                        ,alpha=1.0
                        ,color=color)
        
        # plot latest value
        if plot_latest_val != []:
            if plot_latest_val[c]!= None:
                ax.scatter(df.index.max()+MonthBegin(1)
                           ,plot_latest_val[c]
                           ,color=color
                           ,marker="x"
                           ,linewidths=4
                          )

    ylim_min=df.min().min()
    ylim_max=df.max().max()
    
    ####################################################
    
    if plot_diff:
        if len(df.columns)==2:
            diff = (df[df.columns[0]]-df[df.columns[1]])
            ax.plot(df.index
                    ,diff
                    ,label=df.columns[0]+" minus "+df.columns[1]
                    ,color="red"
                   )
            ylim_min=min(ylim_min,diff.min())
            ylim_max=max(ylim_max,diff.max())
            
    
    ####################################################
    
    # format x axis
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
    fig.autofmt_xdate()
    ax.set_xlabel(xlabel,fontsize=fontsize)
    plt.xlim(df.index.min(),df.index.max()+MonthBegin(2))

    # format y axis
    ax.set_ylabel(ylabel,fontsize=fontsize)
    plt.ylim(ylim_min - abs(0.03*ylim_min)
             ,ylim_max + abs(0.03*ylim_max))

    # other elements
    ax.tick_params(axis='both'
                   ,which='major'
                   ,labelsize=fontsize-2
                  )
    ax.set_title(title, fontsize=fontsize+8, fontweight='bold', verticalalignment='bottom')
    ax.legend(loc='upper left',fontsize=fontsize)
    ax.grid(linestyle=":", linewidth=0.5, color='gray')
    
    plt.show()

def plot_histogram(df
                   ,title=""
                   ,fontsize=12
                   ,figsize=(18,8)
                  ):
    
    """
    - df: (1) a pandas dataframe (2) where the index is a date/datetime object and (3) there is only one column which will be ploted
    """
    
    fig, ax = plt.subplots(figsize=figsize)

    # plot histogram
    df.plot(kind="hist"
            ,density=True
            ,alpha=0.50
            ,bins=20
           )
    # kde requires density = True
    df.plot(kind="kde")
   
    # format X axis
    tick_min, tick_max = ax.get_xlim()
    decimals = ceil(abs(log(tick_max-tick_min,10)))+1
    x_tick_interval = 5/(10**decimals)
    tick_min, tick_max = ticker_rounder(tick_min,tick_max,x_tick_interval)
    plt.xticks(np.arange(tick_min
                         ,tick_max
                         ,x_tick_interval))
    plt.xlim(tick_min, tick_max)
        
    # quantiles
    for i in np.arange(0.05,1.00,0.05):
        quantile = df.quantile(i)
        ax.axvline(quantile, linestyle = ":")
        ax.text(quantile
                ,ax.get_ylim()[1]*i
                ,int(100*i)
                ,size=fontsize-2
                ,alpha=0.8)

    # info box with mean, median, and std
    textstr = '\n'.join((
        r'$\mu=%.4f$' % (df.mean(), ),
        r'$\mathrm{median}=%.4f$' % (np.median(df), ),
        r'$\sigma=%.4f$' % (df.std(), )))
    ax.text(0.05
            ,0.95
            ,textstr
            ,transform=ax.transAxes
            ,fontsize=fontsize+2
            ,verticalalignment='top'
            ,bbox=dict(boxstyle='round',facecolor='wheat',alpha=0.5)
           )
    
    # graph elements
    ax.grid(True)
    ax.set_title(title
                 ,size=fontsize+6)
    ax.tick_params(axis='both'
               ,which='major'
               ,labelsize=fontsize-2
              )
    for ax, spine in ax.spines.items():
        spine.set_visible(False)

    plt.show()

def plot_timeseries_stacked(df
                            ,column_to_plot="bid_yield"
                            ,column_date="date"
                            ,column_bond_name="bond_name"
                            ,title=""
                            ,figsize=(24,12)
                            ,fontsize=16
                            ,scale_factor=1
                           ):
    """
    - df: (1) a pandas dataframe (2) where the index is irrelavant.
    There are three columns requirements:
    - column_to_plot: (4) a string that identifies the column that will be ploted.
    - column_date: (5) a string that identifies the column that will be used as date. (6) The column should be a date/datetime object.
    - column_bond_name: (7) a string that identifies the column that will be used as bond_name. (8) The column should uniquely identify bonds.
    """
    
    fig = plt.figure(figsize=figsize)
    ax = plt.axes()

    # Plot multiple lines
    bonds = df[column_bond_name].unique()
    for bond in bonds:
        df_sup=df[df[column_bond_name]==bond]
        ax.plot(df_sup[column_date]
                ,df_sup[column_to_plot]*scale_factor
                ,label=bond)
        
    
    # format x axis
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
    fig.autofmt_xdate()
    plt.xlim(df[column_date].min()
             ,df[column_date].max()+MonthBegin(2)
            )
    
    # other graph elements
    ax.legend(bbox_to_anchor=(1,-0.1)
              ,ncol=ceil(len(bonds)/6)
              ,fontsize=fontsize-2
             )
    ax.set_title(title
                 ,fontsize=fontsize+8
                 ,fontweight='bold'
                 ,verticalalignment='bottom'
                )
    ax.grid(linestyle=":"
            ,linewidth=0.5
            ,color='gray'
           )
    ax.tick_params(axis='both'
                   ,which='major'
                   ,labelsize=fontsize-2
                  )
    for ax, spine in ax.spines.items():
        spine.set_visible(False)

    plt.show()