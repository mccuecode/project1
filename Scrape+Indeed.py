
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import nltk

def get_job_links_page(page):
    base_url = "https://www.indeed.com/jobs?"
    params = {'q': 'data scientist', # data analist, machine learning engineer, BI analyst
             'l': 'Denver, CO'}

    # start = "https://www.indeed.com/jobs?q=Data+Scientist&l=Denver%2C+CO"
    # use a fake header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    params['start'] = 10 * (page-1)

    page = requests.get(base_url, params=params, headers=headers)
    # test = requests.get(start, headers=headers)
    
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("a")
    
    # build a list of links
    some_links = []

    for l in links:
        try:
            hyperlink = l.attrs.get('href')
            if "/rc/clk?" in hyperlink:
                some_links.append(l.attrs.get('href'))
        except:
            pass
    
    job_links = ["https://www.indeed.com{}".format(x)
             for x in some_links
             ]
    
    return job_links


# In[7]:

# WORKING links = [get_job_links_page(x) for x in range(1, 20)]
# POSSIBLE title_links = [get_job_links_page(x, 'title_here') for x in range(1, 20)]

bi_analyst = [get_job_links_page(x, 'bi_analyst') for x in range(1, 20)]
tableau = [get_job_links_page(x, 'tableau') for x in range(1, 20)]

# Add all those lists together


# In[11]:

import itertools
merged = list(itertools.chain(*links))
len(merged)
merged[0]


# In[22]:

merged[0].split("?")[1:][0].split("jk=")[-1].split("&")[0]


# In[49]:

from urllib.parse import urlparse
from urllib.parse import parse_qs

def get_filename_from_url(some_url):
    parsed = parse_qs(some_url)
    fccid =  parsed.get('fccid')[0]
    other_id = parsed.get('https://www.indeed.com/rc/clk?jk')[0]
    return fccid+other_id+ ".html"


# In[50]:

get_filename_from_url(merged[0])


# In[53]:

len(set([get_filename_from_url(x) for x in merged]))


# In[54]:

def download_job_page(link):
    save_name = get_filename_from_url(link)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    test = requests.get(link, headers=headers)
    soup = BeautifulSoup(test.text, "html.parser")
    
    with open('jrj_{}'.format(save_name), 'w') as f:
        f.write(str(soup))
    #spans = soup.find_all('span')
    #spans_w_divs = [span.find_all('div') for span in spans if len(span.find_all('div')) > 0]
    #span = soup.find("span", id="job_summary")
    #return str(span)


# In[56]:

# Download the pages for all the links

for link in tqdm(merged):
    try:
        download_job_page(link)
    except Exception as e:
        print(str(e), link)
    finally:
        time.sleep(1)


# In[2]:

# Load the ref to the files
import glob

html = glob.glob('jeff_html/*.html')
len(html)


# In[3]:

html_divs = []

for html_file in html:
    with open(html_file, 'r') as f:
        _data = BeautifulSoup(f.read(), "html.parser")
        try:
            has_span_job_summary = _data.find("span", id="job_summary").get_text()
            html_divs.append(has_span_job_summary)
        except:
            print('hh')
        
len(html_divs)


# In[6]:

#pd.DataFrame(html_divs).to_csv('parsed_job_desc_jj.csv', header=False, index=False)

current_skill = 'python'
list_of_skills = skills.skill_name.tolist() # All skills we know of
list_of_skills = [x.replace("\xa0", " ").replace("\x92s", " ") for x in list_of_skills]
# https://stackoverflow.com/questions/10993612/python-removing-xa0-from-string


# In[ ]:




# In[7]:

jobs = pd.DataFrame(html_divs)
jobs.columns = ['desc']
jobs.head()


# In[35]:

import string
from collections import defaultdict

found = 0

for index, row in jobs.iterrows():
    job_desc = row.desc
    job_tokens = nltk.word_tokenize(job_desc)
    job_tokens = [word for word in job_tokens if len(word) >= 1]
    job_tokens = [word.lower().strip() for word 
                  in job_tokens if not word in string.punctuation ]
    # repeat and say if word not in stop_words_ist
    has_py = "sql" in job_tokens
    if has_py:
        found +=1
        #am I always matching python right? seems low occurrence to me...
        # find all other skills from list of tokens 
        # var name list_of_skills
        matches = defaultdict(int)
        
        for skill in list_of_skills:
            if skill in job_tokens:
                matches[skill] += 1


# In[39]:

print(found)
matches #10 - 100x more data
sorted(matches.items(), key=lambda x: x[1], reverse=True)


# In[99]:

#nltk.download('punkt')


# In[5]:

import pandas as pd

skills = pd.read_csv('skill_phrases-JBM.csv', encoding="ISO-8859-1")
skills.columns = ['skill_name']
skills['skill_name'] = skills.skill_name.map(lambda x: 
                                           x.lower().strip())
skills.head()


# In[3]:

# END JJ CODE


import csv
from nltk.tokenize import RegexpTokenizer

