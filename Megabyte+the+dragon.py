
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# In[3]:

start = "https://www.indeed.com/jobs?q=Data+Scientist&l=Denver%2C+CO"
# page nbr argument 1-10, 11-20, 


# In[4]:

test = requests.get(start, headers=headers)


# In[8]:

"state-of-the-art" in test.text


# In[11]:

soup = BeautifulSoup(test.text, "html.parser")
links = soup.find_all("a")


# In[57]:

soup


# In[40]:

some_links = []

for l in links:
    try:
        hyperlink = l.attrs.get('href')
        if "rc/clk" in hyperlink:
#             print(l.attrs.get('href'))
            some_links.append(l.attrs.get('href'))
    except:
        pass
# https://www.indeed.com/rc/clk?jk=f3ec178c7a762e5a&fccid=d512f2c02718adce&vjs=3


# In[41]:

some_links = ["https://www.indeed.com{}".format(x)
             for x in some_links
             ]


# In[43]:

some_links[:4]


# In[44]:

vocab = ["sql", "python", "javascript", 
         "nosql", "tableau", "c++", "tensorflow", "keras", "react"]


# In[45]:

def parse_single_listing(some_listing_url):
    data = requests.get(some_listing_url, headers=headers)
    return data.text


# In[46]:

listing = parse_single_listing(some_links[3])


# In[ ]:

Iknow = ['sql', 'python' , 'javascript'] #tiboe index


# In[55]:

from collections import defaultdict

matches = defaultdict(int)

for word in listing.split():
    if word.lower() in vocab:
        matches[word] += 1


# In[56]:

matches


# In[ ]:



