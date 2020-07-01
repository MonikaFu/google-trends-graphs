# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:15:14 2020

@author: MonikaFurdyna
"""

import matplotlib.pyplot as P#, matplotlib.patches as MP
import datetime as dt
import pandas as pd

df_colors_light = pd.DataFrame([[140, 140, 140],[136, 189, 230],[251,178,88],[144,205,151],
                                [246,170,201],[191,165,84],[188,153,199],[237,221,70],
                                [240,126,110]],
                                index=['grey','blue','orange','green','pink','brown','violet','yellow','red'],
                                columns=['R','G','B'])  
df_colors_medium = pd.DataFrame([[77,77,77],[93,165,218],[250,164,58],[96,189,104],
                                [241,124,176],[178,145,47],[178,118,178],[222,207,63],
                                [241,88,84]],
                                index=['grey','blue','orange','green','pink','brown','violet','yellow','red'],
                                columns=['R','G','B'])  
df_colors_dark = pd.DataFrame([[0,0,0],[38,93,171],[223,92,36],[5,151,72],
                                [229,18,111],[157,114,42],[123,58,150],[199,180,46],
                                [203,32,39]],
                                index=['grey','blue','orange','green','pink','brown','violet','yellow','red'],
                                columns=['R','G','B'])  
color_palettes_show_me_the_numbers = {'light':df_colors_light,'medium':df_colors_medium,'dark_bright':df_colors_dark}

def convert_color_to_matplotlib_tuple(rgb_list):
    rgb_list = [col/255 for col in rgb_list]
    return tuple(rgb_list)

def draw_pretty_graph_timeseries_lines(data, timeseries_label, xlabel, ylabel):
    # some settings
        P.rc('figure',figsize=[21,7])    # we wish to work at the final graph size
                                        # in this case 5in x 3in
        
        #P.rc('font',family='Helvetica',size=10) # work in standard sans-serif
        #P.rc('mathtext',fontset='stixsans')     # with math from www.stixfonts.org
        
        P.rc('font',family='serif',size=18,weight='normal')   # OR: work in standard serif
        P.rc('mathtext',fontset='stix')
        
        P.rc('pdf',fonttype=3)          # for proper subsetting of fonts
                                        # but use fonttype=42 for Illustrator editing
        
        P.rc('axes',linewidth=1)      # thin axes; the default for lines is 1pt
        
        axes = P.axes([0.1,0.15,            # location of frame within figure:
                       1 - 0.1  - 0.02,     # x, y, dx, dy
                       1 - 0.15 - 0.02])
        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)
        axes.spines['left'].set_color('darkgrey')
        axes.spines['bottom'].set_color('darkgrey')
        # plot takes all the usual matlab options
        colors_to_use = color_palettes_show_me_the_numbers['dark_bright'].index.to_list()[:len(data.columns)-1]
        plot_colors = []
        for col,colour in zip(data.columns[1:],colors_to_use):
            plot_colors.append(convert_color_to_matplotlib_tuple(color_palettes_show_me_the_numbers['dark_bright'].loc[colour].to_list()))
            P.plot(data.Week,data[col],linewidth = 1,
                   color=plot_colors[-1])
        
        # restrict the axis to where we want it
        P.axis([data[timeseries_label].iloc[0],data[timeseries_label].iloc[-1],0,100])
        
        # labels --- in all text, feel free to mix in LaTeX expressions
        P.xlabel(xlabel, horizontalalignment='center')
        axes.xaxis.set_label_coords(0.5,-0.075)
        
        #  wrap the y label if too long
        P.ylabel(ylabel,rotation='horizontal', horizontalalignment='center')
        # offset the ylabel slightly
        axes.yaxis.set_label_coords(-0.075,0.5)
        
        
        def add_corrected_labels_locations(text_y_locations_dict,idx,curr_y,offset):
            if not text_y_locations_dict:
                text_y_locations_dict[idx] = curr_y
            else:
                test_list = [abs(curr_y - dict_y)<2.5 for dict_y in text_y_locations_dict.values()]
                if not any(test_list):
                    text_y_locations_dict[idx] = curr_y
                else:
                    close_key = [key for i,(key,val) in enumerate(text_y_locations_dict.items()) if abs(curr_y - val)<2.5]    
                    for key in close_key:
                        if text_y_locations_dict[key] > curr_y:
                            text_y_locations_dict[key] += offset
                            curr_y -= offset
                        else:
                            text_y_locations_dict[key] -= offset
                            curr_y += offset
                    text_y_locations_dict[idx] = curr_y
            return text_y_locations_dict
        
        # annotate labels next to the lines instead of legend
        text_y_locations_dict = {}
        text_y_locations_dict_new = {}
        iterations = 0
        for i in range(1,len(data.columns)):
            text_y_locations_dict_new = add_corrected_labels_locations(text_y_locations_dict,i,data.iloc[-1,i],1.5)
            while (text_y_locations_dict_new != text_y_locations_dict) & (iterations < 20):
                text_y_locations_dict = text_y_locations_dict_new
                text_y_locations_dict_new = add_corrected_labels_locations(text_y_locations_dict,i,data.iloc[-1,i],1.5)
                iterations += 1
            
        for i in range(1,len(data.columns)):
            dataxy = (data[timeseries_label].iloc[-1],data.iloc[-1,i])
            colortextxy = (data[timeseries_label].iloc[-1]+dt.timedelta(days=4),text_y_locations_dict[i])
            textxy = (data[timeseries_label].iloc[-1]+dt.timedelta(days=23),text_y_locations_dict[i])
            P.annotate(u"\u2014",dataxy,colortextxy,weight='bold',
                       verticalalignment='center',horizontalalignment='left',
                   color = (plot_colors[i-1][0],plot_colors[i-1][1],plot_colors[i-1][2]),annotation_clip=False)
            P.annotate(data.columns[i],dataxy,textxy,
                       verticalalignment='center',horizontalalignment='left',
                   annotation_clip=False)
            
        return 
    
def draw_pretty_covid_graph_nl(data):
    
    draw_pretty_graph_timeseries_lines(data, 'Week', 'Week (start date)', 'Relative \n number \n of searches')

        # annotate points
    idx_first_case = data.index[data.Week==dt.datetime.strptime('2020-02-23','%Y-%m-%d')] #27th February
    dataxy = (data.Week[idx_first_case],0)
    textxy = (data.Week[idx_first_case],104)
    P.annotate('First \n COVID-19 case \n in the Netheralands',dataxy,textxy,
               verticalalignment='center',horizontalalignment='center',color = 'dimgrey',
               arrowprops={'arrowstyle': '-','color':'silver'},annotation_clip=False)
    
    idx_measures_nl = data.index[data.Week==dt.datetime.strptime('2020-03-08','%Y-%m-%d')] #12th March
    dataxy = (data.Week[idx_measures_nl],0)
    textxy = (data.Week[idx_measures_nl],130)
    P.annotate('Measures introduced \n for the entire Netheralands',dataxy,textxy,
               verticalalignment='center',horizontalalignment='center',color = 'dimgrey',
               arrowprops={'arrowstyle': '-','color':'silver'},annotation_clip=False)
    
    idx_strict_measures = data.index[data.Week==dt.datetime.strptime('2020-03-22','%Y-%m-%d')] #23th March
    dataxy = (data.Week[idx_strict_measures],0)
    textxy = (data.Week[idx_strict_measures],115)
    P.annotate('Stricter social distancing \n rules are introduced',dataxy,textxy,
               verticalalignment='center',horizontalalignment='center',color = 'dimgrey',
               arrowprops={'arrowstyle': '-','color':'silver'},annotation_clip=False)
    
    fig = P.gcf()
    
    return fig

def draw_pretty_covid_graph_world(data, climate=False):
    
    draw_pretty_graph_timeseries_lines(data, 'Week', 'Week (start date)', 'Relative \n number \n of searches')

    # annotate points
    idx_first_case = data.index[data.Week==dt.datetime.strptime('2019-12-29','%Y-%m-%d')] #31st December
    dataxy = (data.Week[idx_first_case],0)
    textxy = (data.Week[idx_first_case],104)
    P.annotate('China: cluster of \n 41 cases of \n a myserious pneumonia',dataxy,textxy,
               verticalalignment='center',horizontalalignment='center', color = 'dimgrey',
               arrowprops={'arrowstyle': '-','color':'silver'},annotation_clip=False)
    
    idx_measures_nl = data.index[data.Week==dt.datetime.strptime('2020-01-26','%Y-%m-%d')] #30th January
    dataxy = (data.Week[idx_measures_nl],0)
    textxy = (data.Week[idx_measures_nl],132)
    P.annotate('WHO declares a global \n public-health emergency',dataxy,textxy,
               verticalalignment='center',horizontalalignment='center', color = 'dimgrey',
               arrowprops={'arrowstyle': '-','color':'silver'},annotation_clip=False)
    
    idx_strict_measures = data.index[data.Week==dt.datetime.strptime('2020-03-08','%Y-%m-%d')] #11th March
    dataxy = (data.Week[idx_strict_measures],0)
    textxy = (data.Week[idx_strict_measures],119)
    P.annotate('WHO declares the outbreak \n of a pandemic.',dataxy,textxy,
               verticalalignment='center',horizontalalignment='center', color = 'dimgrey',
               arrowprops={'arrowstyle': '-','color':'silver'},annotation_clip=False)
    if climate:
        idx = data.index[data.Week==dt.datetime.strptime('2019-09-22','%Y-%m-%d')] #23th September
        dataxy = (data.Week[idx],0)
        textxy = (data.Week[idx],143)
        P.annotate('Greta  Thunberg \n speech',dataxy,textxy,
                   verticalalignment='center',horizontalalignment='center', color = 'dimgrey',
                   arrowprops={'arrowstyle': '-','color':'silver'},annotation_clip=False)
 
    fig = P.gcf()
        
    return fig