#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

#pieces commented out will all work once cltk is properly installed
#import cltk
#from cltk.stops import grc
import ast
import streamlit as st

st.title('This is a little app to investigate the speakers\' language in Euripidean plays.')

tragedy = open('toy_dataset_tragedy.csv', 'r')

tragedy_df = pd.read_csv(tragedy)

greek_stoplist = []
#greek_stoplist = cltk.stops.grc.STOPS
# it turned out that some of the lemmata are not recognised as stopwords, even though they look identical; i had no time to figure out why (encoding?) so i added them manually
# see the illustration below (uncomment to run)
# len(greek_stoplist)
# greek_stoplist[13]
# 'δέ' in greek_stoplist

greek_stoplist.extend(['δέ', 'δʼ', 'καί', 'σύ', 'ἐγώ', 'δέ', 'γάρ', 'τίς', 'εἰμί', 'τʼ', 'σός', 'ἔχω', 'μή', 'λέγω', 'ἐμός', 'πρός', 'μέν', 'παῖς', 'ἀλλʼ', 'πατήρ', 'θεός', 'γʼ', 'τὰν', 'θʼ'])
st.header("Select speakers and plays for comparison")

def find_favourite_words(play, speaker, df=tragedy_df):
    working_df = df[(df['play']==play) & (df['speaker'] == speaker)]
    lemmata_as_list = working_df['lemmatized_text'].apply(lambda x: ast.literal_eval(x))
    working_df['lemmata_as_list'] = lemmata_as_list
    # making a list of all the tokens altogether
    lemmata_list_full = [item for sublist in working_df['lemmata_as_list'].to_list() for item in sublist]
    lemmata_list = [lemma for lemma in lemmata_list_full if lemma not in greek_stoplist]
    #print(len(lemmata_list_full))
    #print(len(lemmata_list))
    lemmata_dict={}
    for lemma in lemmata_list:
        lemmata_dict[lemma] = lemmata_list.count(lemma)
    lemmata_count = pd.DataFrame.from_dict(lemmata_dict, orient='index', columns=['count']).reset_index(level=0)
    lemmata_count['frequency'] = lemmata_count['count'] / len(lemmata_count.index)
    return(lemmata_count.sort_values(by=['count'], ascending=False))

col1, col2 = st.columns(2)


with col1:
    play1 = st.radio('Play', tragedy_df['play'].unique(), key='play1')
    speaker1 = st.selectbox('Speaker', tragedy_df[tragedy_df['play']==play1]['speaker'].unique(), key='speaker1')
    st.write('Here are top 20 words used by ' + speaker1)
    st.table(find_favourite_words(play1, speaker1)[:20])

with col2:
    play2 = st.radio('Play', tragedy_df['play'].unique(), key='play2')
    speaker2 = st.selectbox('Speaker', tragedy_df[tragedy_df['play']==play2]['speaker'].unique(), key='speaker2')
    st.write('Here are top 20 words used by ' + speaker2)
    st.table(find_favourite_words(play2, speaker2)[:20])

st.write('built by Daria Kondakova during the Bologna ENCODE workshop of JAN23')
