# -*- coding: utf-8 -*-
"""
Script for creating Google Trends data visualizations

Created on Thu May  7 13:51:34 2020

@author: MonikaFurdyna
"""
# import path to the code on your computer
from settings import path 

import os

os.chdir(path+'/dataset')
from make_dataset import make_dataset_for_plots

os.chdir(path+'/visualization')
from draw_pretty_graphs import draw_pretty_covid_graph_world

import matplotlib.pyplot as plt

os.chdir(path)

# the names of the data files that you want to plot
name_common = 'multiTimeline_'

name_categories = ['Climate','Climate_topics','Education_Online','Energy_topics',
                   'Exercise_Youtube','Food','Food_Delivery','IT_security_topics',
                   'Public_Transport','Remote_Work','Stay_Home','Sustainability_topics',
                   'Vegan_topics']
#name_categories = ['Climate']
for cat in name_categories:
     # import and process data
    data = make_dataset_for_plots('../data/raw_report/'+name_common+ cat +'.csv',': (Worldwide)')
    
    if (cat=='Climate') | (cat=='Climate_topics'):
        fig = draw_pretty_covid_graph_world(data, cat, climate=True)
    else:
        fig = draw_pretty_covid_graph_world(data, cat)
    #plt.savefig('../report/figures_report/'+'searches_over_time_'+cat+'.svg', bbox_inches='tight') # higher quality
    plt.savefig('../report/figures_report/'+'searches_over_time_'+cat+'.png', bbox_inches='tight')
    
    plt.show()
        