def initialize_highlighting(filename):
# Read a list of skill phrases from a file
    skill_phrases = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            skill_phrases.append(str(*row).strip())
    skill_phrases = set(skill_phrases)

    # Write this clean version back out
    with open('skill_phrases_out.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for skill_phrase in skill_phrases:
            csv_writer.writerow([skill_phrase])
        
    #separate each skill phrase into a list of its words
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9#+-]+')
    skill_phrase_wl = [tokenizer.tokenize(skill_phrase) for skill_phrase in skill_phrases]
    
    return skill_phrase_wl


# In[4]:

def tally_skill_mentions_in_job(t, skill_phrase_wl):
    
    skill_mentions_in_job = defaultdict(int)
    # tokenize the text of the description, without spans
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9#+-]+')
    tokens = tokenizer.tokenize(t)
    # create a dictionary of the words in the job description
    word_index = defaultdict(list)
    for i, k in enumerate(tokens):
        word_index[k].append(i)
    
    # search the word_index dictionary to find the fist word of each skill_phrase
    for skill_phrase in skill_phrase_wl:
        if word_index.get(skill_phrase[0]):
            for occurence in word_index.get(skill_phrase[0]):
                # Check to see if the whole phrase matches
                if all((skill_phrase[j] == tokens[j+occurence]) for j in range(len(skill_phrase))):
                    skill_mentions_in_job[tuple(skill_phrase)] += 1
    return skill_mentions_in_job        


# In[5]:

from collections import defaultdict
import pandas as pd
from IPython.core.display import HTML

# requires the global variable skill_phrase_wl
# maybe this should be a parameter rather than a global
def highlight_phrases_from_list(t):

    # tokenize the text of the description, with spans
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9#+-]+')
    span_generator = tokenizer.span_tokenize(t)
    spans = [span for span in span_generator]
    tokens = [t[span[0]:span[1]] for span in spans]
    
#     # create a dictionary of the words, with spans as the values
#     # and another dictionary with the same keys, with the word indexes as the values
    char_span = defaultdict(list)
    word_index = defaultdict(list)
    for i, (k, span) in enumerate(zip(tokens, spans)):
        char_span[k].append(span)
        word_index[k].append(i)
    # is this useful?
    df = pd.DataFrame({'Character Index Spans': pd.Series(char_span), 'Word Indexes': pd.Series(word_index)})

    highlight_spans = []   
    for skill_phrase in skill_phrase_wl:
        if word_index.get(skill_phrase[0]):
            for i, occurence in enumerate(word_index.get(skill_phrase[0])):
                if all((skill_phrase[j] == tokens[j+occurence]) for j in range(len(skill_phrase))):
                    highlight_span = (spans[occurence][0], spans[occurence + len(skill_phrase) - 1][1])
                    highlight_spans.append (highlight_span)

# # look up the words in our skill list in the dictionary.  List the findings as spans to be highlighted
#     for skill in single_word_skills:
#         highlight_spans += char_span[skill]

    # Sort the spans to be highlighted
    highlight_spans.sort()

    # Insert html tags to highlight the keywords
    html_start_tag = '<font color="red">'
    html_end_tag = '</font>'
    highlighted = ''
    cursor = 0
    for span in highlight_spans:
        if (span[0] > cursor): # go forwards only, not backwards 
            if (cursor>0):
                highlighted += html_end_tag
            highlighted += t[cursor:span[0]] +                             html_start_tag +                             t[span[0]:span[1]]
        elif (span[1] > cursor):
            highlighted += t[cursor:span[1]]
        cursor = span[1]
    highlighted += html_end_tag + t[cursor:]
    display(HTML(highlighted))    


# In[6]:

job_links = []
for page in range(1,25):
    job_links+=(get_job_links_page(page))


# In[7]:

from tqdm import tqdm

tallied_skill_mentions = []
skill_phrase_wl = initialize_highlighting('skill_phrases_purged-JBM.csv')
skill_dict = {tuple(skill_phrase): 0 for skill_phrase in skill_phrase_wl}
for link in tqdm(job_links):
    # highlight_phrases_from_list(get_job_summary(link))
    tallied_skill_mentions.append(tally_skill_mentions_in_job(get_job_summary(link), skill_dict))


# In[8]:

df = pd.DataFrame(tallied_skill_mentions, index = job_links).fillna(0).astype(int)


# In[9]:

skills_mentioned = df.columns.values
skill_phrases_mentioned = [' '.join(c) for c in df.columns.values]
df.columns = skill_phrases_mentioned


# In[10]:

df


# In[11]:

not_mentioned = skill_dict
for skill in skills_mentioned:
    del not_mentioned[skill]


# In[12]:

phrases_not_mentioned = [' '.join(s) for s in not_mentioned]
phrases_not_mentioned


# In[13]:

len (phrases_not_mentioned)


# In[14]:

df.sum(axis = 1).sort_values()


# In[15]:

skill_phrases = []
with open('skill_phrases_purged-JBM.csv', 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        skill_phrases.append(str(row[]).strip())


# In[17]:

skill_phrases=list(set(skill_phrases))


# In[33]:

import random
from itertools import compress
skill_percentage = random.random()
n_skill_phrases = len(skill_phrases)
n_my_skills = skill_percentage * n_skill_phrases
my_skills_bool = [(x < n_my_skills) for x in range(n_skill_phrases)]
random.shuffle(my_skills_bool)
my_skill_list = list(compress(skill_phrases,my_skills_bool))
my_skill_list


# In[ ]:



