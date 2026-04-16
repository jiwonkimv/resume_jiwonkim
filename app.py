import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="브랜드 발굴 레이더 | Shell",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Theme / CSS
# --------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #f6f7f8;
    --card: #ffffff;
    --text: #111827;
    --muted: #6b7280;
    --line: #e5e7eb;
    --green: #15936f;
    --green-soft: rgba(21,147,111,.10);
    --amber: #b7791f;
    --blue: #2563eb;
    --red: #dc2626;
    --shadow: 0 10px 30px rgba(17,24,39,.05);
    --radius: 18px;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f8fafb 0%, #f4f6f8 100%);
}

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--line);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.hero {
    background: linear-gradient(135deg, #ffffff 0%, #f7fbf9 55%, #eef8f4 100%);
    border: 1px solid #e6efe9;
    border-radius: 24px;
    padding: 28px 30px 24px 30px;
    box-shadow: var(--shadow);
    margin-bottom: 18px;
}
.hero-eyebrow {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: var(--green-soft);
    color: var(--green);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .03em;
}
.hero-title {
    font-size: 32px;
    line-height: 1.15;
    font-weight: 700;
    color: var(--text);
    margin: 14px 0 10px 0;
}
.hero-sub {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.65;
    max-width: 880px;
}

.panel {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 18px 18px 16px 18px;
    box-shadow: var(--shadow);
    margin-bottom: 14px;
}
.panel-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 6px;
}
.panel-desc {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 14px;
}

