import streamlit as st
st.title('my first project!!!!') 
c1, c2 = st.columns((4,1))
with c1:
  with st.expander('Contents....'):
        st.subheader('Contents..')
with c2:
    with st.expander('Tips...'):
        st.info('Tips...')
