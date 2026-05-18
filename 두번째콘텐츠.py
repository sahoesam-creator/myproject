import streamlit as st
st. subheader('두번째 콘텐츠')
import pandas as pd
df_score = pd.read_csv('./score.csv', encoding='cp949')
st.write(df_score)
st.bar_chart(df_score.groupby(by='이름').sum())
df_score['총점'] = df_score.loc[:,'국어'] + df_score.loc[:,'영어'] + df_score.loc[:,'수학']
# 총점 컬럼 추가
st.table(df_score)