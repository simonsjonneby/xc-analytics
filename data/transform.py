#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import numpy as np
import csv
import os


# In[12]:


Result = pd.read_csv('extract/raw-data.csv')
columns =['Unnamed: 0']
Result.drop(columns, inplace=True, axis=1)



# In[13]:


Result.replace(r'^\s*$', np.nan, regex=True, inplace=True)
Result['Rank']=Result['Rank'].fillna(method='ffill')
Result.info()
Result


# In[14]:


Result['Rank'] = Result['Rank'].astype('int')
Result.info()


# In[15]:


def technique(Event):
    if "C/F" in Event:
        return "Skiathlon"
    elif "C" in Event:
        return 'Classic'
    elif "F" in Event:
        return 'Free'
    return 'Team'

def gender(Event):
    if "Women" in Event:
        return "Women"
    return "Men"

def team(Event):
    if "Team" in Event or "Rel" in Event:
        return "Team"
    return "Individual"

def sprintdistance(Event):
    if "SP" in Event or "sprint" in Event:
        return "Sprint"
    if "Overall" in Event:
        return "Overall"
    return "Distance"

def distance(Event):
    if "SP" in Event or "sprint" in Event:
        return "Sprint"
    elif "10" in Event:
        return "10"
    elif "15" in Event:
        return "15"
    elif "7.5/7.5" in Event:
        return "7.5/7.5"
    elif "15/15" in Event:
        return "15/15"
    elif "4x" in Event:
        return "Relay"
    elif "30" in Event:
        return "30"
    elif "50" in Event:
        return "50"
    elif "Overall" in Event:
        return "Overall"
    return "Other"

def points(ResultType):
    if "Overall" in ResultType:
        return 0
    elif "World Cup" in ResultType:
        return 1
    return 0


Result['Technique']=Result.apply(lambda x: technique(x['Event']),axis=1)
Result['Gender']=Result.apply(lambda x: gender(x['Event']),axis=1)
Result['Event individual/team']=Result.apply(lambda x: team(x['Event']),axis=1)
Result['Event sprint/distance']=Result.apply(lambda x: sprintdistance(x['Event']),axis=1)
Result['Distance']=Result.apply(lambda x: distance(x['Event']),axis=1)
Result['Points']=Result.apply(lambda x: points(x['Result Type']+x['Event']),axis=1)
Result
#Result.loc[(Result['FIS code']=='3185705') & (Result['Rank']<=3)]


# In[24]:


athletes=Result[['FIS code','Athlete','Year','Nation']]
athletes=athletes.drop_duplicates()
athletes=athletes.dropna()
athletes.loc[athletes['FIS code']==3295157]


# In[17]:


columns=['Athlete','Year','Nation',]
Result.drop(columns, inplace=True, axis=1)
Result


# Left joinar på Wins på Athlete tabellen.
#
# Räknar endast när Rank=1 och Points=1 vilket betyder att det inte är ett kval eller overall slutresultat.

# In[27]:


KPI = 'Podiums'
GroupBy = 'Points'
Definition = (Result['Rank'] <= 3) & (Result['Points']==1)

if KPI in athletes:
    athletes.drop(KPI, inplace=True, axis=1)

tmp_kpi=Result.loc[Definition]
tmp_kpi=tmp_kpi.groupby('FIS code')[GroupBy].value_counts()

athletes = pd.merge(athletes, tmp_kpi,how='left', on='FIS code')
athletes.rename(columns={GroupBy:KPI}, inplace=True)
athletes[KPI] = athletes[KPI].fillna(0)

athletes


# In[28]:


KPI = 'Wins'
GroupBy = 'Points'
Definition = (Result['Rank'] == 1) & (Result['Points']==1)

if KPI in athletes:
    athletes.drop(KPI, inplace=True, axis=1)

tmp_kpi=Result.loc[Definition]
tmp_kpi=tmp_kpi.groupby('FIS code')[GroupBy].value_counts()

athletes = pd.merge(athletes, tmp_kpi,how='left', on='FIS code')
athletes.rename(columns={GroupBy:KPI}, inplace=True)
athletes[KPI] = athletes[KPI].fillna(0)

athletes


# In[31]:


KPI = 'Top 10'
GroupBy = 'Points'
Definition = (Result['Rank'] <= 10) & (Result['Points']==1)

if KPI in athletes:
    athletes.drop(KPI, inplace=True, axis=1)

tmp_kpi=Result.loc[Definition]
tmp_kpi=tmp_kpi.groupby('FIS code')[GroupBy].value_counts()

athletes = pd.merge(athletes, tmp_kpi,how='left', on='FIS code')
athletes.rename(columns={GroupBy:KPI}, inplace=True)
athletes[KPI] = athletes[KPI].fillna(0)

athletes


# In[32]:


athletes.info()
Result.info()


# In[33]:



# df['Rank']=df['Rank'].astype('int')
# df['Bib']=df['Bib'].astype('int')
# df['FIS code']=df['FIS code'].astype('int')
# df['FIS Points']=df['FIS Points'].astype('float')
# df['Year']=df['Year'].astype('int')


if os.path.isfile('transform/results.csv'):
    os.remove('transform/results.csv')
Result.to_csv('transform/results.csv',encoding='utf-8',header=False)
if os.path.isfile('transform/athletes.csv'):
    os.remove('transform/athletes.csv')
athletes.to_csv('transform/athletes.csv',encoding='utf-8',header=False)



# In[ ]:
