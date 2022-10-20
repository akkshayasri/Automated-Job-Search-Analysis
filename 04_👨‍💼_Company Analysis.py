import streamlit as st
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


import warnings 
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import joblib

from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
import spacy
import gensim
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import re
from os import path
from PIL import Image
import plotly
from sklearn.feature_extraction.text import CountVectorizer
st.set_page_config(
    page_title = 'Company Analysis Dashboard',
    page_icon = 'chart_with_upwards_trend',
    layout = 'wide'
)

company = st.selectbox('Select the company',('Honeywell', 'IBM', 'Microsoft', 'Oracle'))

if company == "Honeywell":
    df = pd.read_csv('D:\COLLEGE\YEAR V\SEM IX\MINOR PROJECT\proj\pages\company1_review.csv', index_col=[0], parse_dates=['Comment Datetime']) 
elif company == "IBM":
    df = pd.read_csv('D:\COLLEGE\YEAR V\SEM IX\MINOR PROJECT\proj\pages\IBM.csv', index_col=[0], parse_dates=['Comment Datetime'])
elif company == "Microsoft":
    df = pd.read_csv('D:\COLLEGE\YEAR V\SEM IX\MINOR PROJECT\proj\pages\Microsoft.csv', index_col=[0], parse_dates=['Comment Datetime'])
else:
    df = pd.read_csv('D:\COLLEGE\YEAR V\SEM IX\MINOR PROJECT\proj\pages\Oracle.csv', index_col=[0], parse_dates=['Comment Datetime'])
    
    
df.drop_duplicates(inplace = True)
rating_columns = df.select_dtypes(include = ['float64'])
string_columns = df.select_dtypes(exclude = ['float64'])
df_column_sorted = pd.concat([string_columns, rating_columns], axis = 1)


def extract_cat_data(row):
    
    # 1. extract current/former employee flags from'Author Years'
    if not pd.isna(row['Author Years']):
        if "have been working" in row['Author Years']:
            row['Current Employee'] = 1
        elif "I worked at" in row['Author Years']:
            row['Current Employee'] = 0
        else:
            row['Current Employee'] = Np.NaN          
    
    # 2. extract tenure from 'Author Years'
    string_to_number = row["Author Years"].replace("a year", "1 year")  # replace 'a year' with '1 year'
    tenure = re.findall(r'\d+', string_to_number)                       # find the digit in the string
    
    if tenure: 
        row['Tenure'] = int(tenure[0])                 # use the number in the list
        if 'more than' in row["Author Years"]:         
            row['Tenure'] += 0.5                       # add 0.5 year if there is 'more than'
        elif 'less than' in row["Author Years"]:       
            row['Tenure'] -=0.5                        # minus 0.5 year if there is 'less than'
    else:
        row['Tenure'] = np.NaN                         # if no tenure is specified, set to NaN
    
    
     # 3. extract full-time/part-time flags from 'Author Years'
    if 'full-time' in string_to_number or 'full time' in string_to_number:
        row['Full-time'] = 1
    elif 'part-time' in string_to_number or 'part time' in string_to_number:
        row['Full-time'] = 0
    else:
        row['Full-time'] = np.NaN                       # if not specified, set it NaN
 
    
    # 4. extract 'Recommended','Positive Outlook','Approves of CEO' from column'Recommendation' 
    row['Recommended'] = 0
    row['Positive Outlook'] = 0
    row['Approves of CEO'] = 0
    
    if not pd.isna(row['Recommendation']):
        if 'Recommends' in row['Recommendation']:
            row['Recommended'] = 1
        elif "Doesn't Recommend" in row['Recommendation']:
            row['Recommended'] = -1
        
        elif 'Positive Outlook' in row['Recommendation']:
            row['Positive Outlook'] = 1
        elif 'Negative Outlook' in row['Recommendation']:   
            row['Positive Outlook'] = -1
        elif 'Neutral Outlook' in row['Recommendation']: 
            row['Positive Outlook'] = 0
            
        elif 'Approves of CEO' in row['Recommendation']:
            row['Approves of CEO'] = 1
        elif 'Disapproves of CEO' in row['Recommendation']:
            row['Approves of CEO'] = -1
        elif 'No opinion of CEO' in row['Recommendation']:   
            row['Approves of CEO'] = 0

    return row