.metric-card {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px 18px 16px 18px;
    box-shadow: var(--shadow);
    min-height: 112px;
}
.metric-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .04em;
}
.metric-value {
    font-size: 30px;
    line-height: 1.1;
    font-weight: 700;
    color: var(--text);
    margin-top: 12px;
}
.metric-foot {
    font-size: 12px;
    color: var(--muted);
    margin-top: 10px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
}
.pill-green { background: #e8f7f1; color: #13795b; }
.pill-amber { background: #fff4df; color: #9a6700; }
.pill-blue { background: #eaf2ff; color: #1d4ed8; }
.pill-gray { background: #f3f4f6; color: #4b5563; }

.candidate-card {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
    box-shadow: var(--shadow);
    margin-bottom: 12px;
}
.candidate-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 14px;
}
.candidate-name {
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin: 0;
}
.candidate-meta {
    font-size: 13px;
    color: var(--muted);
    margin-top: 4px;
}
.candidate-score {
    text-align: right;
}
.score-label {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .04em;
}
.score-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--green);
    line-height: 1.1;
    margin-top: 6px;
}

.store-chip {
    background: #f8fafc;
    border: 1px solid #e8edf3;
    border-radius: 14px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.store-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
}
.store-sub {
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
}

.placeholder-box {
    border: 1.5px dashed #cdd5df;
    border-radius: 18px;
    padding: 26px 18px;
    text-align: center;
    background: #fafbfc;
    color: var(--muted);
}

.small-note {
    font-size: 12px;
    color: var(--muted);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 8px 14px;
    height: auto;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    border-color: #cfe3da !important;
}

div[data-testid="stExpander"] {
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    background: #fff !important;
}

[data-testid="stMetric"] {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 10px 14px;
}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Dummy data
# --------------------------------------------------

def get_dummy_candidates() -> list[dict]:
    return [
        {
            "name": "브랜드 A",
            "category": "테크 / 가전",
            "score": 82.4,
            "status": ["신규 발굴", "선점 가능", "고성장"],
            "summary": "검색량, 커뮤니티 반응, 콘텐츠 확산 속도가 동시에 올라오는 상황을 가정한 샘플 카드입니다.",
            "signals": {
                "검색량 성장률": 86,
                "SNS 저장 반응": 74,
                "커뮤니티 언급": 68,
                "경쟁사 미등장": 92,
            },
            "stores": [
                {"name": "잠실점", "fit": 91, "desc": "MZ·팝업 반응 강점"},
                {"name": "동탄점", "fit": 84, "desc": "얼리어답터·가족 수요"},
                {"name": "본점", "fit": 78, "desc": "프리미엄 노출 적합"},
            ],
            "memo": "브랜드 A는 롯데백화점 내 단기 팝업 테스트에 적합한 후보로 가정합니다.",
        },
        {
            "name": "브랜드 B",
            "category": "라이프스타일 / 홈",
            "score": 74.1,
            "status": ["신규 발굴", "관찰 필요"],
            "summary": "리빙 카테고리 기반의 샘플 케이스로, 검색량은 우수하나 경쟁사 노출 여부를 추가 검토해야 하는 상황입니다.",
            "signals": {
                "검색량 성장률": 78,
                "SNS 저장 반응": 61,
                "커뮤니티 언급": 66,
                "경쟁사 미등장": 54,
            },
            "stores": [
                {"name": "영등포점", "fit": 88, "desc": "가전·리빙 친화 점포"},
                {"name": "본점", "fit": 80, "desc": "프리미엄 큐레이션 적합"},
                {"name": "인천점", "fit": 73, "desc": "글로벌 수요 테스트 가능"},
            ],
            "memo": "추후 내부 거래선 DB, 점포별 고객군, 경쟁사 팝업 이력을 연결할 수 있습니다.",
        },
        {
            "name": "브랜드 C",
            "category": "뷰티 / 퍼퓨머리",
            "score": 68.7,
            "status": ["기거래선 가능성", "선점 가능"],
            "summary": "퍼퓨머리/뷰티 계열 UI 테스트용 샘플 카드입니다. 실제 기능 연결 시 상세 근거 영역을 채우면 됩니다.",
            "signals": {
                "검색량 성장률": 63,
                "SNS 저장 반응": 77,
                "커뮤니티 언급": 59,
                "경쟁사 미등장": 76,
            },
            "stores": [
                {"name": "강남점", "fit": 92, "desc": "감도 높은 고객군 적합"},
                {"name": "잠실점", "fit": 85, "desc": "트렌드 반응 검증 적합"},
                {"name": "본점", "fit": 79, "desc": "브랜드 노출 효과 기대"},
            ],
            "memo": "기능 추가 시 브랜드별 시계열, 뉴스, 제안서 자동생성을 붙일 수 있도록 구조만 남겨두었습니다.",
        },
    ]


def get_dummy_pipeline_status() -> list[dict]:
    return [
        {"step": "키워드 수집", "status": "대기", "detail": "Google Trends / Naver DataLab 연결 예정"},
        {"step": "후보 정제", "status": "대기", "detail": "중복 제거·브랜드명 정규화·카테고리 분류"},
        {"step": "점수 산출", "status": "대기", "detail": "가중치 로직 연결 예정"},
        {"step": "점포 얼라인", "status": "대기", "detail": "점포 프로필 및 타깃 매핑 예정"},
        {"step": "제안서 생성", "status": "대기", "detail": "LLM 템플릿 연결 예정"},
    ]


# --------------------------------------------------
# Helper renderers
# --------------------------------------------------

def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero">
            <span class="hero-eyebrow">UI SHELL · FUNCTION READY</span>
            <div class="hero-title">브랜드 발굴 레이더</div>
            <div class="hero-sub">
                기능은 비워두고 화면 구조만 먼저 고정한 Streamlit 깡통 버전입니다.
                이후 Google Trends, 네이버 API, 내부 거래선 DB, 제안서 자동생성 기능을 단계적으로 붙일 수 있도록
                카드/패널/탭 구조를 모듈형으로 정리했습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_metrics(candidates: list[dict]) -> None:
    cols = st.columns(4)
    metrics = [
        ("발굴 후보", f"{len(candidates)}", "현재는 더미 데이터"),
        ("평균 점수", f"{sum(c['score'] for c in candidates)/len(candidates):.1f}", "실제 계산 로직 연결 가능"),
        ("선점 가능", "2", "경쟁사 미등장 태그 샘플"),
        ("추천 점포 매칭", "9", "후보×Top3 점포 기준"),
    ]
    for col, (label, value, foot) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-foot">{foot}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_signal_chart(signals: dict) -> None:
    labels = list(signals.keys())
    values = list(signals.values())
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            text=[str(v) for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        height=230,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(range=[0, 110], showgrid=False, showticklabels=False),
        xaxis=dict(tickfont=dict(size=11)),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_placeholder(title: str, desc: str, height: int = 170) -> None:
    st.markdown(
        f"""
        <div class="placeholder-box" style="min-height:{height}px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <div style="font-weight:700; color:#374151; margin-bottom:6px;">{title}</div>
            <div style="font-size:13px; max-width:460px; line-height:1.6;">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_candidate_card(item: dict) -> None:
    pill_html = []
    for tag in item["status"]:
        cls = "pill-green"
        if "관찰" in tag or "기거래선" in tag:
            cls = "pill-amber"
        elif "선점" in tag:
            cls = "pill-blue"
        pill_html.append(f'<span class="status-pill {cls}">{tag}</span>')

    with st.container():
        st.markdown(
            f"""
            <div class="candidate-card">
                <div class="candidate-head">
                    <div>
                        <div class="candidate-name">{item['name']}</div>
                        <div class="candidate-meta">{item['category']}</div>
                    </div>
                    <div class="candidate-score">
                        <div class="score-label">Trend Score</div>
                        <div class="score-value">{item['score']:.1f}</div>
                    </div>
                </div>
                <div>{''.join(pill_html)}</div>
                <div style="margin-top:12px; font-size:14px; color:#4b5563; line-height:1.65;">{item['summary']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab1, tab2, tab3, tab4 = st.tabs(["신호", "점포 얼라인", "제안 메모", "연결 예정"])
        with tab1:
            render_signal_chart(item["signals"])
        with tab2:
            cols = st.columns(3)
            for col, store in zip(cols, item["stores"]):
                with col:
                    st.markdown(
                        f"""
                        <div class="store-chip">
                            <div class="store-title">{store['name']}</div>
                            <div style="font-size:22px; font-weight:700; color:#15936f; margin-top:8px;">{store['fit']}%</div>
                            <div class="store-sub">{store['desc']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        with tab3:
            st.text_area(
                "메모",
                value=item["memo"],
                height=180,
                key=f"memo_{item['name']}",
            )
            st.caption("현재는 편집 가능한 더미 텍스트만 표시합니다.")
        with tab4:
            render_placeholder(
                "기능 연결 슬롯",
                "이 영역에 API 응답 원본, 경쟁사 뉴스, 내부 거래선 DB 매칭, 제안서 자동생성 결과 등을 단계적으로 연결할 수 있습니다.",
                height=150,
            )


# --------------------------------------------------
# Future integration stubs
# --------------------------------------------------

def fetch_google_trends():
    """TODO: Google Trends 수집 로직 연결"""
    return None


def fetch_naver_datalab():
    """TODO: Naver DataLab 수집 로직 연결"""
    return None


def calculate_trend_score(data=None):
    """TODO: 트렌드 점수 산출 로직 연결"""
    return None


def generate_proposal_text(candidate=None):
    """TODO: 제안서 자동 생성 로직 연결"""
    return None


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("### 설정 패널")
    st.caption("지금은 UI만 유지하는 깡통 버전입니다.")

    st.markdown("#### 카테고리")
    selected_categories = []
    category_defaults = {
        "테크 / 가전": True,
        "라이프스타일 / 홈": True,
        "뷰티 / 퍼퓨머리": False,
        "패션 / 어패럴": False,
        "푸드 / 디저트": False,
        "캐릭터 IP / 굿즈": False,
    }
    for category, default in category_defaults.items():
        if st.checkbox(category, value=default):
            selected_categories.append(category)

    st.markdown("#### 필터")
    min_score = st.slider("최소 점수", 0, 100, 60)
    only_new = st.toggle("신규 브랜드만 보기", value=False)
    show_debug = st.toggle("디버그 패널 보기", value=True)

    st.markdown("#### 가중치 (비활성 예시)")
    st.slider("검색량", 0.0, 1.0, 0.30, 0.05, disabled=True)
    st.slider("SNS 반응", 0.0, 1.0, 0.25, 0.05, disabled=True)
    st.slider("커뮤니티", 0.0, 1.0, 0.20, 0.05, disabled=True)
    st.slider("선점성", 0.0, 1.0, 0.25, 0.05, disabled=True)

    st.markdown("#### 액션")
    st.button("자동 발굴 실행", type="primary", use_container_width=True, disabled=True)
    st.button("샘플 데이터 새로고침", use_container_width=True)

    st.markdown("---")
    st.caption(f"마지막 업데이트 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")


# --------------------------------------------------
# Main content
# --------------------------------------------------
candidates = get_dummy_candidates()
if selected_categories:
    candidates = [c for c in candidates if c["category"] in selected_categories]
candidates = [c for c in candidates if c["score"] >= min_score]

render_hero()
render_top_metrics(get_dummy_candidates())

left, right = st.columns([1.5, 1], gap="large")

with left:
    st.markdown('<div class="panel"><div class="panel-title">추천 후보 리스트</div><div class="panel-desc">실제 기능 연결 전까지는 더미 카드로 UI만 유지합니다. 카드 구조와 탭 구성은 그대로 재사용 가능합니다.</div></div>', unsafe_allow_html=True)

    search = st.text_input("후보 검색", placeholder="브랜드명, 카테고리 등")
    filtered = candidates
    if search:
        filtered = [c for c in filtered if search.lower() in (c["name"] + c["category"]).lower()]

    if not filtered:
        render_placeholder(
            "표시할 후보가 없습니다",
            "현재 필터 조건에 맞는 더미 카드가 없도록 설정된 상태입니다. 실제 기능 연결 시 이 영역에 빈 상태 UX를 그대로 재사용할 수 있습니다.",
            height=180,
        )
    else:
        for item in filtered:
            render_candidate_card(item)

with right:
    st.markdown('<div class="panel"><div class="panel-title">파이프라인 상태</div><div class="panel-desc">기능 연결 전 단계에서 어떤 영역이 비어 있는지 한눈에 보는 패널입니다.</div></div>', unsafe_allow_html=True)
    for step in get_dummy_pipeline_status():
        st.markdown(
            f"""
            <div class="store-chip">
                <div class="store-title">{step['step']}</div>
                <div class="store-sub"><strong>{step['status']}</strong> · {step['detail']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="panel" style="margin-top:14px;"><div class="panel-title">연결 예정 위젯</div><div class="panel-desc">차트, 로그, 수집 상태, 예외 메시지 슬롯</div></div>', unsafe_allow_html=True)
    render_placeholder(
        "실시간 수집 로그 영역",
        "향후 Google Trends, Naver DataLab, 뉴스 검색, 내부 DB 매칭 결과를 여기서 상태 배너 또는 로그 테이블로 보여줄 수 있습니다.",
        height=180,
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    render_placeholder(
        "점포별 타깃 맵",
        "후속 버전에서 점포 프로필, 고객군, 브랜드 타깃 매칭을 시각화할 수 있는 자리입니다.",
        height=180,
    )

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

bottom_left, bottom_right = st.columns([1, 1], gap="large")

with bottom_left:
    st.markdown('<div class="panel"><div class="panel-title">운영 메모</div><div class="panel-desc">기획 방향이나 후속 작업 TODO를 적어두는 영역입니다.</div></div>', unsafe_allow_html=True)
    st.text_area(
        "운영 메모",
        value=(
            "- 기능은 비워두고 UI 구조만 유지\n"
            "- 추후 Trends/API/DB/LLM 연결\n"
            "- 카드/탭/패널 구조는 그대로 재사용\n"
            "- 점수 계산/필터/로그는 함수 단위로 추가"
        ),
        height=180,
    )

with bottom_right:
    st.markdown('<div class="panel"><div class="panel-title">개발 슬롯</div><div class="panel-desc">나중에 기능 붙일 때 참고할 연결 포인트입니다.</div></div>', unsafe_allow_html=True)
    dev_df = pd.DataFrame(
        [
            ["fetch_google_trends()", "Google Trends 수집"],
            ["fetch_naver_datalab()", "네이버 검색량 수집"],
            ["calculate_trend_score()", "가중치 기반 점수 산출"],
            ["generate_proposal_text()", "제안서 문안 자동 생성"],
        ],
        columns=["Function Stub", "Purpose"],
    )
    st.dataframe(dev_df, use_container_width=True, hide_index=True)
    st.markdown('<div class="small-note">현재 app.py 하나만으로 돌아가지만, 이후 components/ services/ utils 구조로 분리하기 쉽게 설계했습니다.</div>', unsafe_allow_html=True)

if show_debug:
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    with st.expander("디버그 패널", expanded=False):
        st.write({
            "selected_categories": selected_categories,
            "min_score": min_score,
            "only_new": only_new,
            "visible_candidates": [c["name"] for c in filtered] if 'filtered' in locals() else [],
            "shell_mode": True,
        })
