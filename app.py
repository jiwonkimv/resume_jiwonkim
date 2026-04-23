import os, re, json, html, time, random, smtplib
from collections import Counter
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pytrends.request import TrendReq

st.set_page_config(
    page_title="트렌드 레이더 | 롯데백화점 MD",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Pretendard', -apple-system, sans-serif; }
.main > div { padding-top: 1rem; }

.trend-card {
    background:#fff; border:1px solid #e8ecf0; border-radius:12px;
    padding:14px 18px; margin-bottom:8px;
}
.trend-card.brand  { border-left:3px solid #1D9E75; }
.trend-card.issue  { border-left:3px solid #5B8DEF; }
.trend-card.scarce { border-left:3px solid #E84545; }

.type-tag {
    display:inline-block; padding:2px 8px; border-radius:4px;
    font-size:11px; font-weight:700; letter-spacing:.3px; margin-right:6px;
}
.type-brand  { background:#e7f7ef; color:#0F6E56; }
.type-issue  { background:#eaf0ff; color:#2D5BE3; }
.type-scarce { background:#fde8e8; color:#C0392B; }
.type-existing { background:#fff3e5; color:#854F0B; }

.heat-num { font-size:15px; font-weight:800; }
.heat-hi  { color:#E84545; }
.heat-mid { color:#F39C12; }
.heat-lo  { color:#1D9E75; }

.binfo-card { background:#f7f9fc; border:1px solid #e8ecf0; border-radius:12px; padding:14px 18px; margin-bottom:12px; }

.score-pill { display:inline-block; padding:4px 12px; border-radius:999px; font-size:13px; font-weight:700; }
.score-high { background:#e7f7ef; color:#0F6E56; }
.score-mid  { background:#fff3e5; color:#854F0B; }
.score-low  { background:#f5f5f5; color:#888; }

.verify-ok   { background:#e7f7ef; color:#0F6E56; padding:3px 10px; border-radius:999px; font-size:12px; font-weight:600; }
.verify-warn { background:#fff3e5; color:#854F0B; padding:3px 10px; border-radius:999px; font-size:12px; font-weight:600; }
.verify-info { background:#eaf3ff; color:#185FA5; padding:3px 10px; border-radius:999px; font-size:12px; font-weight:600; }

.sig-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.sig-label { width:90px; font-size:12px; color:#666; flex-shrink:0; }
.sig-bar-bg { flex:1; height:6px; background:#f0f0f0; border-radius:3px; }
.sig-val { width:32px; text-align:right; font-size:12px; font-weight:600; color:#333; }

.store-card { background:#f7f9fc; border-radius:12px; padding:14px 16px; text-align:center; }
.store-name { font-size:14px; font-weight:600; color:#1a1a1a; }
.store-match { font-size:20px; font-weight:700; color:#1D9E75; margin:4px 0; }
.store-traits { font-size:11px; color:#888; line-height:1.6; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SECRETS
# ─────────────────────────────────────────────────────────────
def _s(k, d=""):
    try:    return st.secrets.get(k, d)
    except: return os.getenv(k, d)

NAVER_ID     = _s("NAVER_CLIENT_ID", "").strip()
NAVER_SEC    = _s("NAVER_CLIENT_SECRET", "").strip()
YOUTUBE_KEY  = _s("YOUTUBE_API_KEY", "").strip()
GMAIL_USER   = _s("GMAIL_USER", "").strip()
GMAIL_APP_PW = _s("GMAIL_APP_PASSWORD", "").strip()

# ─────────────────────────────────────────────────────────────
# 트렌드 스캔 시드 — 광범위, 카테고리 없음
# ─────────────────────────────────────────────────────────────
TREND_SCAN_SEEDS = [
    # 밈 / 바이럴
    "요즘 화제","바이럴 화제","인터넷 밈 유행","커뮤니티 화제","틱톡 트렌드",
    "유튜브 쇼츠 화제","인스타 릴스 유행","온라인 이슈","에브리타임 화제",
    # 품귀 / 오픈런
    "품귀현상 2025","한정판 매진","오픈런 화제","품절대란","리셀 급등",
    "당근마켓 급등","한정 굿즈 품귀","팝업 오픈런","대란 아이템",
    # 팝업 / 브랜드 오픈
    "팝업스토어 오픈 2025","신규 브랜드 론칭","플래그십스토어 오픈",
    "한국 첫 상륙 브랜드","서울 팝업 신규","성수동 팝업","홍대 팝업 오픈",
    "강남 팝업스토어","잠실 팝업 오픈","브랜드 한국 진출",
    # 패션 / 스니커즈
    "스니커즈 드롭 화제","한정판 드롭","패션 브랜드 신제품","콜라보 한정판 출시",
    "스트릿 패션 트렌드","하이패션 신규","무신사 인기 브랜드",
    # 뷰티
    "뷰티 신제품 화제","스킨케어 바이럴","메이크업 트렌드","향수 신제품",
    "K뷰티 바이럴","인디 뷰티 브랜드 론칭",
    # 푸드 / 카페
    "신메뉴 화제","먹방 바이럴 신상","카페 신규 오픈","디저트 대란",
    "줄서는 카페","인스타 맛집 오픈","성수 카페 신규","연남동 신규 오픈",
    # 엔터 / IP / 굿즈
    "아이돌 팝업스토어","케이팝 굿즈 화제","웹툰 굿즈 팝업","캐릭터 팝업 오픈",
    "IP 콜라보 한정판","넷플릭스 화제 드라마 굿즈","유튜버 브랜드 론칭",
    # 영화관 / CGV 특수
    "CGV 굿즈 화제","영화관 한정 굿즈","요시컵 cgv","cgv 팝콘통 대란",
    "영화 콜라보 굿즈","메가박스 굿즈","롯데시네마 한정",
    # 테크 / 가전
    "가전 신제품 화제","IT 신제품 출시","스마트기기 신규","소형가전 바이럴",
    # 라이프스타일
    "친환경 브랜드 화제","비건 브랜드 신규","펫 브랜드 론칭","홈인테리어 트렌드",
    "헬스 트렌드 2025","러닝 트렌드","필라테스 브랜드",
    # 특이 트렌드 / 테스트 / 챌린지
    "MBTI 테스트 화제","SBTI 테스트","챌린지 유행","밈 테스트 확산",
    "포켓몬빵 대란","포켓몬카드 대란","스타벅스 한정 화제","편의점 한정 화제",
]

# ─────────────────────────────────────────────────────────────
# 분류 시그널
# ─────────────────────────────────────────────────────────────
BRAND_SIGNALS  = ["브랜드","팝업","론칭","오픈","출시","콜라보","한국 진출","플래그십","스토어","론칭","신규 매장"]
SCARCE_SIGNALS = ["품귀","대란","매진","오픈런","웨이팅","구하기 힘","리셀","품절","줄서","물량 부족"]
ISSUE_SIGNALS  = ["밈","유행","화제","이슈","트렌드","테스트","챌린지","현상","논란","확산"]

def classify_trend(title: str, desc: str) -> str:
    text = (title + " " + desc).lower()
    s = sum(1 for s in SCARCE_SIGNALS if s in text)
    b = sum(1 for s in BRAND_SIGNALS  if s in text)
    i = sum(1 for s in ISSUE_SIGNALS  if s in text)
    if s >= 1:           return "scarce"
    if b >= 2:           return "brand"
    if b >= 1 and i < 2: return "brand"
    return "issue"

# ─────────────────────────────────────────────────────────────
# 노이즈 — 최소화 (너무 강하면 아무것도 안 나옴)
# ─────────────────────────────────────────────────────────────
HARD_NOISE = {
    "정치","선거","사고","사망","경제","주가","환율","코로나","날씨","국회","대통령",
    "뮤직비디오","앨범","컴백","데뷔","콘서트","팬미팅","직캠","티저",
}

def is_noise(token: str) -> bool:
    t = token.strip()
    if len(t) < 2: return True
    if t.lower() in HARD_NOISE: return True
    if re.fullmatch(r"[\d\s\W]+", t): return True
    return False

def extract_main_entity(title: str, desc: str) -> str:
    """제목에서 핵심 명사(브랜드/아이템) 추출 — 관대하게"""
    # 따옴표·괄호 안 우선
    for m in re.finditer(r"['\"\u2018\u2019\u201c\u201d'']([A-Za-z가-힣·&\s]{2,20})['\"\u2018\u2019\u201c\u201d'']", title):
        t = m.group(1).strip()
        if not is_noise(t): return t

    # 영문 대문자 브랜드
    for m in re.finditer(r"\b[A-Z][A-Za-z]{1,14}\b", title):
        t = m.group()
        if not is_noise(t): return t

    # 한글 고유명사 (2~7자) — 제목 앞쪽 우선
    for m in re.finditer(r"[가-힣]{2,7}", title):
        t = m.group()
        if not is_noise(t): return t

    # 마지막 수단: 제목 앞 20자
    return re.sub(r"[^\w가-힣A-Za-z\s]", "", title)[:20].strip()

# ─────────────────────────────────────────────────────────────
# STORE PROFILES
# ─────────────────────────────────────────────────────────────
STORE_PROFILES = {
    "본점":     {"traits":["프리미엄","30~50대","전통 고객층","고단가"],      "keywords":["프리미엄","럭셔리","명품","시계","주얼리","아트"]},
    "잠실점":   {"traits":["MZ","20~35대","팝업 최강","집객↑"],              "keywords":["트렌드","팝업","캐릭터","IP","MZ","굿즈","콜라보","한정판","스트릿","힙","바이럴"]},
    "강남점":   {"traits":["럭셔리","25~45대","패션·뷰티","감도↑"],           "keywords":["럭셔리","패션","뷰티","향수","주얼리","프리미엄","하이엔드"]},
    "영등포점": {"traits":["실용","30~50대","가전·리빙","가족 단위"],          "keywords":["가전","리빙","홈","주방","인테리어","실용","가족"]},
    "부산본점": {"traits":["지역 1위","25~45대","관광","식음료 강"],           "keywords":["카페","디저트","식음료","관광","로컬","부산"]},
    "동탄점":   {"traits":["신도시","25~40대","얼리어답터","가족·유아"],        "keywords":["신도시","캐릭터","키즈","얼리어답터","가족","펫"]},
    "인천점":   {"traits":["공항 근접","20~40대","글로벌","여행객"],            "keywords":["글로벌","해외","여행","공항","트렌디","면세"]},
    "광복점":   {"traits":["부산 트렌드","20~40대","관광객","로컬"],            "keywords":["로컬","부산","관광","트렌드","스트릿"]},
    "노원점":   {"traits":["가족","30~50대","실용","지역 밀착"],               "keywords":["가족","실용","키즈","리빙","식품","생활"]},
    "미아점":   {"traits":["지역 상권","30~50대","생활 밀착","실용"],           "keywords":["실용","생활","가족","리빙","식품"]},
    "청량리점": {"traits":["재개발 수혜","30~50대","교통 요충지"],              "keywords":["실용","가족","리빙","교통","지역"]},
    "관악점":   {"traits":["대학가","20~40대","가성비","트렌드 민감"],          "keywords":["가성비","트렌드","젊은층","캐주얼","스트릿"]},
    "수원점":   {"traits":["경기 남부","25~45대","가족","실용"],               "keywords":["가족","실용","키즈","리빙","경기"]},
    "광주점":   {"traits":["호남 1위","25~45대","지역","식음료"],              "keywords":["로컬","광주","지역","식음료","패션"]},
    "대구점":   {"traits":["대구 상권","25~45대","패션 강세"],                 "keywords":["패션","대구","지역","트렌드","뷰티"]},
}

# ─────────────────────────────────────────────────────────────
# 기거래선 DB — 600개+
# ─────────────────────────────────────────────────────────────
EXISTING_BRANDS = list(dict.fromkeys([
    # 해외 명품
    "루이비통","샤넬","에르메스","구찌","프라다","버버리","발렌시아가","셀린느","디올","생로랑",
    "발렌티노","지방시","보테가베네타","페라가모","몽블랑","까르띠에","티파니","불가리","반클리프아펠",
    "롤렉스","오메가","태그호이어","IWC","파텍필립","브라이틀링","론진","라도","피아제",
    "바쉐론콘스탄틴","예거르쿨트르","파네라이","튜더","쇼파드","해리윈스턴","그라프","드비어스",
    "메종마르지엘라","아크네스튜디오","톰포드","알렉산더맥퀸","스텔라맥카트니","드리스반노튼",
    "마르니","질샌더","막스마라","발망","랑방","로에베","끌로에","이자벨마랑","자크뮈스",
    "아미파리","코레쥬","메종키츠네","아피씨","쿠레주",
    # 해외 컨템포러리
    "COS","아르켓","앤아더스토리즈","자라","마시모두띠","유니클로","GU","무인양품","H&M","망고",
    "폴로랄프로렌","타미힐피거","캘빈클라인","게스","라코스테","챔피온","컨버스","반스",
    "바나나리퍼블릭","갭","아베크롬비앤피치","홀리스터","아메리칸이글",
    # 해외 스포츠
    "나이키","아디다스","뉴발란스","살로몬","아크테릭스","노스페이스","파타고니아","콜롬비아",
    "캐나다구스","몽클레어","피크퍼포먼스","헬리한센","피레니스","아이스브레이커","스마트울",
    "몽벨","마모트","에코","메렐","킨","오스프리","그레고리","알트라","브룩스","아식스",
    "온러닝","호카","미즈노","스케쳐스","리복","K스위스","슈퍼가","DC슈즈",
    # 국내 패션
    "MLB","아더에러","앤더슨벨","우영미","지이크","갤럭시","닥스","헤지스","타임","마인",
    "시스템","꼼데가르송","이세이미야케","엠폴리오아르마니","마르지엘라","아크네","톰브라운",
    "쿠론","MCM","루이까또즈","메트로시티","빈폴","폴햄","지오다노","에잇세컨즈","스파오","탑텐",
    "커버낫","디스이즈네버댓","그라미치","로맨틱크라운","파스텔리","마하그리드","노이어",
    "하티스트","아뇨","BYC","쌍방울","트라이","원더플레이스","에스쁘리","나이스클랍","조이너스",
    "크로커다일","예작","까스텔바쟉","팬텀","볼빅","PGA투어","제이린드버그","핑","테일러메이드",
    "타이틀리스트","캘러웨이","클리블랜드","스릭슨","브리지스톤",
    # 해외 럭셔리 뷰티
    "샤넬뷰티","디올뷰티","입생로랑뷰티","조르지오아르마니뷰티","톰포드뷰티","겔랑",
    "랑콤","에스티로더","맥","클리니크","바비브라운","베네피트","어반디케이","스매쉬박스",
    "NARS","로라메르시에","메이크업포에버","샬롯틸버리","SK-II","시세이도","클레드포보테",
    "비오템","비쉬","라로쉐포제","세타필","아벤느","유리아쥬","이브로쉐",
    # 국내 뷰티
    "설화수","헤라","후","오휘","숨","에스트라","아모레퍼시픽","라네즈","마몽드","이니스프리",
    "에뛰드","에스쁘아","일리윤","려","미쟝센","해피바스","한율","아이오페",
    "CNP차앤박","닥터자르트","코스알엑스","AHC","JMsolution","메디힐","탬버린즈",
    "토니모리","네이처리퍼블릭","더페이스샵","스킨푸드","홀리카홀리카","벨리프","비욘드",
    "클리오","페리페라","롬앤","3CE","라카","듀이트리","닥터지","메디큐브","VT코스메틱",
    "구달","어뮤즈","글로우레시피",
    # 니치 향수
    "딥티크","조말론","르라보","바이레도","메종마르지엘라향수","로에베향수","킬리안","펜할리곤스",
    "세르주루텐스","아닉구딸","메모파리","오르몽드제인","크리드","프레데릭말","나르시소로드리게스",
    "이세이미야케향수","겐조향수","캐롤리나헤레라","아쿠아디파르마","불가리향수","에르메스향수",
    # 주얼리
    "판도라","스와로브스키","아가타","클루","미니골드","주얼리아","레이첼콕스","제이에스티나",
    "임프레션","디디에두보","에스쥬얼리","골든듀","스톤헨지","코이","케이크",
    "코치","마이클코어스","케이트스페이드","롱샴","토리버치","살바토레페라가모","멀버리",
    # 가전 / 테크
    "다이슨","발뮤다","드롱기","뱅앤올룹슨","브레빌","스메그","키친에이드","드비알렛",
    "보스","소노스","마샬","JBL","젠하이저","삼성","LG","애플","소니","파나소닉","샤프",
    "필립스","브라운","쿠쿠","쿠첸","위닉스","청호나이스","코웨이","바디프랜드","세라젬",
    "로보락","에코백스","드리미","아이로봇","네스프레소","일리","테팔","가민","핏빗","오라링",
    # 리빙 / 가구
    "데스커","일룸","리바트","에이스침대","시몬스","씰리","슬로우","이케아","자라홈","웨스트엘름",
    "포터리반","크레이트앤배럴","르크루제","스타우브","헤이","HAY","무토","앤트레디션",
    "하우스닥터","노만코펜하겐","까사미아","한샘","현대리바트","퍼시스","시디즈","에이스","템퍼",
    "허만밀러","놀","스틸케이스","카시나","비트라","마지스","카르텔",
    # F&B
    "스타벅스","투썸플레이스","폴바셋","블루보틀","% 아라비카","프릳츠","센터커피",
    "파리바게뜨","뚜레쥬르","아티제","베이크","르뱅쿠키","노티드","런던베이글뮤지엄",
    "배스킨라빈스","딥스","하겐다즈","젤라또피케","나뚜루",
    "버거킹","맥도날드","쉐이크쉑","파이브가이즈","웬디스","칼스주니어",
    "교촌","BBQ","페리카나","네네치킨","굽네치킨","BHC",
    "공차","더벤티","빽다방","메가커피","할리스","이디야","탐앤탐스","커피빈",
    # 스포츠 / 골프 / 아웃도어
    "레드페이스","블랙야크","케이투","밀레","네파","아이더","코오롱스포츠","라푸마","마운티아",
    "트렉스타","잭울프스킨","마무트","클라임X","알로요가","룰루레몬","젝시믹스","안다르",
    "뮬라웨어","스컬핏","뷰오리","휠라","엘레쎄","카파","엄브로","디아도라",
    "핑골프","PXG","카카오프렌즈골프","왁골프","잭버니","어노브",
    # 키즈
    "레고","플레이모빌","피셔프라이스","매텔","해즈브로","실바니안","리카","바비",
    "모이몰른","제리백","쁘띠바또","오이리","폴스미스키즈","버버리키즈","구찌키즈","아르마니키즈",
    "갭키즈","자라키즈","H&M키즈","유니클로키즈","나이키키즈","아디다스키즈",
    # 펫
    "어바웃펫","퍼피에이트","네츄럴발란스","오리젠","아카나","로얄캐닌","힐스",
    "플레이독","독워크","페오펫","멍냥공작소","강아지대통령","핏펫","먼슬리독",
    # 문구 / 서적
    "교보문고","영풍문고","알라딘","모닝글로리","알파","아트박스","몰스킨","파이로트",
    # 여행 / 가방
    "쌤소나이트","투미","리모와","만다리나덕","델세이","글로브트로터",
    # 언더웨어
    "비비안","비너스","캘빈클라인언더웨어","와코루","트라이앵글","신영",
    # 안경
    "젠틀몬스터","프로젝트프로덕트","레이밴","오클리","마우이짐","카레라","린드버그",
    # 엔터 / 영화관
    "CGV","메가박스","롯데시네마","CJ ENM","카카오엔터","하이브","SM엔터","YG엔터","JYP",
    "넷플릭스","디즈니플러스","티빙","왓챠","쿠팡플레이","애플TV",
    # 편의점 / 유통
    "CU","GS25","세븐일레븐","이마트24","올리브영","다이소","무신사","W컨셉","29CM",
]))

COMPETITOR_MARKERS = ["무신사","올리브영","현대백화점","신세계","갤러리아","AK플라자","롯데아울렛"]

# ─────────────────────────────────────────────────────────────
# 헬퍼
# ─────────────────────────────────────────────────────────────
def _naver_headers():
    return {"X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SEC}

def _clean(text: str) -> str:
    text = html.unescape(text or "")
    return re.sub(r"<[^>]+>", " ", text).strip()

# ─────────────────────────────────────────────────────────────
# API
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_naver_news(query: str, display: int = 20) -> list:
    if not NAVER_ID: return []
    try:
        r = requests.get("https://openapi.naver.com/v1/search/news.json",
                         headers=_naver_headers(),
                         params={"query": query, "display": display, "sort": "date"}, timeout=6)
        r.raise_for_status()
        return r.json().get("items", [])
    except: return []

@st.cache_data(ttl=300, show_spinner=False)
def fetch_naver_blog(query: str, display: int = 15) -> list:
    if not NAVER_ID: return []
    try:
        r = requests.get("https://openapi.naver.com/v1/search/blog.json",
                         headers=_naver_headers(),
                         params={"query": query, "display": display, "sort": "date"}, timeout=6)
        r.raise_for_status()
        return r.json().get("items", [])
    except: return []

@st.cache_data(ttl=600, show_spinner=False)
def fetch_naver_shopping_items(query: str, display: int = 5) -> list:
    if not NAVER_ID: return []
    try:
        r = requests.get("https://openapi.naver.com/v1/search/shop.json",
                         headers=_naver_headers(),
                         params={"query": query, "display": display, "sort": "sim"}, timeout=6)
        r.raise_for_status()
        return r.json().get("items", [])
    except: return []

@st.cache_data(ttl=600, show_spinner=False)
def fetch_naver_shopping_count(query: str) -> int:
    if not NAVER_ID: return 0
    try:
        r = requests.get("https://openapi.naver.com/v1/search/shop.json",
                         headers=_naver_headers(),
                         params={"query": query, "display": 1}, timeout=5)
        r.raise_for_status()
        return int(r.json().get("total", 0))
    except: return 0

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_trend(keyword: str) -> dict:
    try:
        pt = TrendReq(hl="ko-KR", tz=540, timeout=(10, 25))
        pt.build_payload([keyword], timeframe="today 3-m", geo="KR")
        df = pt.interest_over_time()
        if df.empty: return {"success": False, "data": [], "growth": 0}
        vals  = df[keyword].tolist()
        half  = len(vals) // 2
        early = sum(vals[:half]) / max(half, 1)
        late  = sum(vals[half:]) / max(len(vals)-half, 1)
        growth = ((late - early) / (early + 1)) * 100
        data = [{"period": str(d.date()), "ratio": v} for d, v in zip(df.index, vals)]
        return {"success": True, "data": data, "growth": round(growth, 1)}
    except:
        return {"success": False, "data": [], "growth": 0}

@st.cache_data(ttl=600, show_spinner=False)
def fetch_youtube_videos(keyword: str, max_results: int = 4) -> list:
    if not YOUTUBE_KEY: return []
    try:
        params = {
            "part": "snippet", "q": f"{keyword} 리뷰 후기",
            "type": "video", "order": "relevance",
            "publishedAfter": (datetime.utcnow()-timedelta(days=180)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "maxResults": max_results, "regionCode": "KR", "relevanceLanguage": "ko", "key": YOUTUBE_KEY,
        }
        r = requests.get("https://www.googleapis.com/youtube/v3/search", params=params, timeout=10)
        r.raise_for_status()
        result = []
        for item in r.json().get("items", []):
            vid_id  = item.get("id", {}).get("videoId", "")
            snippet = item.get("snippet", {})
            if vid_id:
                result.append({
                    "title":   snippet.get("title", "")[:50],
                    "channel": snippet.get("channelTitle", ""),
                    "url":     f"https://www.youtube.com/watch?v={vid_id}",
                    "thumb":   snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                    "date":    snippet.get("publishedAt", "")[:10],
                })
        return result
    except: return []

# ─────────────────────────────────────────────────────────────
# ★ 소스 1: 구글 트렌드 — 한국 실시간 급상승 검색어
#   pytrends trending_searches() 로 내가 모르는 키워드도 자동 포착
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=180, show_spinner=False)
def fetch_google_trending_kr() -> list:
    """구글 트렌드 한국 실시간 급상승 검색어 (상위 20개)"""
    try:
        pt = TrendReq(hl="ko-KR", tz=540, timeout=(10, 25))
        df = pt.trending_searches(pn="south_korea")
        keywords = df[0].tolist()[:20]
        return [str(k).strip() for k in keywords if str(k).strip()]
    except:
        return []

# ─────────────────────────────────────────────────────────────
# ★ 소스 2: 유튜브 — 한국 실시간 트렌딩 영상 제목 파싱
#   내가 모르는 밈/이슈가 유튜브에서 먼저 터지는 경우 포착
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=180, show_spinner=False)
def fetch_youtube_trending_kr() -> list:
    """유튜브 한국 트렌딩 — 음악/엔터 카테고리 제외, MD 관련 카테고리 중심"""
    if not YOUTUBE_KEY:
        return []
    # 제외할 카테고리 ID (음악=10, 엔터테인먼트=24)
    EXCLUDE_CATEGORIES = {"10", "24"}
    # 제목에 이게 포함되면 아이돌 콘텐츠로 간주해서 제외
    IDOL_NOISE = {
        "mv", "official", "lyrics", "lyric", "teaser", "performance",
        "dance", "fancam", "직캠", "뮤직비디오", "음악", "앨범", "컴백",
        "데뷔", "콘서트", "팬미팅", "쇼케이스", "live session",
    }
    try:
        r = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part":       "snippet",
                "chart":      "mostPopular",
                "regionCode": "KR",
                "maxResults": 50,   # 많이 가져와서 필터 후 선별
                "key":        YOUTUBE_KEY,
            },
            timeout=10,
        )
        r.raise_for_status()
        items = r.json().get("items", [])
        keywords = []
        for item in items:
            snippet     = item.get("snippet", {})
            category_id = snippet.get("categoryId", "")
            title       = snippet.get("title", "")
            title_clean = re.sub(r"<[^>]+>", "", html.unescape(title)).strip()
            title_lower = title_clean.lower()

            # 음악/엔터 카테고리 제외
            if category_id in EXCLUDE_CATEGORIES:
                continue
            # 아이돌 노이즈 키워드 포함 제외
            if any(n in title_lower for n in IDOL_NOISE):
                continue
            # 너무 짧거나 특수문자만인 것 제외
            if len(title_clean) < 3:
                continue

            keywords.append(title_clean[:40])

        return list(dict.fromkeys(keywords))[:15]
    except:
        return []

# ─────────────────────────────────────────────────────────────
# ★ 소스 3: 네이버 DataLab — 실시간 인기 검색어
#   (도메인 허용 후 동작)
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=180, show_spinner=False)
def fetch_naver_trending_kw() -> list:
    """네이버 DataLab 실시간 인기 검색어"""
    if not NAVER_ID:
        return []
    try:
        # DataLab 쇼핑 인사이트 — 분야별 인기 키워드
        end   = datetime.today().strftime("%Y-%m-%d")
        start = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        categories = [
            {"name":"패션의류", "param":[{"name":"패션의류","categoryId":"50000000"}]},
            {"name":"화장품미용", "param":[{"name":"화장품미용","categoryId":"50000002"}]},
            {"name":"식품", "param":[{"name":"식품","categoryId":"50000008"}]},
            {"name":"생활건강", "param":[{"name":"생활건강","categoryId":"50000006"}]},
        ]
        keywords = []
        for cat in categories:
            body = {
                "startDate":   start,
                "endDate":     end,
                "timeUnit":    "date",
                "category":    cat["param"],
                "keyword":     [{"name": cat["name"], "param": [cat["name"]]}],
                "device":      "",
                "ages":        [],
                "gender":      "",
            }
            r = requests.post(
                "https://openapi.naver.com/v1/datalab/shopping/categories",
                headers={**_naver_headers(), "Content-Type": "application/json"},
                data=json.dumps(body),
                timeout=8,
            )
            if r.status_code == 200:
                results = r.json().get("results", [])
                for res in results:
                    keywords.append(res.get("title", ""))
        return [k for k in keywords if k]
    except:
        return []

# ─────────────────────────────────────────────────────────────
# ★ 키워드 → 뉴스/블로그 본문 수집 → 트렌드 아이템 생성
# ─────────────────────────────────────────────────────────────
def keywords_to_trend_items(keywords: list, source: str) -> list:
    """실시간으로 잡힌 키워드/제목을 트렌드 아이템으로 변환"""
    items = []
    for kw in keywords[:15]:
        # HTML 완전 제거
        kw = re.sub(r"<[^>]+>", "", html.unescape(str(kw))).strip()
        if not kw or len(kw) < 2:
            continue

        news     = fetch_naver_news(kw, 5) if NAVER_ID else []
        blogs    = fetch_naver_blog(kw, 3) if NAVER_ID else []
        combined = news + blogs

        if combined:
            best  = combined[0]
            title = _clean(best.get("title", kw))
            desc  = _clean(best.get("description", ""))
            link  = best.get("link", "") or best.get("originallink", "")
            date  = (best.get("pubDate","") or best.get("postdate",""))[:16]
        else:
            title = kw
            desc  = f"{source}에서 화제 중"
            link  = ""
            date  = datetime.now().strftime("%Y-%m-%d")

        trend_type = classify_trend(title, desc)
        heat = random.randint(40, 70)
        if trend_type == "scarce": heat += 20
        if trend_type == "brand":  heat += 10
        boosters = ["대란","품귀","오픈런","바이럴","화제","한정판","매진"]
        heat += sum(5 for b in boosters if b in title)
        heat = min(heat, 99)

        items.append({
            "entity":      kw,         # 원본 제목/키워드 그대로
            "type":        trend_type,
            "title":       title,
            "desc":        desc[:100],
            "link":        link,
            "date":        date,
            "heat":        heat,
            "source":      source,
            "shop_count":  0,
            "is_fallback": False,
        })
    return items

# ─────────────────────────────────────────────────────────────
# ★ 메인 스캔 — 네이버 뉴스/블로그 메인, 유튜브 보조
# 폴백 제거 — 실제 데이터만 표시
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=180, show_spinner=False)
def run_trend_scan(custom_query: str = "") -> list:
    all_results: list[dict] = []
    seen_entities: set = set()

    seeds = TREND_SCAN_SEEDS.copy()
    if custom_query.strip():
        seeds = [custom_query.strip()] + seeds

    # ── 1순위: 네이버 뉴스+블로그 (메인) ─────────────────────
    if NAVER_ID:
        for seed in seeds[:25]:
            news  = fetch_naver_news(seed, 10)
            blogs = fetch_naver_blog(seed, 6)
            for raw in news + blogs:
                title = _clean(raw.get("title", ""))
                desc  = _clean(raw.get("description", ""))
                link  = raw.get("link", "") or raw.get("originallink", "")
                date  = (raw.get("pubDate","") or raw.get("postdate",""))[:16]
                if not title or len(title) < 4:
                    continue
                entity = extract_main_entity(title, desc)
                if not entity or entity in seen_entities or len(entity) < 2:
                    continue
                seen_entities.add(entity)
                trend_type = classify_trend(title, desc)
                heat = random.randint(30, 60)
                if trend_type == "scarce": heat += 30
                if trend_type == "brand":  heat += 15
                boosters = ["대란","품귀","오픈런","바이럴","화제","한정판","매진","품절","오픈","론칭"]
                heat += sum(5 for b in boosters if b in title)
                heat = min(heat, 99)
                all_results.append({
                    "entity":      entity,
                    "type":        trend_type,
                    "title":       title,
                    "desc":        desc[:100],
                    "link":        link,
                    "date":        date,
                    "heat":        heat,
                    "source":      "네이버",
                    "shop_count":  0,
                    "is_fallback": False,
                })
                if len(all_results) >= 60: break
            if len(all_results) >= 60: break

    # ── 2순위: 유튜브 트렌딩 (보조, 최대 5개) ────────────────
    if YOUTUBE_KEY:
        yt_added = 0
        for kw in fetch_youtube_trending_kr():
            if yt_added >= 5: break
            if kw in seen_entities: continue
            seen_entities.add(kw)
            all_results.append({
                "entity":      kw,
                "type":        classify_trend(kw, ""),
                "title":       kw,
                "desc":        "유튜브 트렌딩에서 포착",
                "link":        "",
                "date":        datetime.now().strftime("%Y-%m-%d"),
                "heat":        random.randint(30, 50),
                "source":      "유튜브",
                "shop_count":  0,
                "is_fallback": False,
            })
            yt_added += 1

    all_results.sort(key=lambda x: x["heat"], reverse=True)
    return all_results[:50]

# ─────────────────────────────────────────────────────────────
# 브랜드 심층 정보
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_brand_deep(keyword: str) -> dict:
    info = {
        "description":    "",
        "products":       [],
        "related_kws":    [],
        "related_queries":[],   # ★ 구글 연관 검색어 (트렌드 상세용)
        "blog_reviews":   [],
        "news_articles":  [],   # ★ 관련 뉴스 (트렌드 상세용)
        "youtube":        [],
        "shop_count":     0,
        "google_trend":   {"success":False,"data":[],"growth":0},
        "competitor":     False,
    }
    info["google_trend"] = fetch_google_trend(keyword)
    info["shop_count"]   = fetch_naver_shopping_count(keyword)
    info["youtube"]      = fetch_youtube_videos(keyword, 4)

    # ── 구글 연관 검색어 (pytrends related_queries) ───────────
    try:
        pt = TrendReq(hl="ko-KR", tz=540, timeout=(10, 25))
        pt.build_payload([keyword], timeframe="today 1-m", geo="KR")
        rq = pt.related_queries()
        if keyword in rq and rq[keyword].get("top") is not None:
            df_top = rq[keyword]["top"]
            if df_top is not None and not df_top.empty:
                info["related_queries"] = df_top["query"].tolist()[:10]
        if keyword in rq and rq[keyword].get("rising") is not None:
            df_rising = rq[keyword]["rising"]
            if df_rising is not None and not df_rising.empty:
                rising = df_rising["query"].tolist()[:5]
                info["related_queries"] = list(dict.fromkeys(
                    info["related_queries"] + rising
                ))[:12]
    except:
        pass

    if NAVER_ID:
        # 브랜드/트렌드 설명 (뉴스에서)
        news = fetch_naver_news(keyword, 8)
        for item in news[:3]:
            d = _clean(item.get("description",""))
            if len(d) > 30:
                info["description"] = d[:180] + ("..." if len(d)>180 else "")
                break

        # 관련 뉴스 (트렌드 상세용 — 최대 6개)
        for item in news[:6]:
            t  = _clean(item.get("title",""))
            l  = item.get("link","") or item.get("originallink","")
            dt = item.get("pubDate","")[:16]
            if t and l:
                info["news_articles"].append({"title": t[:55], "link": l, "date": dt})

        # 쇼핑 상품
        shop_items = fetch_naver_shopping_items(keyword, 6)
        seen_p = set()
        for item in shop_items:
            t = _clean(item.get("title",""))[:35]
            if t and t not in seen_p:
                seen_p.add(t)
                info["products"].append({
                    "title":    t,
                    "category": item.get("category2") or item.get("category1",""),
                    "price":    item.get("lprice",""),
                    "link":     item.get("link",""),
                })

        # 블로그 후기
        blogs = fetch_naver_blog(f"{keyword} 후기 사용기", 8)
        for item in blogs[:5]:
            t  = _clean(item.get("title",""))
            d  = _clean(item.get("description",""))
            l  = item.get("link","")
            dt = item.get("postdate","")
            if t and l:
                info["blog_reviews"].append({
                    "title": t[:45],
                    "desc":  d[:80]+"..." if len(d)>80 else d,
                    "link":  l,
                    "date":  f"{dt[:4]}.{dt[4:6]}.{dt[6:8]}" if len(dt)>=8 else dt,
                })

        # 연관 키워드 (블로그 제목 기반)
        kw_counter: Counter = Counter()
        for item in fetch_naver_blog(keyword, 20):
            for m in re.finditer(r"[가-힣A-Za-z]{2,8}", _clean(item.get("title",""))):
                t = m.group()
                if not is_noise(t) and t != keyword: kw_counter[t] += 1
        info["related_kws"] = [k for k,_ in kw_counter.most_common(12)]

        # 경쟁사 진출
        comp_news = fetch_naver_news(f"{keyword} 팝업", 8)
        info["competitor"] = any(
            any(c in (_clean(i.get("title",""))+_clean(i.get("description",""))) for c in COMPETITOR_MARKERS)
            for i in comp_news
        )
    return info

# ─────────────────────────────────────────────────────────────
# 점수 계산
# ─────────────────────────────────────────────────────────────
def compute_score(deep: dict, weights: dict) -> dict:
    gg  = deep["google_trend"]["growth"] if deep["google_trend"]["success"] else 0.0
    s_search  = min(max(gg / 80 * 100, 0), 100)
    s_youtube = 0.0
    s_blog    = min(len(deep["blog_reviews"]) / 5 * 100, 100)
    s_shop    = min(deep["shop_count"] / 10_000 * 100, 100)
    s_nocomp  = 20 if deep["competitor"] else 85
    total = (s_search*weights["search"] + s_youtube*weights["youtube"]
             + s_blog*weights["blog"] + s_shop*weights["shopping"] + s_nocomp*weights["nocomp"])
    return {
        "score": round(total, 1),
        "breakdown": {
            "검색량 증가":   round(s_search,1),
            "유튜브 반응":   round(s_youtube,1),
            "블로그 언급":   round(s_blog,1),
            "쇼핑 관심도":   round(s_shop,1),
            "경쟁사 미진출": round(s_nocomp,1),
        },
    }

def check_existing(keyword: str, db: list) -> bool:
    kw = keyword.lower().strip()
    return any(kw in b.lower() or b.lower() in kw for b in db)

def match_stores(keyword: str, extra: str = "") -> list:
    combined = (keyword + " " + extra).lower()
    scores = {}
    for store, profile in STORE_PROFILES.items():
        hits = sum(2 for kw in profile["keywords"] if kw.lower() in combined)
        scores[store] = min(55 + hits*8 + random.randint(-3,3), 97)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return [{"store":s,"match":sc,**STORE_PROFILES[s]} for s,sc in ranked]

# ─────────────────────────────────────────────────────────────
# Gmail
# ─────────────────────────────────────────────────────────────
def send_gmail(to_addr, subject, body):
    if not GMAIL_USER or not GMAIL_APP_PW:
        return False, "Gmail 계정 정보 미설정"
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = GMAIL_USER
        msg["To"]      = to_addr
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PW)
            server.sendmail(GMAIL_USER, to_addr, msg.as_string())
        return True, "메일이 발송되었습니다."
    except smtplib.SMTPAuthenticationError:
        return False, "Gmail 인증 실패 — 앱 비밀번호를 확인하세요."
    except Exception as e:
        return False, f"오류: {e}"

def proposal_draft(entity, score_info, stores, trend_title, deep):
    top  = stores[0]
    comp = "경쟁사 팝업 미진출 확인 — 선점 기회" if not deep["competitor"] else "경쟁사 일부 진출"
    gg   = deep["google_trend"]["growth"] if deep["google_trend"]["success"] else 0
    return f"""Subject: [{entity}] 팝업스토어 유치 제안 검토 요청

안녕하세요,
롯데백화점 MD본부 바이어입니다.

최근 실시간 트렌드 레이더를 통해 '{trend_title}' 관련 이슈를 포착하였으며,
귀 브랜드를 유력 팝업 후보로 발굴하여 연락드립니다.

━━━━━━━━━━━━━━━━━━━━━
트렌드 분석 요약
- 브랜드: {entity}
- 트렌드 점수: {score_info['score']:.0f} / 100
- 구글 트렌드 증가율: +{gg:.0f}%
- 쇼핑 관심: {deep['shop_count']:,}건
- 경쟁 현황: {comp}

━━━━━━━━━━━━━━━━━━━━━
추천 점포 (타겟 매칭 기반)
1순위: {top['store']} (매칭도 {top['match']}%)
   고객 특성: {' · '.join(top['traits'])}

━━━━━━━━━━━━━━━━━━━━━
제안 내용
- 형태: 단독 팝업스토어 (2~4주)
- 위치: {top['store']} 팝업 전용 공간
- 희망 시기: 협의 가능

미팅을 통해 구체적인 조건을 협의하고 싶습니다.
검토 후 회신 부탁드립니다.

감사합니다.
롯데백화점 MD본부 바이어
({datetime.now().strftime("%Y-%m-%d %H:%M")} 기준)""".strip()

# ─────────────────────────────────────────────────────────────
# UI 헬퍼
# ─────────────────────────────────────────────────────────────
def score_pill(s):
    cls = "score-high" if s>=65 else "score-mid" if s>=35 else "score-low"
    return f'<span class="score-pill {cls}">{s:.0f}점</span>'

def signal_bar(label, val, color="#1D9E75"):
    pct = int(val)
    st.markdown(f"""<div class="sig-row">
      <div class="sig-label">{label}</div>
      <div class="sig-bar-bg"><div style="width:{pct}%;background:{color};height:6px;border-radius:3px;"></div></div>
      <div class="sig-val">{pct}</div>
    </div>""", unsafe_allow_html=True)

def trend_chart(data):
    if not data: st.caption("트렌드 데이터 없음"); return
    df = pd.DataFrame(data)
    df["period"] = pd.to_datetime(df["period"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["period"], y=df["ratio"], mode="lines+markers",
        line=dict(color="#1D9E75", width=2.5), marker=dict(size=4),
        fill="tozeroy", fillcolor="rgba(29,158,117,0.08)",
        hovertemplate="%{x|%Y-%m-%d} %{y}<extra></extra>",
    ))
    fig.update_layout(height=160, margin=dict(l=0,r=0,t=4,b=0),
                      plot_bgcolor="white", paper_bgcolor="white",
                      yaxis=dict(range=[0,105], gridcolor="#f5f5f5"),
                      xaxis=dict(gridcolor="#f5f5f5"), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
def _init():
    defaults = {
        "view": "radar", "selected": None, "deep": None,
        "score_info": None, "stores": [], "proposal_txt": "",
        "existing_db": EXISTING_BRANDS.copy(),
        "custom_query": "", "scan_results": [], "last_scan": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()
S = st.session_state

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 분석 가중치")
    w_search   = st.slider("검색량 증가",   0.0,1.0,0.35,0.05)
    w_youtube  = st.slider("유튜브 반응",   0.0,1.0,0.20,0.05)
    w_blog     = st.slider("블로그 언급",   0.0,1.0,0.20,0.05)
    w_shopping = st.slider("쇼핑 관심도",   0.0,1.0,0.15,0.05)
    w_nocomp   = st.slider("경쟁사 미진출", 0.0,1.0,0.10,0.05)
    total_w    = round(w_search+w_youtube+w_blog+w_shopping+w_nocomp, 2)
    if abs(total_w-1.0) > 0.01:
        st.warning(f"합계 {total_w} — 1.0 맞춰주세요")
    else:
        st.success(f"합계 {total_w} ✓")
    weights = {"search":w_search,"youtube":w_youtube,"blog":w_blog,"shopping":w_shopping,"nocomp":w_nocomp}

    st.divider()
    st.markdown("### 기거래선 DB")
    st.caption(f"{len(S.existing_db)}개 등록")
    new_b = st.text_input("브랜드 추가", placeholder="예: 발뮤다")
    if st.button("추가") and new_b.strip():
        if new_b.strip() not in S.existing_db:
            S.existing_db.append(new_b.strip()); st.success("추가됨")
    with st.expander(f"목록 ({len(S.existing_db)}개)"):
        for idx, b in enumerate(S.existing_db):
            c1, c2 = st.columns([4,1])
            c1.caption(b)
            if c2.button("x", key=f"del_{idx}_{b}"):
                S.existing_db.remove(b); st.rerun()

    st.divider()
    st.caption(f"{'ON' if NAVER_ID else 'OFF'} — 네이버 API")
    st.caption(f"{'ON' if YOUTUBE_KEY else 'OFF'} — 유튜브 API")
    st.caption("ON — 구글 트렌드")
    st.caption(f"{'ON' if GMAIL_USER else 'OFF'} — Gmail")

# ─────────────────────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:16px'>
  <div style='display:flex;align-items:baseline;gap:12px'>
    <h2 style='font-size:1.6rem;font-weight:800;margin:0;color:#1a1a1a'>📡 트렌드 레이더</h2>
    <span style='font-size:12px;font-weight:700;color:#E84545;background:#fde8e8;
          padding:2px 10px;border-radius:4px;letter-spacing:.5px'>LIVE</span>
  </div>
  <p style='color:#888;font-size:13px;margin:4px 0 0'>
    밈 · 이슈 · 품귀 아이템을 실시간 감지 — 브랜드 연결 — 제안서 발송
  </p>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# VIEW: RADAR
# ─────────────────────────────────────────────────────────────
if S.view == "radar":

    search_col, btn_col = st.columns([5, 1])
    with search_col:
        custom_q = st.text_input(
            "검색",
            value=S.custom_query,
            placeholder="키워드 입력 (비워두면 전체 자동 스캔) — 예: 요시컵, SBTI테스트, 두바이초콜릿",
            label_visibility="collapsed",
        )
    with btn_col:
        scan_btn = st.button("스캔", type="primary", use_container_width=True)

    if scan_btn or not S.scan_results:
        S.custom_query = custom_q
        with st.spinner("실시간 스캔 중 — 구글 급상승 · 유튜브 트렌딩 · 네이버 뉴스 동시 수집 중..."):
            S.scan_results = run_trend_scan(custom_q)
            S.last_scan    = datetime.now().strftime("%H:%M:%S")

    if not S.scan_results:
        if not NAVER_ID:
            st.warning("네이버 API 키가 설정되지 않았습니다. secrets에 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET을 추가하세요.")
        else:
            st.info("스캔 버튼을 눌러주세요.")
    else:
        total    = len(S.scan_results)
        n_brand  = sum(1 for r in S.scan_results if r["type"]=="brand")
        n_scarce = sum(1 for r in S.scan_results if r["type"]=="scarce")
        n_issue  = sum(1 for r in S.scan_results if r["type"]=="issue")

        st.caption(
            f"스캔 완료 {S.last_scan}  —  "
            f"총 {total}건  |  브랜드 {n_brand}  |  품귀·한정 {n_scarce}  |  트렌드 {n_issue}"
        )

        # 필터 행
        fc = st.columns(4)
        with fc[0]: show_brand  = st.checkbox("브랜드", value=True)
        with fc[1]: show_scarce = st.checkbox("품귀·한정", value=True)
        with fc[2]: show_issue  = st.checkbox("트렌드·이슈", value=True)
        with fc[3]: show_top    = st.number_input("표시 수", 5, 50, 25, 5)

        filtered = [
            r for r in S.scan_results
            if (r["type"]=="brand"  and show_brand)
            or (r["type"]=="scarce" and show_scarce)
            or (r["type"]=="issue"  and show_issue)
        ][:int(show_top)]

        st.markdown("---")

        # 타입별 라벨 (이모지 없음, 텍스트 태그만)
        TYPE_LABEL = {"brand":"브랜드","scarce":"품귀·한정","issue":"트렌드"}
        TYPE_TAG   = {"brand":"type-brand","scarce":"type-scarce","issue":"type-issue"}
        HEAT_CLS   = lambda h: "heat-hi" if h>70 else "heat-mid" if h>40 else "heat-lo"

        for item in filtered:
            label    = TYPE_LABEL.get(item["type"], "이슈")
            tag_cls  = TYPE_TAG.get(item["type"], "type-issue")
            heat_cls = HEAT_CLS(item["heat"])
            is_ex    = check_existing(item["entity"], S.existing_db)
            card_cls = item["type"]  # 따옴표 충돌 방지용 변수

            ex_html  = '<span class="type-tag type-existing">기거래선</span>' if is_ex else ""
            src_html = f'<span style="font-size:10px;color:#aaa;margin-left:4px">{item.get("source","")}</span>'
            entity   = html.escape(item["entity"])
            desc     = html.escape(item["desc"])
            date     = item["date"]
            heat     = item["heat"]

            card = (
                f'<div class="trend-card {card_cls}">'
                f'<div style="display:flex;align-items:center;justify-content:space-between">'
                f'<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap">'
                f'<span class="type-tag {tag_cls}">{label}</span>'
                f'{ex_html}'
                f'<span style="font-size:15px;font-weight:700;color:#1a1a1a">{entity}</span>'
                f'{src_html}'
                f'</div>'
                f'<span class="heat-num {heat_cls}">Heat {heat}</span>'
                f'</div>'
                f'<div style="font-size:12px;color:#666;margin-top:6px;line-height:1.6">{desc}</div>'
                f'<div style="font-size:11px;color:#aaa;margin-top:4px">{date}</div>'
                f'</div>'
            )
            st.markdown(card, unsafe_allow_html=True)

            if item["type"] in ("brand", "scarce"):
                if st.button(
                    f"상세 분석 →  {item['entity']}",
                    key=f"btn_{item['entity']}_{item['heat']}",
                    use_container_width=False,
                ):
                    S.selected   = item
                    S.deep       = None
                    S.score_info = None
                    S.stores     = []
                    S.view       = "detail"
                    st.rerun()
            else:
                # 트렌드/이슈도 상세보기 버튼 추가
                if st.button(
                    f"트렌드 상세 보기 →  {item['entity']}",
                    key=f"btn_{item['entity']}_{item['heat']}",
                    use_container_width=False,
                ):
                    S.selected   = item
                    S.deep       = None
                    S.score_info = None
                    S.stores     = []
                    S.view       = "detail"
                    st.rerun()

            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# VIEW: DETAIL
# ─────────────────────────────────────────────────────────────
elif S.view == "detail":
    item = S.selected
    if not item:
        S.view = "radar"; st.rerun()

    if st.button("← 레이더로"):
        S.view = "radar"; st.rerun()

    TYPE_LABEL = {"brand":"브랜드","scarce":"품귀·한정 아이템","issue":"트렌드·이슈"}
    is_trend   = item["type"] == "issue"
    is_scarce  = item["type"] == "scarce"
    is_brand   = item["type"] == "brand"

    st.markdown(f"## {item['entity']}")
    st.caption(
        f"{TYPE_LABEL.get(item['type'],'?')}  —  "
        f"Heat {item['heat']}  —  {item['date']}  —  출처: {item.get('source','')}"
    )
    if item.get("link"):
        st.markdown(f"[원문 보기 →]({item['link']})")

    st.divider()

    # 데이터 수집
    if S.deep is None:
        with st.spinner(f"'{item['entity']}' 정보 수집 중..."):
            S.deep       = fetch_brand_deep(item["entity"])
            S.score_info = compute_score(S.deep, weights)
            S.stores     = match_stores(item["entity"], item.get("desc",""))

    deep       = S.deep
    score_info = S.score_info

    # ════════════════════════════════════════════════
    # 트렌드·이슈 전용 상세 뷰
    # ════════════════════════════════════════════════
    if is_trend:
        st.markdown("### 이 트렌드는 무엇인가요?")

        # 개요 설명
        if deep["description"]:
            st.markdown(
                f'<div class="binfo-card">'
                f'<div style="font-size:11px;font-weight:700;color:#888;margin-bottom:6px">트렌드 개요</div>'
                f'<div style="font-size:13px;color:#333;line-height:1.8">{html.escape(deep["description"])}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.info(f"**{item['entity']}** — {item['desc']}")

        col1, col2 = st.columns(2)

        with col1:
            # 구글 연관 검색어
            if deep["related_queries"]:
                st.markdown("**함께 검색되는 키워드**")
                kw_html = "<div style='margin:6px 0 14px'>"
                for q in deep["related_queries"]:
                    kw_html += (
                        f'<span style="display:inline-block;padding:4px 12px;margin:3px;'
                        f'background:#f0f4ff;border:1px solid #c5d3f5;border-radius:6px;'
                        f'font-size:12px;color:#2D5BE3;cursor:pointer">{html.escape(q)}</span>'
                    )
                kw_html += "</div>"
                st.markdown(kw_html, unsafe_allow_html=True)
            else:
                st.caption("구글 연관 검색어: 수집 중이거나 데이터 없음")

            # 블로그 언급
            if deep["blog_reviews"]:
                st.markdown("**블로그 언급**")
                for b in deep["blog_reviews"][:4]:
                    st.markdown(
                        f"- [{b['title']}]({b['link']})  \n"
                        f"  <span style='font-size:11px;color:#888'>{b['date']}</span>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("블로그: 네이버 API 도메인 허용 후 표시")

        with col2:
            # 관련 뉴스
            if deep["news_articles"]:
                st.markdown("**관련 뉴스**")
                for a in deep["news_articles"][:6]:
                    st.markdown(
                        f"- [{a['title']}]({a['link']})  \n"
                        f"  <span style='font-size:11px;color:#888'>{a['date']}</span>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("뉴스: 네이버 API 도메인 허용 후 표시")

        # 구글 트렌드 차트
        st.markdown("**구글 트렌드 (최근 1개월)**")
        trend_chart(deep["google_trend"].get("data", []))
        gg = deep["google_trend"]["growth"] if deep["google_trend"]["success"] else 0
        st.caption(f"구글 검색량 변화: +{gg:.0f}%")

        # 유튜브
        if deep["youtube"]:
            st.markdown("**관련 유튜브 영상**")
            yt_cols = st.columns(min(4, len(deep["youtube"])))
            for col, vid in zip(yt_cols, deep["youtube"][:4]):
                with col:
                    if vid.get("thumb"):
                        st.markdown(
                            f'<a href="{vid["url"]}" target="_blank">'
                            f'<img src="{vid["thumb"]}" style="width:100%;border-radius:6px;margin-bottom:4px"/></a>',
                            unsafe_allow_html=True,
                        )
                    st.markdown(
                        f'<a href="{vid["url"]}" target="_blank" style="font-size:12px;font-weight:600;'
                        f'color:#1a1a1a;text-decoration:none">{vid["title"][:35]}{"..." if len(vid["title"])>35 else ""}</a>'
                        f'<br><span style="font-size:11px;color:#888">{vid["channel"]} · {vid["date"]}</span>',
                        unsafe_allow_html=True,
                    )

        st.divider()

        # ── 브랜드 연결 섹션 ────────────────────────────────
        st.markdown("### 이 트렌드, 어떤 브랜드와 연결할 수 있을까요?")

        # 연관 키워드로 브랜드 후보 제안
        brand_candidates = []
        search_kws = deep["related_queries"][:5] + [item["entity"]]
        for kw in search_kws:
            # 기거래선 DB에서 매칭
            matches = [b for b in S.existing_db if kw.lower() in b.lower() or b.lower() in kw.lower()]
            brand_candidates.extend(matches)
        brand_candidates = list(dict.fromkeys(brand_candidates))[:8]

        if brand_candidates:
            st.markdown("**기거래선 중 연관 브랜드**")
            bc_html = "<div style='margin:6px 0 14px'>"
            for b in brand_candidates:
                bc_html += (
                    f'<span style="display:inline-block;padding:5px 14px;margin:3px;'
                    f'background:#fff3e5;border:1px solid #f0c080;border-radius:6px;'
                    f'font-size:13px;font-weight:600;color:#854F0B">{b}</span>'
                )
            bc_html += "</div>"
            st.markdown(bc_html, unsafe_allow_html=True)

        # 직접 브랜드 입력해서 연결
        st.markdown("**이 트렌드에 맞는 브랜드 직접 입력**")
        linked_brand = st.text_input(
            "브랜드명 입력",
            placeholder=f"예: {item['entity']} 관련 브랜드명",
            label_visibility="collapsed",
            key="trend_brand_input",
        )
        if linked_brand.strip():
            st.info(f"선택: **{linked_brand.strip()}** — 이 브랜드로 분석을 이어갑니다.")

        col_a, col_b = st.columns(2)
        with col_a:
            go_brand = st.button(
                "이 트렌드로 브랜드 분석하기",
                type="primary",
                disabled=not linked_brand.strip(),
                use_container_width=True,
            )
            if go_brand and linked_brand.strip():
                # 트렌드 아이템을 브랜드 아이템으로 변환해서 detail로
                S.selected = {
                    **item,
                    "entity": linked_brand.strip(),
                    "type":   "brand",
                }
                S.deep       = None
                S.score_info = None
                S.stores     = []
                st.rerun()
        with col_b:
            if brand_candidates:
                pick = st.selectbox(
                    "기거래선에서 선택",
                    ["선택하세요"] + brand_candidates,
                    label_visibility="collapsed",
                )
                if pick != "선택하세요":
                    if st.button(f"{pick} 분석하기", use_container_width=True):
                        S.selected = {**item, "entity": pick, "type": "brand"}
                        S.deep       = None
                        S.score_info = None
                        S.stores     = []
                        st.rerun()

    # ════════════════════════════════════════════════
    # 브랜드 / 품귀 아이템 상세 뷰
    # ════════════════════════════════════════════════
    else:
        if deep["description"]:
            st.markdown(
                f'<div class="binfo-card">'
                f'<div style="font-size:11px;font-weight:700;color:#888;margin-bottom:4px">브랜드 소개</div>'
                f'<div style="font-size:13px;color:#333;line-height:1.7">{html.escape(deep["description"])}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        col_l, col_r = st.columns(2)
        with col_l:
            if deep["products"]:
                st.markdown("**주요 상품**")
                for p in deep["products"][:4]:
                    price_str = f"  ₩{int(p['price']):,}" if str(p.get("price","")).isdigit() else ""
                    cat_str   = f"  `{p['category']}`" if p.get("category") else ""
                    st.markdown(f"- [{p['title']}]({p['link']}){cat_str}{price_str}")
            else:
                st.caption("네이버 API 연결 시 상품 정보 표시됩니다.")

            if deep["related_kws"]:
                st.markdown("**연관 키워드**")
                kw_html = "<div style='margin:4px 0 12px'>" + "".join(
                    f'<span style="display:inline-block;padding:3px 10px;margin:3px;'
                    f'background:#f0f0f0;border-radius:4px;font-size:12px;color:#444">#{kw}</span>'
                    for kw in deep["related_kws"]
                ) + "</div>"
                st.markdown(kw_html, unsafe_allow_html=True)

            if deep["related_queries"]:
                st.markdown("**구글 함께 검색된 키워드**")
                rq_html = "<div style='margin:4px 0 12px'>" + "".join(
                    f'<span style="display:inline-block;padding:3px 10px;margin:3px;'
                    f'background:#f0f4ff;border:1px solid #c5d3f5;border-radius:4px;font-size:12px;color:#2D5BE3">{html.escape(q)}</span>'
                    for q in deep["related_queries"]
                ) + "</div>"
                st.markdown(rq_html, unsafe_allow_html=True)

        with col_r:
            if deep["blog_reviews"]:
                st.markdown("**네이버 블로그 후기**")
                for b in deep["blog_reviews"][:4]:
                    st.markdown(
                        f"- [{b['title']}]({b['link']})  \n"
                        f"  <span style='font-size:11px;color:#888'>{b['date']} · {b['desc']}</span>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("네이버 API 연결 시 블로그 후기 표시됩니다.")

            if deep["news_articles"]:
                st.markdown("**관련 뉴스**")
                for a in deep["news_articles"][:4]:
                    st.markdown(
                        f"- [{a['title']}]({a['link']})  \n"
                        f"  <span style='font-size:11px;color:#888'>{a['date']}</span>",
                        unsafe_allow_html=True,
                    )

        if deep["youtube"]:
            st.markdown("**유튜브 리뷰**")
            yt_cols = st.columns(min(4, len(deep["youtube"])))
            for col, vid in zip(yt_cols, deep["youtube"][:4]):
                with col:
                    if vid.get("thumb"):
                        st.markdown(
                            f'<a href="{vid["url"]}" target="_blank">'
                            f'<img src="{vid["thumb"]}" style="width:100%;border-radius:6px;margin-bottom:4px"/></a>',
                            unsafe_allow_html=True,
                        )
                    st.markdown(
                        f'<a href="{vid["url"]}" target="_blank" style="font-size:12px;font-weight:600;'
                        f'color:#1a1a1a;text-decoration:none">{vid["title"][:35]}{"..." if len(vid["title"])>35 else ""}</a>'
                        f'<br><span style="font-size:11px;color:#888">{vid["channel"]} · {vid["date"]}</span>',
                        unsafe_allow_html=True,
                    )
        else:
            st.caption("YOUTUBE_API_KEY 설정 시 리뷰 영상이 표시됩니다.")

        st.divider()
        st.markdown("### 트렌드 점수")

        b0,b1,b2,b3 = st.columns(4)
        with b0:
            st.markdown(score_pill(score_info["score"]), unsafe_allow_html=True)
            st.caption("트렌드 점수")
        with b1:
            is_ex = check_existing(item["entity"], S.existing_db)
            st.markdown(f'<span class="{"verify-warn" if is_ex else "verify-ok"}">{"기거래선" if is_ex else "신규 브랜드"}</span>', unsafe_allow_html=True)
            st.caption("거래선 상태")
        with b2:
            comp = deep["competitor"]
            st.markdown(f'<span class="{"verify-warn" if comp else "verify-ok"}">{"경쟁사 진출" if comp else "선점 가능"}</span>', unsafe_allow_html=True)
            st.caption("경쟁사 현황")
        with b3:
            sk = deep["shop_count"]
            st.markdown(f'<span class="verify-info">{f"{sk:,}건" if sk else "—"}</span>', unsafe_allow_html=True)
            st.caption("쇼핑 관심도")

        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("**신호별 점수**")
            colors = {"검색량 증가":"#1D9E75","유튜브 반응":"#185FA5","블로그 언급":"#888","쇼핑 관심도":"#BA7517","경쟁사 미진출":"#0F6E56"}
            for k, v in score_info["breakdown"].items():
                signal_bar(k, v, colors.get(k,"#1D9E75"))
        with sc2:
            st.markdown("**구글 트렌드 (12주)**")
            trend_chart(deep["google_trend"].get("data",[]))
            gg = deep["google_trend"]["growth"] if deep["google_trend"]["success"] else 0
            st.caption(f"구글 +{gg:.0f}%")

        st.divider()
        st.markdown("### 추천 점포")
        for i, (col, store) in enumerate(zip(st.columns(3), S.stores)):
            with col:
                rank = ["1순위","2순위","3순위"][i]
                st.markdown(
                    f'<div class="store-card">'
                    f'<div style="font-size:11px;font-weight:700;color:#888">{rank}</div>'
                    f'<div class="store-name">{store["store"]}</div>'
                    f'<div class="store-match">{store["match"]}%</div>'
                    f'<div class="store-traits">{"<br>".join(store["traits"])}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        override = st.selectbox("점포 직접 변경", ["추천 1순위 유지"]+list(STORE_PROFILES.keys()))
        if override != "추천 1순위 유지":
            S.stores[0] = {"store":override,"match":0,**STORE_PROFILES[override]}

        st.divider()
        if st.button("제안서 작성", type="primary", use_container_width=True):
            S.proposal_txt = proposal_draft(item["entity"], score_info, S.stores, item["title"], deep)
            S.view = "proposal"
            st.rerun()


# ─────────────────────────────────────────────────────────────
# VIEW: PROPOSAL
# ─────────────────────────────────────────────────────────────
elif S.view == "proposal":
    item = S.selected

    if st.button("← 분석으로"):
        S.view = "detail"; st.rerun()

    brand_name = item["entity"] if item else ""
    st.markdown(f"### 제안서 — {brand_name}")

    edited  = st.text_area("초안 (직접 수정 가능)", S.proposal_txt, height=400)
    subject = edited.split("\n")[0].replace("Subject: ","").strip() if edited else "팝업스토어 유치 제안"

    st.markdown("---")
    to_email = st.text_input("수신 이메일", placeholder="brand@example.com")

    c1, c2 = st.columns(2)
    with c1:
        disabled = not (to_email and GMAIL_USER and GMAIL_APP_PW)
        if st.button("Gmail로 발송", type="primary", disabled=disabled, use_container_width=True):
            with st.spinner("발송 중..."):
                lines = edited.split("\n")
                body  = "\n".join(lines[1:]).strip() if lines[0].startswith("Subject:") else edited
                ok, msg = send_gmail(to_email, subject, body)
            if ok: st.success(msg); st.balloons()
            else:  st.error(msg)
        if not GMAIL_USER:
            st.caption("secrets에 GMAIL_USER / GMAIL_APP_PASSWORD 추가 필요")
    with c2:
        st.download_button(
            "텍스트 다운로드", edited,
            file_name=f"제안서_{brand_name}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain", use_container_width=True,
        )

    st.divider()
    if st.button("레이더로 돌아가기", use_container_width=True):
        S.view = "radar"; st.rerun()
