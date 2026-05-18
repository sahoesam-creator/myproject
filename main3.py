import streamlit as st
import pandas as pd
import random
import os

# 페이지 기본 설정
st.set_page_config(page_title="현업적용도 조사 시스템", layout="wide")

# 가상 데이터 생성 함수 (5점 척도: 5=매우그렇다 ~ 1=전혀아니다)
def generate_mock_data():
    last_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "전", "홍"]
    first_names = ["민준", "서연", "도윤", "서윤", "시우", "지우", "민재", "하윤", "주원", "은우", "지안", "윤서", "예준", "수아", "준우", "지훈", "지민", "상철", "영희", "민수"]
    
    data = []
    for _ in range(100):
        name = random.choice(last_names) + random.choice(first_names)
        # 1~5점 랜덤 부여
        satisfaction = random.randint(1, 5)
        competency = random.randint(1, 5)
        utility = random.randint(1, 5)
        
        total = satisfaction + competency + utility
        avg = round(total / 3, 2)
        
        data.append([name, satisfaction, competency, utility, total, avg])
        
    df = pd.DataFrame(data, columns=['이름', '만족도', '역량향상도', '업무활용도', '총점', '평균점수'])
    # 엑셀 등에서 한글 깨짐을 방지하기 위해 utf-8-sig 사용
    df.to_csv('score2.csv', index=False, encoding='utf-8-sig')
    return df

# 사이드바 메뉴 구성
st.sidebar.title("교육운영 지원 메뉴")
menu = st.sidebar.radio("메뉴 이동", ["HOME", "데이터조회", "그래프"])

# 1. HOME 화면
if menu == "HOME":
    st.title("📊 교육과정 현업적용도 조사 분석")
    st.write("본 시스템은 교육과정 수료자를 대상으로 한 현업적용도(만족도, 역량향상도, 업무활용도) 결과를 분석하는 프로토타입입니다.")
    
    st.markdown("---")
    st.subheader("1. 설문 결과 Mock Data 생성")
    st.write("테스트를 위한 100명의 가상 설문 데이터를 생성하고 시스템에 적용합니다.")
    
    if st.button("데이터 생성하기 (100건)"):
        df = generate_mock_data()
        st.success("✅ score.csv 파일이 성공적으로 생성 및 저장되었습니다!")
        st.dataframe(df.head())
        
    # score.csv 파일이 존재할 경우 다운로드 버튼 활성화
    if os.path.exists("score2.csv"):
        st.write("생성된 전체 데이터를 다운로드할 수 있습니다.")
        with open("score2.csv", "rb") as file:
            st.download_button(
                label="📥 score2.csv 파일 다운로드",
                data=file,
                file_name="score2.csv",
                mime="text/csv"
            )

# 2. 데이터조회 화면
elif menu == "데이터조회":
    st.title("📋 데이터 조회")
    
    if os.path.exists("score2.csv"):
        df = pd.read_csv("score2.csv")
        
        st.write("### 전체 설문 결과 데이터")
        # 데이터프레임 출력 (정렬, 필터링 가능)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
        st.write("### 💡 데이터 요약 통계")
        # 점수 관련 컬럼의 통계치 제공
        st.dataframe(df[['만족도', '역량향상도', '업무활용도', '총점', '평균점수']].describe().round(2), use_container_width=True)
    else:
        st.warning("⚠️ 등록된 데이터가 없습니다. HOME 메뉴에서 데이터를 먼저 생성해주세요.")

# 3. 그래프 화면
elif menu == "그래프":
    st.title("📈 현업적용도 분석 그래프")
    
    if os.path.exists("score2.csv"):
        df = pd.read_csv("score2.csv")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 항목별 평균 점수")
            # 3개 항목의 평균을 구하여 막대그래프로 출력
            mean_scores = df[['만족도', '역량향상도', '업무활용도']].mean().to_frame("평균점수")
            st.bar_chart(mean_scores)
            
        with col2:
            st.write("### 교육생 총점 분포")
            # 총점(3~15점)의 빈도수를 계산하여 분포도 출력
            score_counts = df['총점'].value_counts().sort_index()
            st.bar_chart(score_counts)
            
        st.markdown("---")
        st.write("### 세부 항목별 척도(1~5점) 응답 비율")
        # 만족도, 역량향상도, 업무활용도의 각 점수별 빈도수
        satisfaction_dist = df['만족도'].value_counts().sort_index()
        competency_dist = df['역량향상도'].value_counts().sort_index()
        utility_dist = df['업무활용도'].value_counts().sort_index()
        
        dist_df = pd.DataFrame({
            '만족도': satisfaction_dist,
            '역량향상도': competency_dist,
            '업무활용도': utility_dist
        }).fillna(0) # 응답이 없는 점수대는 0으로 처리
        
        st.line_chart(dist_df)
        
    else:
        st.warning("⚠️ 분석할 데이터가 없습니다. HOME 메뉴에서 데이터를 먼저 생성해주세요.")