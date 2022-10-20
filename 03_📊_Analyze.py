import streamlit as st
import pandas as pd
import numpy as np 
import re
from collections import Counter
cnt = Counter()
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
import nltk



st.set_page_config(
    page_title = 'Jobs Analysis Dashboard',
    page_icon = 'chart_with_upwards_trend',
    layout = 'wide'
)

st.markdown("## Overview")
df = pd.read_csv("D:\COLLEGE\YEAR V\SEM IX\MINOR PROJECT\proj\Data Analyst jobs in Kochi naukri.csv")


# kpi 1 

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown("**Number of Jobs**")
    number1 = df.shape[0] 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with kpi2:
    st.markdown("**Top Salary**")
    df["Salary"] = df["Salary"].apply(lambda text: (re.sub(',','', text)))
    df["Salary"] = df["Salary"].apply(lambda text: (re.sub('PA.','', text)))
    df["Salary"] = df["Salary"].apply(lambda text: (re.sub(' ','', text)))
    df = df[df.Salary != "Notdisclosed"]
    split_range = lambda sal_range : [[int(y) for y in x.split('-')] if len(x.split('-')) == 2 else [int(x.split('+')[0])] for x in sal_range]
    df["sal"] = split_range(df["Salary"])
    df["Average Salary"] = pd.Series([sum(ages)/len(ages) for ages in split_range(df["Salary"])])
    number2 = "{:,}".format(df['Average Salary'].max())
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with kpi3:
    st.markdown("**Top Skill**")
    #for text in df["Skills"]:
     #   for word in text.split(","):
      #      cnt[word] += 1'''
    number3 = "Data Analysis" 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

st.markdown("<hr/>",unsafe_allow_html=True)


st.markdown("## Analysis")

# kpi 1 

chart_1, chart_2 = st.columns(2)

with chart_1:
    st.markdown("Top Skills")
    #df['skill'] = df.apply(lambda row: nltk.word_tokenize(row['Skills']), axis=1)
    df["Skills"] = df["Skills"].str.split(",")
    result = ''.join(str(skill) for skill in df["Skills"])
    #print(result)
    #wordcloud = WordCloud().generate(' '.join(df['Skills']))
    wordcloud = WordCloud().generate(result)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    #number1 = 111 
    #st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number1}</h1>", unsafe_allow_html=True)

with chart_2:
    st.markdown("**Top Companies**")
    #number1 = 222
    df["Company"] = df["Company"].str.split(",")
    result_1 = ''.join(str(comp) for comp in df["Company"])
    wordcloud = WordCloud().generate(result_1)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    #st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number1}</h1>", unsafe_allow_html=True)




st.markdown("<hr/>",unsafe_allow_html=True)

st.markdown("## Chart Layout")

chart1, chart2 = st.columns(2)

with chart1:
    chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

with chart2:
    chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
    st.line_chart(chart_data)