#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import numpy as np
import os


# In[71]:


places_urls=[]
url = 'https://www.fis-ski.com/DB/cross-country/calendar-results.html?eventselection=&place=&sectorcode=CC&seasoncode=2020&categorycode=WC&disciplinecode=&gendercode=&racedate=&racecodex=&nationcode=&seasonmonth=X-2020&saveselection=-1&seasonselection='
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")
tableHeader = content.find('div',id='calendardata')
rows = tableHeader.find_all('a', class_='pr-1 g-lg-1 g-md-1 g-sm-2 hidden-xs justify-left')
for row in rows:
    places_urls.append(str(row.get('href')))
    print (str(row.get('href')))


# Sätter season till rätt säsong utifrån url

# In[125]:


tmp_url=places_urls[-1:]
season=tmp_url[0][-4:]


# In[72]:


races_urls=[]
for url in places_urls:
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    tableHeader = content.find('div',id='eventdetailscontent')
    rows = tableHeader.find_all('a', class_='px-1 g-lg-3 g-md-3 g-sm-4 g-xs-4 justify-left')
    for row in rows:
        races_urls.append(str(row.get('href')))
        print(str(row.get('href')))


# In[16]:


Result=pd.DataFrame()
#races_urls = ['https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=34331','https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=34385','https://www.fis-ski.com/DB/general/results.html?sectorcode=CC&raceid=34381']
for url in races_urls:
    labels=[]
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    event = content.find('div', class_='event-header__kind').getText()
    place = content.find('h1', class_ = re.compile('heading.*')).getText()
    date = content.find('span', class_='date__short').getText()
    result_type = content.find('div',class_ = 'event-header__subtitle').getText()
    print(event,place,date,result_type)
    tableHeader = content.find('div',{ "data-boundary" : "#events-info-results"})
    rows = tableHeader.find_all('div', class_ = re.compile('g-lg.*'))

    column_headers = [
    row.get_text() for row in rows
        ]

    data = content.find('div',id='events-info-results')
    data_rows = data.find_all('a', class_ = re.compile('table-row'))


    player_data_02 = []  # create an empty list to hold all the data

    for i in range(len(data_rows)):  # for each table row
            player_row = []  # create an empty list for each pick/player

            # for each table data element from each table row
            for row in data_rows[i].findAll('div', class_ = re.compile('g-lg.*')):
                # get the text content and append to the player_row
                player_row.append(row.getText())

            # then append each pick/player to the player_data matrix
            player_data_02.append(player_row)



    df = pd.DataFrame(player_data_02, columns=column_headers)

    df['Event'] = event
    df['Place'] = place
    df['Date'] = date
    df['Result Type'] = result_type
    df['Season'] = season

    frames = [Result, df]
    Result = pd.concat(frames,sort=False)

Result.info()


# In[19]:


# In[20]:


Result = Result.reset_index(drop=True)
Result['Nation']= Result['Nation'].str.replace('\n','')
Result['Athlete']= Result['Athlete'].str.replace('\n','')
Result['Athlete']= Result['Athlete'].str.strip()

columns=['Name','Tot. Time','(Rk.)','FIS points Time','Unnamed: 0']
Result.drop(columns, inplace=True, axis=1)

# In[21]:

if os.path.isfile('extract/raw-data.csv'):
    os.remove('extract/raw-data.csv')
Result.to_csv('extract/raw-data.csv',encoding='utf-8')



# In[ ]:
