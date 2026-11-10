Python 3.11.2 (tags/v3.11.2:878ead1, Feb  7 2023, 16:38:35) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import base64
import json
import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 및 테마 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="정관장 레드부스터스 드래프트 예측전",
    page_icon="🏀",
    layout="centered",
)

# KGC 레드/블랙 UI 테마 Custom CSS
st.markdown(
    """
<style>
    .stApp {
        background-color: #C8102E;
        color: #ffffff;
    }
    .schedule-box {
        background-color: #141414;
        border: 2px solid #282828;
        border-radius: 14px;
        padding: 16px;
        color: #ffffff;
        margin-bottom: 16px;
    }
    .schedule-box h5 {
        color: #888888;
        font-size: 13px;
        margin-bottom: 8px;
    }
    .schedule-box p {
        font-size: 16px;
        font-weight: bold;
        margin: 0;
    }
    .shared-card-box {
        background-color: #1e1e1e;
        border: 2px solid #FFD700;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 25px;
    }
    .round-title {
        background-color: #141414;
        color: #FFD700;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 10px;
        display: inline-block;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. 공용 파일 데이터베이스 (DB) 로직
# ---------------------------------------------------------
DB_FILE = "shared_predictions.json"


def load_all_predictions():
    """모든 참가자의 예측 데이터를 파일에서 불러옵니다."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_or_update_prediction(nickname, password, picks_r1, picks_r2):
    """
    닉네임이 이미 존재하면 비밀번호 확인 후 수정,
    새로운 닉네임이면 추가합니다.
    """
    data = load_all_predictions()

    for item in data:
        if item["nickname"] == nickname:
            if item.get("password") == password:
                item["picks_r1"] = picks_r1
                item["picks_r2"] = picks_r2
                with open(DB_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True, " 기존 예측 카드가 수정되었습니다! ✏️"
            else:
                return (
                    False,
                    "⚠️ 이미 등록된 닉네임입니다. 비밀번호가 일치하지 않습니다.",
                )

    data.append(
        {
            "nickname": nickname,
            "password": password,
            "picks_r1": picks_r1,
            "picks_r2": picks_r2,
        }
    )
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True, "🎉 새로운 예측 카드가 성공적으로 등록되었습니다!"


def encode_share_data(nickname, picks_r1, picks_r2):
    payload = json.dumps(
        {"nickname": nickname, "picks_r1": picks_r1, "picks_r2": picks_r2}
    )
    return base64.b64encode(payload.encode("utf-8")).decode("utf-8")


def decode_share_data(encoded_str):
    try:
        decoded_raw = base64.b64decode(encoded_str).decode("utf-8")
        return json.loads(decoded_raw)
    except Exception:
        return None


# ---------------------------------------------------------
# 3. 드래프트 지명 후보 선수 데이터 세트
# ---------------------------------------------------------
PLAYERS_DATA = [
    {"선수명": "이주석", "학교": "건국대", "포지션": "F", "신장": 187},
    {"선수명": "여찬영", "학교": "건국대", "포지션": "G", "신장": 182},
    {"선수명": "전기현", "학교": "건국대", "포지션": "F", "신장": 194},
    {"선수명": "이동근", "학교": "고려대", "포지션": "F", "신장": 197},
    {"선수명": "이경민", "학교": "중앙대", "포지션": "G", "신장": 183},
    {"선수명": "김두진", "학교": "중앙대", "포지션": "F", "신장": 197},
    {"선수명": "유형우", "학교": "중앙대", "포지션": "G", "신장": 185},
    {"선수명": "원건", "학교": "중앙대", "포지션": "G", "신장": 185},
    {"선수명": "장지민", "학교": "명지대", "포지션": "G", "신장": 183},
    {"선수명": "김서원파이팅", "학교": "경희대", "포지션": "G", "신장": 184},
    {"선수명": "임성채", "학교": "경희대", "포지션": "G", "신장": 185},
    {"선수명": "이해솔", "학교": "연세대", "포지션": "G", "신장": 188},
    {"선수명": "부드러운홍상민", "학교": "연세대", "포지션": "C", "신장": 199},
    {"선수명": "이채형", "학교": "연세대", "포지션": "G", "신장": 186},
    {"선수명": "이주영", "학교": "연세대", "포지션": "G", "신장": 188},
    {"선수명": "김태영", "학교": "단국대", "포지션": "G", "신장": 183},
    {"선수명": "최준환", "학교": "상명대", "포지션": "C", "신장": 195},
    {"선수명": "송정우", "학교": "상명대", "포지션": "F", "신장": 192},
    {"선수명": "이한결", "학교": "동국대", "포지션": "G", "신장": 181},
    {"선수명": "우성희", "학교": "동국대", "포지션": "C", "신장": 199},
    {"선수명": "유정원", "학교": "동국대", "포지션": "G", "신장": 191},
    {"선수명": "김상윤", "학교": "동국대", "포지션": "F", "신장": 187},
    {"선수명": "한재혁", "학교": "동국대", "포지션": "G", "신장": 180},
    {"선수명": "백승혁", "학교": "동국대wise", "포지션": "G", "신장": 185},
    {"선수명": "구인교", "학교": "성균관대", "포지션": "F", "신장": 194},
    {"선수명": "김태형", "학교": "성균관대", "포지션": "G", "신장": 180},
    {"선수명": "박상혁", "학교": "성균관대", "포지션": "F", "신장": 189},
    {"선수명": "원준석", "학교": "성균관대", "포지션": "F", "신장": 195},
    {"선수명": "김수오", "학교": "경희대", "포지션": "F", "신장": 199},
    {"선수명": "김승우", "학교": "연세대", "포지션": "F", "신장": 192},
    {"선수명": "류정열", "학교": "한양대", "포지션": "C", "신장": 207},
    {"선수명": "김현우", "학교": "한양대", "포지션": "G", "신장": 178},
    {"선수명": "마윤재", "학교": ".", "포지션": "F", "신장": 188},
    {"선수명": "오벨레제이슨", "학교": "동국대wise", "포지션": "G", "신장": 186},
    {"선수명": "임동일", "학교": "동국대wise", "포지션": "C", "신장": 214},
    {"선수명": "조풍", "학교": "동국대wise", "포지션": "G", "신장": 178},
    {"선수명": "심주언", "학교": "고려대", "포지션": "G/F", "신장": 190},
    {"선수명": "고찬유(소민이거)", "학교": "중앙대", "포지션": "G", "신장": 190},
    {"선수명": "이관우", "학교": "성균관대", "포지션": "G", "신장": 180},
    {"선수명": "구민교", "학교": "성균관대", "포지션": "F", "신장": 197},
    {"선수명": "손유찬", "학교": "한양대", "포지션": "G", "신장": 182},
    {"선수명": "이주민", "학교": "성균관대", "포지션": "F", "신장": 196},
    {"선수명": "김현빈", "학교": "한양대", "포지션": "F", "신장": 186},
    {"선수명": "이건희", "학교": "고려대", "포지션": "G", "신장": 186},
]

df_players = pd.DataFrame(PLAYERS_DATA)
all_player_options = [
    f"{row['선수명']} ({row['학교']}, {row['포지션']}, {row['신장']})"
    for _, row in df_players.iterrows()
]

# ---------------------------------------------------------
# 4. 헤더 및 공유 링크 파싱
# ---------------------------------------------------------
st.markdown(
    '<span style="background:#000; color:#fff; padding:4px 10px; border-radius:12px; font-weight:bold; font-size:12px;">정관장 레드부스터스</span>',
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='color:white; margin-top:8px; font-size:38px;'>드래프트 예측전</h1>",
    unsafe_allow_html=True,
)
st.write(
    "1,2라운드 1~10순위 지명 선수를 예측해 보세요! 가장 많은 정답을 맞히신 분께 (지원이가) 선물을 드립니다 "
)

query_params = st.query_params
shared_data = None
if "share" in query_params:
    shared_data = decode_share_data(query_params["share"])

if shared_data:
    st.markdown(
        f"""
    <div class="shared-card-box">
        <h4>📩 친구가 공유한 예측 카드 도착!</h4>
        <p><b>{shared_data.get('nickname')}</b> 님의 1~2라운드 예측 결과입니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    with st.expander(
        f"⭐ {shared_data.get('nickname')} 님의 예측 카드 보기",
        expanded=True,
    ):
        st.markdown(
            '<div class="round-title">🥇 1라운드 1~10순위</div>',
            unsafe_allow_html=True,
        )
        p1 = shared_data.get("picks_r1", {})
        r1_c1 = st.columns(5)
        for r in range(1, 6):
            with r1_c1[r - 1]:
                st.metric(
                    f"1R {r}순위",
                    p1.get(f"1R_{r}순위", "-").split(" (")[0],
                )
        r1_c2 = st.columns(5)
        for r in range(6, 11):
            with r1_c2[r - 6]:
                st.metric(
                    f"1R {r}순위",
                    p1.get(f"1R_{r}순위", "-").split(" (")[0],
                )

        st.markdown(
            '<div class="round-title">🥈 2라운드 1~10순위</div>',
            unsafe_allow_html=True,
        )
        p2 = shared_data.get("picks_r2", {})
        r2_c1 = st.columns(5)
...         for r in range(1, 6):
...             with r2_c1[r - 1]:
...                 st.metric(
...                     f"2R {r}순위",
...                     p2.get(f"2R_{r}순위", "-").split(" (")[0],
...                 )
...         r2_c2 = st.columns(5)
...         for r in range(6, 11):
...             with r2_c2[r - 6]:
...                 st.metric(
...                     f"2R {r}순위",
...                     p2.get(f"2R_{r}순위", "-").split(" (")[0],
...                 )
... 
... col_sch1, col_sch2 = st.columns(2)
... with col_sch1:
...     st.markdown(
...         """
...     <div class="schedule-box">
...         <h5>순위 추첨 · 11/9(월)</h5>
...         <p> 1순위:KT, 2순위:현대모비스, 3순위:SK, 4순위:정관장♥, 5순위:한국가스공사, 6순위:DB, 7순위:삼성, 8순위:LG, 9순위:소노, 10순위:KCC</p>
...     </div>
...     """,
...         unsafe_allow_html=True,
...     )
... with col_sch2:
...     st.markdown(
...         """
...     <div class="schedule-box">
...         <h5>드래프트 첫 지명 · 11/20(금)</h5>
...         <p>결과 대기 중</p>
...     </div>
...     """,
...         unsafe_allow_html=True,
...     )
... 
... # ---------------------------------------------------------
... # 5. 세션 상태 관리 & 동적 중복 제외 로직
... # ---------------------------------------------------------
... st.markdown("### 🏀 내 예측 카드 작성 및 수정하기")
... st.caption(
    "💡 이미 예측을 제출했더라도 **동일한 닉네임과 비밀번호**를 입력하면 나중에 언제든지 수정할 수 있습니다."
)

all_pick_keys = [f"r1_{r}" for r in range(1, 11)] + [
    f"r2_{r}" for r in range(1, 11)
]

# 세션키 초기화
for key in all_pick_keys:
    if key not in st.session_state:
        st.session_state[key] = "선택 안 함"

# 현재 다른 칸들에서 이미 선택된 선수들의 집합 구하기
currently_selected = {
    st.session_state[k]
    for k in all_pick_keys
    if st.session_state[k] != "선택 안 함"
}


def get_available_options(current_key):
    """현재 특정 드롭다운 칸에서 선택할 수 있는 후보 리스트를 반환합니다."""
    current_val = st.session_state[current_key]
    # 다른 드롭다운에서 선택된 선수는 제외하고, 현재 칸에서 선택했던 선수는 목록에 유지
    filtered = [
        p
        for p in all_player_options
        if p == current_val or p not in currently_selected
    ]
    return ["선택 안 함"] + filtered


col_user1, col_user2 = st.columns(2)
with col_user1:
    nickname = st.text_input(
        "참가자 닉네임",
        key="input_nickname",
        placeholder="닉네임 입력 (예: 레드부스터스팬)",
    )
with col_user2:
    password = st.text_input(
        "비밀번호 (수정 시 사용)",
        type="password",
        key="input_password",
        placeholder="비밀번호 4자리 이상",
    )

# 라운드별 탭 구성
tab1, tab2 = st.tabs(
    ["🥇 1라운드 1~10순위 예측", "🥈 2라운드 1~10순위 예측"]
)

with tab1:
    st.write("1라운드 1순위부터 10순위에 들어갈 선수를 선택하세요.")
    cols_r1 = st.columns(2)
    for rank in range(1, 11):
        key = f"r1_{rank}"
        c_idx = (rank - 1) % 2
        with cols_r1[c_idx]:
            st.selectbox(
                f"1R {rank}순위 지명 선수",
                options=get_available_options(key),
                key=key,
            )

with tab2:
    st.write("2라운드 1순위부터 10순위에 들어갈 선수를 선택하세요.")
    cols_r2 = st.columns(2)
    for rank in range(1, 11):
        key = f"r2_{rank}"
        c_idx = (rank - 1) % 2
        with cols_r2[c_idx]:
            st.selectbox(
                f"2R {rank}순위 지명 선수",
                options=get_available_options(key),
                key=key,
            )

submit_button = st.button(
    "내 카드 저장 및 공유하기 🎟️", use_container_width=True, type="primary"
)

if submit_button:
    user_picks_r1 = {
        f"1R_{r}순위": st.session_state[f"r1_{r}"] for r in range(1, 11)
    }
    user_picks_r2 = {
        f"2R_{r}순위": st.session_state[f"r2_{r}"] for r in range(1, 11)
    }

    if not nickname.strip():
        st.error("닉네임을 입력해 주세요!")
    elif not password.strip():
        st.error("수정할 때 사용할 비밀번호를 입력해 주세요!")
    else:
        selected_r1 = [v for v in user_picks_r1.values() if v != "선택 안 함"]
        selected_r2 = [v for v in user_picks_r2.values() if v != "선택 안 함"]

        if len(selected_r1) < 10 or len(selected_r2) < 10:
            st.warning(
                "⚠️ 1라운드와 2라운드 1~10순위 선수를 모두 선택해 주세요."
            )
        else:
            success, msg = save_or_update_prediction(
                nickname, password, user_picks_r1, user_picks_r2
            )
            if success:
                encoded_code = encode_share_data(
                    nickname, user_picks_r1, user_picks_r2
                )
                st.session_state["last_share_code"] = encoded_code
                st.success(msg)
            else:
                st.error(msg)

# ---------------------------------------------------------
# 6. 카드 공유 링크 생성
# ---------------------------------------------------------
if "last_share_code" in st.session_state:
    st.markdown("#### 🔗 친구에게 내 예측 카드 공유하기")
    share_code = st.session_state["last_share_code"]
    share_param_text = f"?share={share_code}"
    st.info(
        "아래 파라미터 주소를 복사해 친구에게 전달하면 내 1~2라운드 예측 카드를 보여줄 수 있습니다!"
    )
    st.code(share_param_text, language="text")

# ---------------------------------------------------------
# 7. 전체 참가자 예측 카드 목록 (실시간 공용 DB)
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 👥 전체 참가자 예측 목록")

all_predictions = load_all_predictions()

if not all_predictions:
    st.markdown(
        """
    <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; color: #666; text-align: center;">
        🤖 아직 등록된 참가자가 없습니다. 첫 1~2라운드 예측 카드를 만들어 보세요!
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    for item in reversed(all_predictions):
        p_nickname = item["nickname"]
        p1 = item.get("picks_r1", {})
        p2 = item.get("picks_r2", {})

        with st.expander(
            f"👤 {p_nickname} 님의 1~2라운드 예측 카드", expanded=False
        ):
            st.markdown("##### 🥇 1라운드 예측 (1~10순위)")
            r1_cols1 = st.columns(5)
            for r in range(1, 6):
                with r1_cols1[r - 1]:
                    name_only = p1.get(f"1R_{r}순위", "-").split(" (")[0]
                    st.metric(f"1R {r}순위", name_only)

            r1_cols2 = st.columns(5)
            for r in range(6, 11):
                with r1_cols2[r - 6]:
                    name_only = p1.get(f"1R_{r}순위", "-").split(" (")[0]
                    st.metric(f"1R {r}순위", name_only)

            st.markdown("##### 🥈 2라운드 예측 (1~10순위)")
            r2_cols1 = st.columns(5)
            for r in range(1, 6):
                with r2_cols1[r - 1]:
                    name_only = p2.get(f"2R_{r}순위", "-").split(" (")[0]
                    st.metric(f"2R {r}순위", name_only)

            r2_cols2 = st.columns(5)
            for r in range(6, 11):
                with r2_cols2[r - 6]:
                    name_only = p2.get(f"2R_{r}순위", "-").split(" (")[0]
