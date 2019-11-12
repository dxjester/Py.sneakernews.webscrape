# -*- coding: utf-8 -*-
"""
FILENAME: sneakernews_scrape.py
PROJECT: Sneaker Website Analysis
DATE CREATED: 15-Aug-19
DATE UPDATED: 9-NOV-19
VERSION: 1.0
"""


#----------------------------------- START -----------------------------------#
#-------------------------- PHASE 1: Import Libraries ------------------------#
#-----------------------------------------------------------------------------#

# 1.1 Module Import ----------------------------------------------------------#
# import the required modules
import requests
import time
import pandas as pd
import datetime
import pprint
from datetime import date 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
# from collections import Counter
# from string import punctuation

# 1.1 Class Declaration ------------------------------------------------------#
class sneaker_site:
    
    # initialize the class
    def __init__ (self, name, url): # provide the name of the website and the url
        '''
        DESCRIPTION: initialize class with default class arguments
        '''
        self.website_name = name
        self.url = url
        self.site_text = ''
        self.lines = ''
        self.site_df = pd.DataFrame(columns = ['website','dtg', 'date','year', 'month', 'day', 'category_name', 'item', 'count'])
        self.site_df['website'] = self.website_name # assign the website name to the entire class dataframe
        
        self.soup = ''
        self.hyperlink_list = ''
        self.paragraph_list = ''
        self.bold_list = ''
        
        self.nike_site_count = 0
        self.adidas_site_count = 0
        self.reebok_site_count = 0
        self.new_balance_site_count = 0
        self.puma_site_count = 0
        self.vans_site_count = 0

        # default Nike list
        self.nike_master = ['Nike', 'Jordan', 'Converse'] 
        # ['Nike', 'Air', 'Max', 'Jordan', 'Zoom', 'React', 'Shox', 'ACG', 'Max Plus', 'Joyride', 'Tinker', 'Force', 'Westbrook', 'Kyrie','Lebron', 'Durant', 'SB', 'Air Max 90', 'Air Max 97', 'Air Max 1', 'Kyrie', 'Air Max 270', 'Travis Scott' ]

        # default Adidas list     
        self.adidas_master = ['Adidas', 'Reebok', 'ADIDAS', 'Yeezy', 'Kanye', 'adidas', 'kanye', 'yeezy']
        # ['Adidas', 'ADIDAS', 'adidas', 'Yeezy', 'Kanye', 'Ultraboost', 'EQT', 'NMD', 'Ultra Boost', 'FYW', 'Harden']
        
        # default New Balance list
        self.new_balance_master = ['New Balance', 'NB', 'new balance']
        # ['New Balance', 'NB', 'Balance', '997', '801']
        
        # default Puma LIst
        self.puma_master = ['Puma', 'puma']
        #['Puma', 'Cell Venom', 'Thunder Spectre', 'Clyde Court']

        # default Vans list
        self.vans_master = ['Vans','vans']
        
        # concatenante the individual sneaker lists into one master list
        self.sneaker_list = self.nike_master + self.adidas_master + self.new_balance_master + self.puma_master + self.vans_master
        self.length = len(self.sneaker_list)         
        print("{} website object created".format(self.website_name))
    
    # class function to calculate the counts of list 
    def site_calculate(self):
        '''
        DESCRIPTION: pull the raw data from the website and append in dataframe
        '''
        
        start_time = time.time()
        print("\nRetrieving {} text and data ...".format(self.website_name))
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, "html.parser")
        
        print("\nConsolidating all hyperlinks and paragraphs for", self.website_name)        
        self.hyperlink_list = self.soup.findAll('a')
        self.paragraph_list = self.soup.findAll('p')
        self.bold_list = self.soup.findAll('b')
        
        self.site_text = self.soup.get_text()
        print("\nConverting ", self.website_name, " to text file ... ")
        
        self.lines = [self.site_text.lower() for line in self.site_text]
        print("\nCalculating individual counts: " )
        
        index_num = 0

        for item in self.sneaker_list:
            website = self.website_name
            name = item + ': '
            count = self.site_text.count(item)
            today = date.today()
            dtg = datetime.datetime.now()
            year = dtg.year
            month = dtg.month
            day_num = dtg.day

            category = ''
            
            if count > 0:
                if item in self.nike_master:
                    self.nike_site_count += count
                    category = 'Nike'
                elif item in self.adidas_master:
                    self.adidas_site_count += count
                    category = 'Adidas'
                elif item in self.new_balance_master:
                    self.new_balance_site_count += count
                    category = 'New Balance'
                elif item in self.puma_master:
                    self.puma_site_count += count
                    category = 'Puma'
                elif item in self.vans_master:
                    self.vans_site_count += count
                    category = 'Vans'
                else: 
                    0
            else: 
                if item in self.nike_master:
                    category = 'Nike'
                elif item in self.adidas_master:
                    category = 'Adidas'
                elif item in self.new_balance_master:
                    category = 'New Balance'
                elif item in self.puma_master:
                    category = 'Puma'
                elif item in self.vans_master:
                    category = 'Vans'
                else: 
                    0                
            self.site_df.loc[index_num] = [website, dtg, today, year, month, day_num, category, item, count]        
            print(name, count)
            index_num += 1
        
        elapsed_time = time.time() - start_time 
        print("\n{} data ingest completed, total elapsed time: {} seconds\n".format(self.website_name, round(elapsed_time,2)))
        
    def display_info(self):
        '''
        DESCRIPTION: display object information
        '''
        print("\nCalculating total counts by shoe company...")
        print("Total Nike mentions: ", self.nike_site_count)
        print("Total Adidas mentions: ", self.adidas_site_count)
        print("Total New Balance mentions: ", self.new_balance_site_count)
        print("Total Puma mentions: ", self.puma_site_count)      
        print("Total Vans mentions: ", self.vans_site_count)      
        # print(self.site_df)      
        
    def return_df(self):
        '''
        DESCRIPTION: return class dataframe 
        '''
        return self.site_df
        
    def display_links(self):
        '''
        DESCRIPTION: display hyperlinks for the object
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.hyperlink_list)
    
    def display_paragraphs(self):
        '''
        DESCRIPTION: display paragraphs for the object
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.paragraph_list)
        
    def display_bold(self):
        '''
        DESCRIPTION: display bold tags for the object
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.bold_list)  
        
        
#----------------------------------- START -----------------------------------#
#-------------------------- PHASE 2: Execution area --------------------------#
#-----------------------------------------------------------------------------#

# 2.A: SNEAKERNEWS.com ingest and analysis -----------------------------------#
sneaker_news = sneaker_site('sneakernews.com', 'https://sneakernews.com/')
sneaker_news.site_calculate()
sneaker_news.display_info()
#sneaker_news.display_links()
#sneaker_news.display_paragraphs()
#sneaker_news.display_bold()

# retrieve master sneakernews.com dataframe
sneaker_news_df = sneaker_news.return_df()
sneaker_news_df.head(10)


# 2.A.1: sneakernews.com plotting 

# slice dataframe with 'category_name' and 'count' columns
sneaker_news_sliced = sneaker_news_df[['category_name','count']]
temp = sneaker_news_sliced.groupby(['category_name']).sum()

# sort the two column dataframe by descending on count
temp = temp.sort_values('count', ascending = False)
sneaker_news_bar = temp.reset_index()
sneaker_news_bar.head(10)

# begin bar chart plotting
x_val = sneaker_news_bar['category_name']
y_val = sneaker_news_bar['count']

cr = ['red', 'grey', 'blue', 'green', 'orange']
sneaker_news_fig = plt.figure()
sneaker_news_ax = sneaker_news_fig.add_subplot(111)
sneaker_news_ax.bar(x_val, y_val, align='center', color = cr)
sneaker_news_ax.title.set_text('Sneakernews.com Category Chart')
plt.show()
# end bar chart plot


# 2.B: SOLECOLLECTOR.com ingest and analysis ---------------------------------#
sole_collector = sneaker_site('Solecollector.com', 'https://solecollector.com/')
sole_collector.site_calculate()
sole_collector.display_info()
#sole_collector.display_links()
#sole_collector.display_paragraphs()
#sole_collector.display_bold()

# retrieve master sneakernews.com dataframe
sole_collector_df = sole_collector.return_df()
sole_collector_df.head(10)


# 2.B.1: sneakernews.com plotting 

# slice dataframe with 'category_name' and 'count' columns
sole_collector_sliced = sole_collector_df[['category_name','count']]
temp = sole_collector_sliced.groupby(['category_name']).sum()

# sort the two column dataframe by descending on count
temp = temp.sort_values('count', ascending = False)
sole_collector_bar = temp.reset_index()
sole_collector_bar.head(10)

# begin bar chart plotting
x_val = sole_collector_bar['category_name']
y_val = sole_collector_bar['count']

cr = ['red', 'grey', 'blue', 'green', 'orange']
sole_collector_fig = plt.figure()
sole_collector_ax = sole_collector_fig.add_subplot(111)
sole_collector_ax.bar(x_val, y_val, align='center', color = cr)
sole_collector_ax.title.set_text('Solecollector.com Category Chart')
plt.show()
# end bar chart plot


# 2.C: HYPEBEAST.com ingest and analysis -------------------------------------#
hypebeast = sneaker_site('hypebeast.com', 'https://hypebeast.com/')
hypebeast.site_calculate()
hypebeast.display_info()
#hypebeast.display_links()
#hypebeast.display_paragraphs()
#hypebeast.display_bold()
