import streamlit as st
st.title{'Graphical Visualization'}

import pandas as pd

x = 1
y = 2

def adder(x, y):
    return x+y

st.write(f'{x}+{y}={adder(x,y)}')

df = pd.read_csv('./data.csv')
st.markdown('---')
df_val = df.groupby(by='name')
st.write(f'{df.iloc[1,1]}-{df.iloc[2,2]}')
st.table(df_val)

st.bar_chart(df_val)
st.line_chart(df_val)
st.area_chart(df_val)