import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# 1. 초기 데이터 생성 및 세션 상태 저장
def generate_mock_data():
    last_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황"]
    first_names = ["민준", "서연", "도윤", "서윤", "시우", "지우", "준우", "하윤", "주원", "지민", "건우", "윤서", "예준", "지아", "현우", "나은"]
    
    data = []
    for _ in range(100):
        name = random.choice(last_names) + random.choice(first_names)
        kor = random.randint(40, 100)
        eng = random.randint(40, 100)
        math = random.randint(40, 100)
        sci = random.randint(40, 100)
        
        total = kor + eng + math + sci
        avg = round(total / 4, 2)
        
        # 등급 산정
        if avg >= 90: grade = 'A'
        elif avg >= 80: grade = 'B'
        elif avg >= 70: grade = 'C'
        elif avg >= 60: grade = 'D'
        else: grade = 'E'
        
        data.append([name, kor, eng, math, sci, total, avg, grade])
    
    return pd.DataFrame(data, columns=['이름', '국어', '영어', '수학', '과학', '총점', '평균', '등급'])

# 세션 상태에 데이터가 없으면 생성
if 'df' not in st.session_state:
    st.session_state.df = generate_mock_data()

# 2. 사이드바 메뉴 설정
st.sidebar.title("📚 성적 관리 시스템")
menu = st.sidebar.radio("메뉴를 선택하세요", ["HOME", "성적테이블조회", "성적시각화"])

# 3. 메뉴별 페이지 구현
if menu == "HOME":
    st.title("🏠 성적 처리 시스템 HOME")
    st.write("Streamlit으로 구현된 간단한 성적 관리 애플리케이션입니다.")
    st.info("왼쪽 사이드바에서 메뉴를 선택하여 데이터를 확인하거나 시각화할 수 있습니다.")
    
    # 데이터 요약 정보
    st.subheader("📊 시스템 요약 정보")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 학생 수", f"{len(st.session_state.df)}명")
    col2.metric("전체 평균", f"{st.session_state.df['평균'].mean():.2f}점")
    col3.metric("최고점(총점)", f"{st.session_state.df['총점'].max()}점")

    # CSV 다운로드 버튼
    st.subheader("📥 데이터 내보내기")
    csv = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="score.csv 다운로드",
        data=csv,
        file_name='score.csv',
        mime='text/csv',
    )

elif menu == "성적테이블조회":
    st.title("📋 성적 데이터 조회")
    st.write("전체 학생의 성적 데이터를 확인하고 필터링할 수 있습니다.")
    
    # 검색 기능
    search_name = st.text_input("이름으로 검색")
    if search_name:
        display_df = st.session_state.df[st.session_state.df['이름'].str.contains(search_name)]
    else:
        display_df = st.session_state.df
    
    st.dataframe(display_df, use_container_width=True)

elif menu == "성적시각화":
    st.title("📈 성적 데이터 시각화")
    
    # 1. 등급 분포 파이 차트
    st.subheader("📍 등급별 분포")
    grade_counts = st.session_state.df['등급'].value_counts().sort_index()
    fig_pie = px.pie(values=grade_counts.values, names=grade_counts.index, title="등급 비율")
    st.plotly_chart(fig_pie)
    
    # 2. 과목별 점수 분포 박스플롯
    st.subheader("📍 과목별 점수 분포")
    subjects = ['국어', '영어', '수학', '과학']
    fig_box = px.box(st.session_state.df, y=subjects, title="과목별 점수 범위")
    st.plotly_chart(fig_box)
    
    # 3. 평균 점수 히스토그램
    st.subheader("📍 평균 점수 분포")
    fig_hist = px.histogram(st.session_state.df, x="평균", nbins=20, title="평균 점수 도수분포표")
    st.plotly_chart(fig_hist)
