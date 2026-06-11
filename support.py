import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random

# --- 1. 앱 설정 및 CSS 스타일 (초기 선호 디자인 복구 및 고정) ---
st.set_page_config(layout="wide", page_title="지방자치인재개발원 교육지원시스템")

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

        /* [디자인 복구] 초기 선호 스타일: 어두운 남색 바탕 / 하얀 글씨 메뉴 버튼 */
        div.stButton > button {
            background-color: #003366 !important; /* 어두운 남색 */
            color: white !important; /* 하얀 글씨 */
            border-radius: 5px;
            border: none;
            height: 55px !important; 
            width: 100% !important; 
            font-weight: 700 !important;
            font-size: 17px !important;
            transition: background 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #002244 !important;
        }

        /* 버튼 간격 최적화 */
        [data-testid="column"] { padding: 0 4px !important; }

        /* 표(Table) 헤더 디자인 */
        thead tr th {
            background-color: #f0f2f6 !important;
            color: #003366 !important;
            text-align: center !important;
        }

        /* 헤더 영역 */
        .header-box { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 3px solid #003366; }
        .auth-buttons { display: flex; gap: 10px; }
        .auth-btn { border: 1px solid #ddd; padding: 6px 16px; border-radius: 4px; font-size: 0.9rem; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- 2. 데이터베이스 초기화 ---
@st.cache_resource
def init_db():
    conn = sqlite3.connect('logodi_v_final.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, title TEXT, content TEXT, author TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS replies (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, author TEXT, content TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS lecture_schedule (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, start_time TEXT, end_time TEXT, title TEXT, lecturer TEXT, file_data BLOB, file_name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS facility_files (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, file_data BLOB, file_name TEXT, date TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- 3. 세션 상태 관리 ---
if 'current_menu' not in st.session_state: st.session_state.current_menu = "홈"
if 'chat_history' not in st.session_state: st.session_state.chat_history = [{"role": "assistant", "content": "안녕하세요! 궁금한 점을 질문해 주세요."}]
if 'group_members' not in st.session_state:
    st.session_state.group_members = ["김철수", "이영희", "박지민", "최유진", "정현우", "강다솜", "임세찬", "윤서아", "오지훈", "한나래"]

def set_menu(menu_name):
    st.session_state.current_menu = menu_name

# --- 4. 상단 헤더 및 메뉴 ---
st.markdown(f"""
    <div class="header-box">
        <img src="https://www.logodi.go.kr/images/common/logo.png" width="250">
        <div class="auth-buttons">
            <div class="auth-btn" style="background:white; color:#333;">로그인</div>
            <div class="auth-btn" style="background:#003366; color:white;">회원가입</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br><h2 style='text-align: center; color: #003366;'>지방자치인재개발원 교육지원시스템</h2>", unsafe_allow_html=True)

m_cols = st.columns(5)
menus = ["1. 안내", "2. 일정", "3. 공지사항", "4. 소모임", "5. Q&A"]
for i, m in enumerate(menus):
    if m_cols[i].button(m, key=f"nav_{i}"): set_menu(m)

st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

# --- 5. 공통 게시판 로직 ---
def show_board(category):
    st.subheader(f"📋 {category} 목록")
    df = pd.read_sql(f"SELECT id, title, author, date FROM posts WHERE category='{category}' ORDER BY id DESC LIMIT 10", conn)
    if not df.empty:
        st.table(df.rename(columns={'id':'순번', 'title':'제목', 'author':'작성자', 'date':'작성일시'}))
        with st.expander("상세 내용 확인 및 답글 달기"):
            pid = st.selectbox("순번 선택", df['id'].tolist(), key=f"sel_{category}")
            p = conn.execute("SELECT title, content, author, date FROM posts WHERE id=?", (pid,)).fetchone()
            if p:
                st.info(f"**제목: {p[0]}**\n\n{p[1]}")
                reps = pd.read_sql(f"SELECT author, content, date FROM replies WHERE post_id={pid}", conn)
                for _, r in reps.iterrows(): st.caption(f"↳ {r['author']}: {r['content']} ({r['date']})")
                with st.form(f"rep_{pid}"):
                    rt = st.text_input("답글 입력")
                    if st.form_submit_button("등록"):
                        conn.execute("INSERT INTO replies (post_id, author, content, date) VALUES (?,?,?,?)", (pid, "관리자", rt, datetime.now().strftime("%Y-%m-%d %H:%M")))
                        conn.commit(); st.rerun()
    else: st.info("데이터가 없습니다.")
    with st.expander(f"➕ {category} 작성하기"):
        with st.form(f"w_{category}"):
            wt, wa, wc = st.text_input("제목"), st.text_input("작성자", value="관리자"), st.text_area("내용")
            if st.form_submit_button("저장"):
                conn.execute("INSERT INTO posts (category, title, content, author, date) VALUES (?,?,?,?,?)", (category, wt, wc, wa, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit(); st.rerun()

# --- 6. 메뉴별 상세 구현 ---

if st.session_state.current_menu == "홈":
    st.image("https://www.logodi.go.kr/images/common/main_visual_01.jpg", use_container_width=True)
    recent = pd.read_sql("SELECT title, author, date FROM posts ORDER BY id DESC LIMIT 5", conn)
    if not recent.empty: st.table(recent.rename(columns={'title':'최근 소식','author':'작성자','date':'날짜'}))

elif st.session_state.current_menu == "1. 안내":
    t = st.tabs(["전달사항", "교육안내", "시설안내", "문의사항"])
    with t[0]: show_board("전달사항")
    with t[1]: show_board("교육안내")
    with t[2]:
        st.subheader("🏛️ 시설 안내")
        st.image("https://www.logodi.go.kr/images/sub/img_facility_01.jpg", width=800)
        f_df = pd.read_sql("SELECT id, title, file_name, date FROM facility_files", conn)
        if not f_df.empty: st.table(f_df.rename(columns={'id':'순번','title':'자료명','file_name':'파일명','date':'등록일'}))
        with st.expander("파일 업로드"):
            with st.form("fac"):
                ft, ff = st.text_input("자료 제목"), st.file_uploader("파일", type=['pdf','docx'])
                if st.form_submit_button("업로드"):
                    if ff: conn.execute("INSERT INTO facility_files (title, file_data, file_name, date) VALUES (?,?,?,?)", (ft, ff.read(), ff.name, datetime.now().strftime("%Y-%m-%d"))); conn.commit(); st.rerun()
    with t[3]: show_board("문의사항")

elif st.session_state.current_menu == "2. 일정":
    t = st.tabs(["시간표", "금일 강의"])
    h_opts = [f"{h:02d}:00" for h in range(9, 19)]
    with t[1]:
        with st.form("lec"):
            s_t, e_t = st.selectbox("시작", h_opts), st.selectbox("종료", h_opts, index=1)
            lt, ln, lf = st.text_input("제목"), st.text_input("강사"), st.file_uploader("교재", type="pdf")
            if st.form_submit_button("등록"):
                conn.execute("INSERT INTO lecture_schedule (date, start_time, end_time, title, lecturer, file_data, file_name) VALUES (?,?,?,?,?,?,?)", (datetime.now().strftime("%Y-%m-%d"), s_t, e_t, lt, ln, lf.read() if lf else None, lf.name if lf else "")); conn.commit(); st.rerun()
        lecs = pd.read_sql(f"SELECT start_time, end_time, title, lecturer, file_name FROM lecture_schedule WHERE date='{datetime.now().strftime('%Y-%m-%d')}' ORDER BY start_time", conn)
        if not lecs.empty:
            lecs.insert(0, '차시', range(1, len(lecs)+1)); lecs['시간'] = lecs['start_time'] + "~" + lecs['end_time']
            st.table(lecs[['차시','시간','title','lecturer','file_name']].rename(columns={'title':'강의제목','lecturer':'강사명','file_name':'교재파일'}))
    with t[0]:
        tt = pd.DataFrame(index=h_opts[:-1], columns=["교육 내용"])
        data = conn.execute(f"SELECT start_time, title FROM lecture_schedule WHERE date='{datetime.now().strftime('%Y-%m-%d')}'").fetchall()
        for s, tit in data:
            if s in tt.index: tt.at[s, "교육 내용"] = tit
        st.table(tt.fillna("-"))

elif st.session_state.current_menu == "3. 공지사항":
    t = st.tabs(["담당자 공지", "소모임 공지", "내 그룹 공지"])
    with t[0]: show_board("담당자 공지")
    with t[1]: show_board("소모임 공지")
    with t[2]:
        st.subheader("📱 내 그룹 공지 (SMS 전송 시뮬레이션)")
        with st.form("sms_sim"):
            msg = st.text_area("메시지 내용", placeholder="전송할 내용을 입력하세요.")
            st.markdown("**[그룹원 선택]**")
            
            # [수정 핵심] 전체 선택 체크박스
            is_all = st.checkbox("전체 선택하기 (모두 클릭)")
            
            selected_users = []
            grid = st.columns(5)
            for i, name in enumerate(st.session_state.group_members):
                with grid[i % 5]:
                    # value=is_all 설정을 통해 상단 체크박스와 실시간 연동
                    if st.checkbox(name, value=is_all, key=f"user_check_{i}"):
                        selected_users.append(name)
            
            st.divider()
            if st.form_submit_button("SMS 전송"):
                if not msg: st.warning("내용을 입력하세요.")
                elif not selected_users: st.warning("대상을 선택하세요.")
                else: st.success(f"✅ 전송되었습니다. (수신인: {', '.join(selected_users)})")

elif st.session_state.current_menu == "4. 소모임":
    show_board("소모임 활동")

elif st.session_state.current_menu == "5. Q&A":
    st.subheader("💬 AI 챗봇")
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    q = st.text_input("궁금한 점을 입력하세요", key="qa_input")
    if st.button("질문하기"):
        if q:
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.session_state.chat_history.append({"role": "assistant", "content": f"'{q}'에 대한 교육지원 안내입니다. 상세 내용은 공지사항을 확인 바랍니다."})
            st.rerun()

# --- 7. 푸터 ---
st.markdown("---")
f1, f2 = st.columns([8, 2])
with f1:
    st.caption("지방자치인재개발원 | (54315) 전북특별자치도 완주군 이서면 반교로 150 | TEL. 063-907-5100")
    st.caption("Copyright © Local Government Officials Development Institute. All Rights Reserved.")
with f2: st.image("https://www.logodi.go.kr/images/common/f_logo.png", width=150)
