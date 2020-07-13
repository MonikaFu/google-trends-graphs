# -*- coding: utf-8 -*-
"""
Library with data processing function.

Converts the .csv data files dowloaded from the Google Tredns platform into a dataframe that can be processed by the data 
visualization functions.
Created on Wed May 13 16:25:04 2020

@author: MonikaFurdyna
"""

import pandas as pd
import datetime as dt

def make_dataset_for_plots(filename,remove_area,cut_off_date='2017-01-01'):
    # import data to a dataframe
    data = pd.read_csv(filename ,sep=',',skiprows=[0,1])
    
    # drop the last row - contains only predictions
    data.drop(data.tail(1).index,inplace=True)
    
    # clean column names (search terms)
    data.columns = map(lambda x: x.replace(remove_area,''),data.columns)
    
    # convert all values to numeric
    data.replace('<1','0.5', inplace=True) # remove '<1' from data
    data[data.columns[1:]] = data[data.columns[1:]].astype(float)
    
    # convert to date format
    data.Week = pd.to_datetime(data.Week)
    
    # use only data starting from the cut off date
    data = data[data.Week>=dt.datetime.strptime(cut_off_date,'%Y-%m-%d')].reset_index(drop=True)
    return data