df_cat_extracted = df.apply(extract_cat_data, axis=1)

def extract_loc_job(row):
    
    # 1. extract location
    if not pd.isna(row['Author Location']):
        if re.search(r'[A-Z]{2}$',row['Author Location']): 
            # extract the last 2 captical letters as state
            row['State'] = re.search(r'[A-Z]{2}$',row['Author Location'])[0]
        else:
            row['State'] = np.NaN      
    else:
            row['State'] = np.NaN                               
    
    # 2. extract job title
    if pd.notnull(row['Author Title']) and row['Author Title']: 
        if '-'in row['Author Title']:  # author title usually starts like this: "Current Employee - Analyst" 
            row['Job Title'] = row['Author Title'].split("-")[1]  # get the 2nd element after the split 
        else:
            row['Job Title'] = row['Author Title']
    else:
         row['Job Title'] = 'Unknown Title'
    # remove "senior" and "principal" to get fewer job categories 
    # remove the beginning & end spaces
    row['Job Title'] = row['Job Title'].replace('Senior',"").replace('Principal',"").strip() 
    
    return row       

df_loc_job_filled = df_cat_extracted.apply(extract_loc_job,axis=1) 

df_cleaned = df_loc_job_filled.drop(columns = ['Recommendation', 'Author Title', 'Author Years', 'Author Location'])

df_cleaned = df_cleaned[['Comment Datetime', 'State', 'Job Title','Tenure','Current Employee','Full-time',
                          'Summary','Pro','Con','Recommended', 'Positive Outlook','Approves of CEO',
                          'Overall Rating','Career Opportunities','Compensation and Benefits',
                          'Work/Life Balance','Senior Management','Culture & Values']]
df_cleaned.set_index('Comment Datetime',inplace=True)
df_cleaned = df_cleaned.sort_index()



st.markdown("## All Ratings")

# plot all ratings using boxplots

column_list = ['Overall Rating','Career Opportunities','Compensation and Benefits',
            'Work/Life Balance','Senior Management','Culture & Values']

figure, ax = plt.subplots(1,6,figsize=(12,5))  

for column, curr_ax in zip(column_list, ax.ravel()):  # use ax.ravel() to flatten ax(2 by 3) in order to zip
    curr_ax.boxplot(df_cleaned[column].dropna())      # drop those NaN values    
    curr_ax.set_title(f'{column}')

plt.tight_layout()
st.pyplot(figure) 


st.markdown("## Overall recommendations")

rec_count = df_cleaned['Recommended'].value_counts(normalize=True)

fig, ax = plt.subplots()
ax.bar(['Recommend', 'Unknown','Not Recommend'], rec_count, color=['tab:olive','tab:orange','tab:red'])
ax.set_title('Recommend Or Not?', fontsize=20)
ax.set_ylabel('Frequency')
# plt.savefig('recommend_or_not.png')

st.pyplot(fig)

# plot sub categories average ratings

column_list = ['Overall Rating','Career Opportunities','Compensation and Benefits',
               'Work/Life Balance','Senior Management','Culture & Values']

sub_ratings = df_cleaned[column_list].mean()
colors1=['tab:cyan','tab:orange','tab:red','tab:pink','tab:purple','tab:olive']

figure_sc, ax = plt.subplots(figsize=(12,5))  
ax.bar(sub_ratings.index, sub_ratings, color=colors1)

ax.set_title ('Sub-categories Average Ratings', fontsize=20)
ax.set_ylabel ('Average Ratings')
ax.set_xticklabels(sub_ratings.index,rotation=45)
# figure.savefig('subcategory_rating.png', bbox_inches = 'tight')
st.pyplot(figure_sc)
#plt.show() 

# plot the 10 states with top ratings 

top_10 = df_cleaned.groupby('State')['Overall Rating'].mean().nlargest(10)
colors2 = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
           'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

fig,ax = plt.subplots(figsize=(10,5))
ax.bar(top_10.index,top_10, color=colors2)
ax.set_title('Top 10 States with Highest Ratings', fontsize=20)
ax.set_xlabel('States')
ax.set_ylabel('Overall rating')
# plt.savefig('top10_states_high_rate.png')

