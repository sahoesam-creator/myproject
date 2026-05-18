import streamlit as st
import base64
import urllib.parse
st.title('This is my first webapp!!')
txt_data = '''
'''
c1, c2 = st.columns((4, 1))
with c1:
    with open("인재원AI교재.pdf", "rb") as f:
        pdf_bytes = f.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'''
        <iframe 
        src="data:application/pdf;base64,{base64_pdf}" 
        width="100%" 
        height="430" 
        type="application/pdf">
        </iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
        st.markdown(txt_data)
with c2:
    with st.expander('Tips..'):
        imglink = 'https://search.pstatic.net/sunny/?src=https%3A%2F%2Fplay-lh.googleusercontent.com%2FfKP9h8bi96PuFc853Ar0lZHkAqZsZ2JKM4VHZWTGCeo0xbjpZXVA5tmboDDVZ53DgAw&type=a340'
        st.image(imglink)
        st.info('교재 바로보기')
c3, c4 = st.columns((4, 1))
with c3:
    with st.expander("AI에게 질문하기"):

        st.write("학습 내용을 ChatGPT에게 질문해보세요.")

        question = st.text_area(
            "질문 작성",
            "이 교재 내용을 초등학생도 이해할 수 있게 설명해줘."
        )

        if st.button("ChatGPT로 질문 보내기"):

            encoded = urllib.parse.quote(question)
            url = f"https://chat.openai.com/?q={encoded}"

            st.link_button("ChatGPT 열기", url)
with c4:
    with st.expander('Tips..'):
        imglink = 'https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNTEyMjZfMiAg%2FMDAxNzY2NzIyNDU3OTIx.KzfLq8B-pma-G0ru_h1MzUnxBqcwfVtZMOYLWV4Xd1Yg.g5SiQNNZTjR7W5B9_E8pY8xQXpptQBDSLzG2cykCCa8g.JPEG%2FScreenshot%25A3%25DF20251226%25A3%25DF131100%25A3%25DFOne_UI_Home.jpg&type=a340'
        st.image(imglink)
        st.info('챗GPT에게 질문하기')
c5, c6 = st.columns((4, 1))
with c5:
    with open("인재원AI교재.pdf", "rb") as f:
        st.download_button(label="교재 다운로드", data=f, file_name="AI교재.pdf", mime="application/pdf")
        st.markdown(txt_data)
with c6:
    with st.expander('Tips..'):
        imglink = 'https://search.pstatic.net/sunny/?src=https%3A%2F%2Fcdn-icons-png.freepik.com%2F512%2F10152%2F10152125.png&type=a340'
        st.image(imglink)
        st.info('교재파일 다운받기ck')
