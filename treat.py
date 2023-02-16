import numpy as np
import pandas as pd
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

#Import the dataset
df = pd.read_csv('msgs.csv')
def Qui(name,df):
    if name =='C':
        df=df.loc[df['Qui']=='C']
        hist1 = 'indianred'
    else:
        df=df.loc[df['Qui']=='I']
        hist1 = 'dodgerblue'
    return df, hist1

#Title
st.set_page_config(page_title = 'Message Exchange', page_icon=":warning:",layout="wide")

#---------ZERO SECTION: INTRO
st.title(':arrow_down_small: Conversation Data')
st.header('> Person: ')
choice = st.selectbox("Choose the person",["C","I"])

df,hist1 = Qui(choice,df)

#---------FIRST SECTION: INPUT
st.header('> About time for response: ')


#hist, bin_edges = np.histogram(pd.to_datetime(df['Hrs (1eme)']),bins=n_bins)

df['Date'] = pd.to_datetime(df['Jour'].astype(str)+'-'+df['Mois'].astype(str)+'-'+df['An'].astype(str)+' '+df['Hrs (1eme)'])

choice2 = st.selectbox("Sort by",["Hour","Weekday","Monthday"])

def sorter(choice,df):
    if choice =='Hour':
        ph = df.groupby(df['Hrs (1eme)'].astype("datetime64").dt.hour).count()['Hrs (1eme)']
    if choice =='Weekday':
        ph = df['Date'].groupby(df['Date'].dt.weekday).count()
        ph.index=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    if choice =='Monthday':
        ph = df['Jour'].groupby(df['Jour']).count()
    return ph

ph = sorter(choice2,df)
#fig = px.histogram(ph, nbins=n_bins, opacity=0.8, color_discrete_sequence=[hist1])
fig = px.bar(ph,opacity=0.8, color_discrete_sequence=[hist1])
st.plotly_chart(fig, use_container_width=True)

#------------SECOND SECTION
# First plot, the month frequency
st.header('> Volume by month: ')


P_chg = df.loc[df['Platform']=='Bumble'].iloc[-1]
st.write('Change from platform happened between '+P_chg['Jour'].astype(str) + ' of ' + P_chg['Mois'].astype(str) + ' of ' + P_chg['An'].astype(str)  )

choice3 = st.selectbox("Sort by",["Hour","Week-day","Monthday"])

def sorter2(choice,df):
    if choice =='Hour':
        ph2 = df['Count'].groupby(df['Hrs (1eme)'].astype("datetime64").dt.hour).sum()
    if choice =='Week-day':
        ph2 = df['Count'].groupby(df['Date'].dt.weekday).sum()
        ph2.index=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    if choice =='Monthday':
        ph2 = df['Count'].groupby(df['Jour']).sum()
    return ph2

ph2 = sorter2(choice3,df)
fig = px.bar(ph2, opacity=0.8, color_discrete_sequence=[hist1])
st.plotly_chart(fig, use_container_width=True)

#----------------Third Section
#To be answered: where in the month do the responses come most often?