plt.show()

# plot the 5 states with lowest ratings 

lowest_5 = df_cleaned.groupby('State')['Overall Rating'].mean().nsmallest(5)
colors3 = ['tab:blue','tab:pink','tab:cyan','tab:orange','tab:purple']

fig,ax = plt.subplots(figsize=(10,5))
ax.bar(lowest_5.index,lowest_5, color=colors3)
ax.set_title('Top 5 States with Lowest Ratings',fontsize=20)
ax.set_xlabel('States')
ax.set_ylabel('Overall rating')
# plt.savefig('top5_states_low_rate.png')

plt.show()

# plot overall rating by full-time/part-time employee

rate_by_fte = df_cleaned.groupby('Full-time')['Overall Rating'].mean()

fig_fte, ax = plt.subplots()
ax.bar(['Part_Time', 'Full_Time'], rate_by_fte,color=['tab:pink','tab:cyan'])
ax.set_title('Overall Ratings by Full/Part-time Employee', fontsize=20)
ax.set_ylabel('Overall rating')
# plt.savefig('rating_by_fulltime_parttime.png')

st.pyplot(fig_fte)

# plot overall rating by current/former employee

rate_by_emp_type = df_cleaned.groupby('Current Employee')['Overall Rating'].mean()

fig_emptype, ax = plt.subplots()
ax.bar(['Former Employee', 'Current Employee'], rate_by_emp_type,color=['tab:pink','tab:cyan'])
ax.set_title('Overall Ratings by Current/Former Employee', fontsize=20)
ax.set_ylabel('Overall rating')
# plt.savefig('rating_by_current_former.png')

st.pyplot(fig_emptype)
# plot the most frenquest reviewer job titles

top_20_job = df_cleaned['Job Title'].value_counts().nlargest(20)

top_20 = plt.figure(figsize=(12,7))
sns.countplot(y='Job Title',data=df_cleaned, order=top_20_job.index)
sns.set_context('talk')
plt.title('Most Frequest Employee Job Titles', fontsize=20)
# figure.savefig('most_freq_job_title.png',bbox_inches = 'tight')

st.pyplot(top_20)

top_20job_review = df_cleaned.loc[df_cleaned['Job Title'].isin(top_20_job.index), ['Job Title','Overall Rating']]
top_20job_mean_review = top_20job_review.groupby('Job Title')['Overall Rating'].mean().sort_values(ascending = False)

# plot the reviewers in the top 20 job families' overall rating

job_family = plt.figure(figsize=(12,7))
sns.barplot(y=top_20job_mean_review.index, x=top_20job_mean_review, hue_order=top_20job_mean_review)
sns.set_context('talk')
plt.title('Overall Rating by Job Family', fontsize=20)
# figure.savefig('rating_by_job_family.png',bbox_inches = 'tight')

st.pyplot(job_family)

df_cleaned.to_csv('df_cleaned1.csv')
df_cleaned = pd.read_csv('D:\COLLEGE\YEAR V\SEM IX\MINOR PROJECT\proj\pages\df_cleaned.csv')
def get_common_words(column,n):
    text = df_cleaned[column].to_string()
    tokens = [w for w in word_tokenize(text.lower()) if w.isalpha()]
    no_stops = [t for t in tokens if t not in stopwords.words('english')]
    top_n = Counter(no_stops).most_common(n)
    
    return top_n
top_20_summary = get_common_words('Summary',20)
top_20_pro = get_common_words('Pro',20)
top_20_con = get_common_words('Con',20)
stop_words = set(stopwords.words("english"))
cus_words = ["work", "place", "anonymous","anonymou","they","there"]
stop_words = stop_words.union(cus_words)
def plot_wordcloud(column):
    text = df_cleaned[column].to_string().lower()
    wordcloud = WordCloud(background_color='white',
                          stopwords = stop_words,
                          max_words=100,
                          max_font_size=50, 
                          random_state=42).generate(text)

    wc = plt.figure(figsize=(10,10))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.title(column, fontsize=20)
    st.pyplot(wc)
