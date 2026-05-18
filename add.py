import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. 데이터베이스 연결 및 테이블 생성 함수
def init_db():
    # 요청하신 myproject.db 파일로 데이터베이스 생성 및 연결
    conn = sqlite3.connect('myproject.db')
    c = conn.cursor()
    # 주소록 저장을 위한 address 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS address (
            idx INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            juso TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            emailadd TEXT NOT NULL,
            gender TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 앱이 실행될 때마다 DB 초기화 함수 호출
init_db()

# 2. 사이드바 메뉴 구성
st.sidebar.title("주소록 관리 메뉴")
menu = st.sidebar.radio("이동할 페이지 선택:", ["홈페이지", "주소 등록", "주소 검색"])

# ---------------------------------------------------------
# 루트 페이지: 홈페이지
# ---------------------------------------------------------
if menu == "홈페이지":
    st.title("🏠 나의 주소록 관리 앱")
    st.write("""
    주소록 관리 앱에 오신 것을 환영합니다!
    
    왼쪽 사이드바 메뉴를 클릭하여 원하는 기능을 사용해 보세요.
    
    * **주소 등록:** 새로운 연락처 정보를 데이터베이스(`myproject.db`)에 안전하게 추가합니다.
    * **주소 검색:** 등록된 사람들의 이름이나 연락처를 검색하고 전체 목록을 확인합니다.
    """)
    st.info("💡 모든 데이터는 내 컴퓨터의 myproject.db 파일에 로컬로 저장됩니다.")

# ---------------------------------------------------------
# 서브페이지 1: 주소 등록
# ---------------------------------------------------------
elif menu == "주소 등록":
    st.title("📝 새로운 주소 등록")
    st.write("모든 항목은 필수 입력 사항입니다.")

    # 입력 폼 구성
    with st.form("address_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("이름", placeholder="예: 홍길동")
            age = st.number_input("나이", min_value=0, max_value=150, value=30, step=1)
            gender = st.selectbox("성별", ["남성", "여성", "기타"])
            
        with col2:
            phone_number = st.text_input("전화번호", placeholder="010-1234-5678")
            emailadd = st.text_input("이메일", placeholder="example@email.com")
            
        juso = st.text_input("주소", placeholder="상세 주소를 입력하세요")
        
        # 등록 버튼
        submitted = st.form_submit_button("주소록에 저장")

        if submitted:
            # TEXT형 컬럼들의 빈 값 체크 (Not Null 제약 조건 준수)
            if not all([name, juso, phone_number, emailadd]):
                st.error("입력되지 않은 항목이 있습니다. 모든 정보를 작성해 주세요.")
            else:
                try:
                    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # DB 저장 프로세스
                    conn = sqlite3.connect('myproject.db')
                    c = conn.cursor()
                    
                    # 요청하신 컬럼 순서대로 매핑
                    c.execute('''
                        INSERT INTO address (name, age, juso, phone_number, emailadd, gender, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (name, int(age), juso, phone_number, emailadd, gender, created_at))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ {name}님의 정보가 'myproject.db'에 성공적으로 저장되었습니다.")
                    
                except Exception as e:
                    st.error(f"저장 중 오류가 발생했습니다: {e}")

# ---------------------------------------------------------
# 서브페이지 2: 주소 검색
# ---------------------------------------------------------
elif menu == "주소 검색":
    st.title("🔍 주소록 검색")
    
    # 검색어 입력
    search_query = st.text_input("검색할 이름을 입력하세요 (비워두면 전체 목록이 표시됩니다):")
    
    # DB에서 데이터 불러오기
    conn = sqlite3.connect('myproject.db')
    
    if search_query:
        # 이름에 검색어가 포함된 데이터만 조회 (LIKE 구문 활용)
        query = "SELECT idx AS 번호, name AS 이름, phone AS 연락처, address AS 주소, email AS 이메일, created_at AS 등록일시 FROM address WHERE name LIKE ?"
        df = pd.read_sql_query(query, conn, params=('%' + search_query + '%',))
    else:
        # 전체 데이터 조회
        query = "SELECT idx AS 번호, name AS 이름, phone AS 연락처, address AS 주소, email AS 이메일, created_at AS 등록일시 FROM address"
        df = pd.read_sql_query(query, conn)
        
    conn.close()

    # 결과 화면 출력
    if df.empty:
        st.warning("등록된 데이터가 없습니다.")
    else:
        st.write(f"총 **{len(df)}**건의 데이터가 있습니다.")
        # 데이터프레임을 화면 너비에 맞춰 표 형태로 출력
        st.dataframe(df, use_container_width=True, hide_index=True)