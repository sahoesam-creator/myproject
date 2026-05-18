import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

def init_db():
    conn = sqlite3.connect('myproject.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            item1 INTEGER NOT NULL, 
            item2 INTEGER NOT NULL,  
            item3 INTEGER NOT NULL           
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

st.title('SQLite & Streamlit DB table creation examples')

with st.form("user_register_form"):
    name = st.text_input('Your Name? ', key='name')
    age = st.number_input('Your Age? ', min_value=1, max_value=120, key='age')

    if st.form_submit_button('add User!!'):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUE (?, ?)", (name, age))
        conn.commit()
        st.success(f'added {name} to the databases!!!')

st.subheader('Current User!!')
query = "SELECT * FROM users"
df = pd.read_sql_query(query, conn)
st.dataframe(df, use_container_width=True)

search_query = st.text_input('Search by Name')
if search_query:
    filtered_df = df[df['name'].str.contains(search_query, case=False)]
    st.write("Search results")
    st.markdown('---')
    st.dataframe(filtered_df)

st.title('SQLite & Streamlit DB table creation examples')

with st.form("survey system"):
    item1 = st.radio('Your Name? ', ['1','2','3','4'], index=1, key='item1')
    item2 = st.radio('Your Name? ', ['1','2','3','4'], index=1, key='item2')
    item3 = st.radio('Your Name? ', ['1','2','3','4'], index=1, key='item3')
    
    if st.form_submit_button('Add New Opinion'):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO survey (item1, item2, item3) VALUES (?, ?, ?)", (item1, item2, item3))
        conn.commit()
        st.success(f'Added new opinion to the databases!!!')

st.subheader('Survey status...')
query_s = "SELECT * FROM survey"
df_s = pd.read_sql_query(query_s, conn)
st.dataframe(df_s, use_container_width=True)

st.line_chart(df_s)