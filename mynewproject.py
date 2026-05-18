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
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT,
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
    st.write("등록할 사람의 정보를 입력해 주세요.")

    # 입력 폼 생성 (제출 시 폼 안의 내용이 초기화됨)
    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("이름 (필수)", placeholder="홍길동")
        phone = st.text_input("연락처 (필수)", placeholder="010-0000-0000")
        address = st.text_input("주소 (필수)", placeholder="서울특별시 ...")
        email = st.text_input("이메일 (선택)", placeholder="user@email.com")
        
        # 폼 제출 버튼
        submitted = st.form_submit_button("등록하기")

        if submitted:
            if not name or not phone or not address:
                st.error("이름, 연락처, 주소는 필수 입력 항목입니다.")
            else:
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # DB에 데이터 저장
                conn = sqlite3.connect('myproject.db')
                c = conn.cursor()
                c.execute('''
                    INSERT INTO address (name, phone, address, email, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, phone, address, email, created_at))
                conn.commit()
                conn.close()
                
                st.success(f"'{name}'님의 정보가 성공적으로 등록되었습니다!")

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