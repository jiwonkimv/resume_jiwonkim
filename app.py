import streamlit as st
import base64, os

st.set_page_config(
    page_title="Jiwon Kim — Portfolio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 사진 로드 ──────────────────────────────────────────────
PHOTO_B64 = ""
photo_paths = [
    "photo.jpg",
    os.path.join(os.path.dirname(__file__), "photo.jpg"),
]
for p in photo_paths:
    if os.path.exists(p):
        with open(p, "rb") as f:
            PHOTO_B64 = base64.b64encode(f.read()).decode()
        break

PHOTO_HTML = (
    f'<img src="data:image/jpeg;base64,{PHOTO_B64}" class="hero-photo" />'
    if PHOTO_B64 else ""
)

st.markdown(f"""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/variable/pretendardvariable.css');

/* ── 리셋 & 기본 ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body, [class*="css"], .stApp {{
    font-family: 'Pretendard Variable', 'Pretendard', -apple-system, sans-serif !important;
    background: #F8F9FB !important;
    color: #111827;
}}
.main {{ background: #F8F9FB !important; }}
.main > div {{ padding: 0 !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
section[data-testid="stSidebar"] {{ display: none; }}
[data-testid="stHeader"] {{ display: none; }}
[data-testid="stDecoration"] {{ display: none; }}

/* ── 색 변수 (3색만) ──
   #0A2540  딥 네이비 (메인 텍스트 / 배경)
   #0F6FFF  블루 (포인트 / 강조)
   #FFFFFF  화이트
   보조: #F8F9FB 배경, #6B7280 회색 텍스트, #E5E7EB 경계선
── */

/* ── HERO ── */
.hero {{
    background: #0A2540;
    padding: 56px 9% 60px;
    display: flex;
    align-items: center;
    gap: 48px;
}}
.hero-photo {{
    width: 130px;
    height: 160px;
    object-fit: cover;
    object-position: top;
    border-radius: 12px;
    border: 3px solid rgba(255,255,255,0.15);
    flex-shrink: 0;
}}
.hero-body {{ flex: 1; }}
.hero-eyebrow {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #0F6FFF;
    margin-bottom: 10px;
}}
.hero-name {{
    font-size: clamp(36px, 5vw, 58px);
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 8px;
}}
.hero-title {{
    font-size: 15px;
    font-weight: 400;
    color: rgba(255,255,255,0.55);
    margin-bottom: 28px;
    line-height: 1.6;
}}
.hero-contacts {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 28px;
}}
.hero-contact {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 500;
    color: rgba(255,255,255,0.75) !important;
    text-decoration: none !important;
    transition: background .15s;
}}
.hero-contact:hover {{
    background: rgba(255,255,255,0.12);
    color: #fff !important;
}}
/* 공유 링크 — 눈에 띄게 */
.share-btn {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0F6FFF;
    border-radius: 8px;
    padding: 7px 16px;
    font-size: 12px;
    font-weight: 700;
    color: #FFFFFF !important;
    text-decoration: none !important;
    letter-spacing: 0.2px;
    transition: background .15s;
}}
.share-btn:hover {{ background: #0058e0; }}
.hero-stats {{
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.1);
}}
.stat-num {{
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1;
}}
.stat-label {{
    font-size: 11px;
    color: rgba(255,255,255,0.4);
    margin-top: 3px;
    font-weight: 500;
    letter-spacing: 0.3px;
}}

/* ── 탭 — 크고 명확하게 ── */
div[data-baseweb="tab-list"] {{
    background: #FFFFFF !important;
    border-bottom: 1.5px solid #E5E7EB !important;
    padding: 0 9% !important;
    gap: 0 !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06) !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
}}
div[data-baseweb="tab"] {{
    font-family: 'Pretendard Variable','Pretendard',sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #9CA3AF !important;
    padding: 18px 28px !important;
    letter-spacing: -0.2px !important;
    border-bottom: 2.5px solid transparent !important;
    margin-bottom: -1.5px !important;
}}
div[aria-selected="true"] {{
    color: #0A2540 !important;
    border-bottom-color: #0F6FFF !important;
    font-weight: 700 !important;
}}
div[data-baseweb="tab"]:hover {{
    color: #0A2540 !important;
}}

/* ── 섹션 래퍼 ── */
.section {{ padding: 56px 9%; }}
.section-alt {{ background: #FFFFFF; }}

/* ── 공통 레이블 ── */
.sec-label {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #0F6FFF;
    margin-bottom: 6px;
}}
.sec-title {{
    font-size: clamp(22px, 3vw, 32px);
    font-weight: 800;
    color: #0A2540;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 6px;
}}
.sec-desc {{
    font-size: 14px;
    color: #6B7280;
    line-height: 1.75;
    max-width: 620px;
    margin-bottom: 36px;
}}

/* ── 프로필 텍스트 ── */
.profile-text {{ font-size: 15px; line-height: 1.85; color: #374151; max-width: 760px; }}
.profile-text strong {{ color: #0A2540; font-weight: 700; }}

/* ── KPI 카드 ── */
.kpi-row {{ display: flex; gap: 16px; flex-wrap: wrap; margin-top: 32px; }}
.kpi-card {{
    flex: 1;
    min-width: 180px;
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 14px;
    padding: 22px 24px;
    border-top: 3px solid #0F6FFF;
}}
.kpi-num {{
    font-size: 32px;
    font-weight: 800;
    color: #0A2540;
    line-height: 1;
    margin-bottom: 6px;
}}
.kpi-desc {{ font-size: 13px; color: #6B7280; line-height: 1.5; font-weight: 500; }}

/* ── 경험 타임라인 ── */
.tl-wrap {{ position: relative; padding-left: 20px; }}
.tl-wrap::before {{
    content: '';
    position: absolute;
    left: 0; top: 12px; bottom: 12px;
    width: 2px;
    background: linear-gradient(180deg, #0F6FFF 0%, #E5E7EB 100%);
    border-radius: 1px;
}}
.tl-card {{
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 16px;
    padding: 28px 30px;
    margin-bottom: 16px;
    position: relative;
}}
.tl-card::before {{
    content: '';
    position: absolute;
    left: -27px; top: 24px;
    width: 14px; height: 14px;
    border-radius: 50%;
    background: #0F6FFF;
    border: 3px solid #F8F9FB;
    box-shadow: 0 0 0 1.5px #0F6FFF;
}}
.tl-role {{
    font-size: 17px;
    font-weight: 700;
    color: #0A2540;
    margin-bottom: 2px;
}}
.tl-company {{
    font-size: 13px;
    font-weight: 600;
    color: #0F6FFF;
    margin-bottom: 3px;
}}
.tl-period {{
    font-size: 11px;
    font-weight: 500;
    color: #9CA3AF;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}}
.tl-scope {{
    font-size: 12px;
    color: #6B7280;
    background: #F8F9FB;
    border-radius: 8px;
    padding: 8px 14px;
    margin-bottom: 16px;
    font-weight: 500;
    line-height: 1.6;
}}
.sub-label {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #0F6FFF;
    margin: 18px 0 10px;
}}
.bul {{
    font-size: 13.5px;
    color: #374151;
    line-height: 1.75;
    padding-left: 16px;
    position: relative;
    margin-bottom: 8px;
}}
.bul::before {{
    content: '—';
    position: absolute;
    left: 0;
    color: #0F6FFF;
    font-size: 11px;
    font-weight: 700;
    top: 3px;
}}
.bul b {{ color: #0A2540; font-weight: 700; }}
.badges {{
    display: flex; flex-wrap: wrap;
    gap: 6px; margin: 8px 0 2px;
}}
.badge {{
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
    color: #1D4ED8;
}}

/* ── 프로젝트 카드 ── */
.proj-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.proj-card {{
    background: #0A2540;
    border-radius: 16px;
    padding: 28px;
    position: relative;
    overflow: hidden;
}}
.proj-card::after {{
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: rgba(15,111,255,0.12);
}}
.proj-no {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
    margin-bottom: 10px;
}}
.proj-title {{
    font-size: 17px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.3;
    margin-bottom: 6px;
}}
.proj-sub {{
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    margin-bottom: 14px;
    font-weight: 500;
}}
.proj-badges {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }}
.proj-badge {{
    background: rgba(15,111,255,0.25);
    border: 1px solid rgba(15,111,255,0.4);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
    color: #93C5FD;
}}
.proj-bul {{
    font-size: 13px;
    color: rgba(255,255,255,0.7);
    line-height: 1.7;
    padding-left: 14px;
    position: relative;
    margin-bottom: 7px;
}}
.proj-bul::before {{
    content: '→';
    position: absolute;
    left: 0;
    color: #0F6FFF;
    font-size: 11px;
    top: 2px;
}}
.proj-bul b {{ color: #FFFFFF; }}

/* ── 스킬 ── */
.skill-block {{
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 12px;
}}
.skill-title {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #0A2540;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.skill-title::before {{
    content: '';
    width: 4px; height: 4px;
    border-radius: 50%;
    background: #0F6FFF;
}}
.skill-tags {{ display: flex; flex-wrap: wrap; gap: 7px; }}
.skill-tag {{
    background: #F8F9FB;
    border: 1px solid #E5E7EB;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
    color: #374151;
}}

/* ── 학력 ── */
.edu-card {{
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    gap: 18px;
}}
.edu-icon {{
    width: 44px; height: 44px;
    border-radius: 10px;
    background: #0A2540;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}}
.edu-degree {{ font-size: 16px; font-weight: 700; color: #0A2540; margin-bottom: 2px; }}
.edu-school {{ font-size: 12px; font-weight: 600; color: #0F6FFF; margin-bottom: 3px; }}
.edu-period {{ font-size: 11px; color: #9CA3AF; letter-spacing: 0.5px; font-weight: 500; margin-bottom: 10px; }}

/* ── 푸터 ── */
.footer {{
    background: #0A2540;
    padding: 40px 9%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}}
.footer-name {{ font-size: 18px; font-weight: 800; color: #FFFFFF; }}
.footer-sub {{ font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 2px; }}
.footer-links {{ display: flex; gap: 20px; align-items: center; }}
.footer-link {{
    font-size: 12px; font-weight: 600;
    color: rgba(255,255,255,0.5); text-decoration: none;
}}
.footer-link:hover {{ color: #FFFFFF; }}

div[data-testid="stMarkdownContainer"] p {{ margin: 0; }}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
linkedin = "https://linkedin.com/in/jiwon-kim-673244226"
st.markdown(f"""
<div class="hero">
  {PHOTO_HTML}
  <div class="hero-body">
    <div class="hero-eyebrow">◈ Portfolio · South Korea</div>
    <div class="hero-name">Jiwon Kim</div>
    <div class="hero-title">
      Retail Buyer &amp; Brand Activator &nbsp;·&nbsp;
      Lotte Department Store HQ &nbsp;·&nbsp;
      $350M+ GMV Managed
    </div>
    <div class="hero-contacts">
      <a class="hero-contact" href="tel:+821026573623">📞 (+82) 10-2657-3623</a>
      <a class="hero-contact" href="mailto:jiwonkimv@gmail.com">✉ jiwonkimv@gmail.com</a>
      <a class="hero-contact" href="{linkedin}" target="_blank">in LinkedIn</a>
      <a class="share-btn" href="{linkedin}" target="_blank">🔗 Share Profile</a>
    </div>
    <div class="hero-stats">
      <div><div class="stat-num">5+</div><div class="stat-label">Years</div></div>
      <div><div class="stat-num">$350M+</div><div class="stat-label">GMV Managed</div></div>
      <div><div class="stat-num">160+</div><div class="stat-label">Brands</div></div>
      <div><div class="stat-num">55+</div><div class="stat-label">Locations</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
t_about, t_exp, t_projects, t_skills, t_edu = st.tabs([
    "About", "Experience", "Key Projects", "Skills", "Education"
])

# ── ABOUT ─────────────────────────────────────────────────────
with t_about:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Commercial Retail Buyer<br>with a Track Record of Activation</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="profile-text">
      Commercial retail buyer with <strong>5+ years</strong> of P&amp;L ownership across department store
      and outlet channels. Managed a multi-category portfolio of <strong>₩460B+ ($350M+)</strong>
      spanning 55+ locations and 160+ brands.<br><br>
      Track record of vendor negotiation, margin restructuring, pop-up activation, and turning
      underperforming assets into profit contributors.
      Led high-impact traffic activations with national media reach — including
      <strong>Korea's first Asahi Super Dry retail activation</strong> ($120K in 14 days, 13 press features)
      and the <strong>first premium built-in kitchen zone</strong> in a Korean department store.<br><br>
      Experienced in Joint Business Planning, influencer-linked commerce, IP retail programs,
      and cross-functional collaboration with Marketing, Finance, and Supply Chain.
      Strong analytical foundation via 5+ years of advanced Excel (Pivot, Scenario Analysis, financial modeling).
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class="kpi-card">
          <div class="kpi-num">$4M</div>
          <div class="kpi-desc">Single campaign GMV<br>111% of target · +12.1% YoY</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-card">
          <div class="kpi-num">+23%</div>
          <div class="kpi-desc">Hi-mart rental increase<br>5-year stalled negotiation closed</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kpi-card">
          <div class="kpi-num">+30%</div>
          <div class="kpi-desc">Daily views at Naver<br>Data-driven content curation</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="kpi-card">
          <div class="kpi-num">13</div>
          <div class="kpi-desc">Press features<br>Zero paid media spend</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── EXPERIENCE ────────────────────────────────────────────────
with t_exp:
    st.markdown('<div class="section section-alt">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Career</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Experience</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-desc">5+ years across department store and outlet buying, brand activation, and CE retail operations.</div>', unsafe_allow_html=True)

    st.markdown('<div class="tl-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div class="tl-card">
      <div class="tl-role">Buyer, Consumer Electronics (GL)</div>
      <div class="tl-company">Lotte Department Store HQ</div>
      <div class="tl-period">AUG 2025 – PRESENT</div>
      <div class="tl-scope">$190M+ annual GMV &nbsp;·&nbsp; 37 locations &nbsp;·&nbsp; 50+ brands &nbsp;·&nbsp; Partner: Lotte Hi-mart (450+ stores nationwide)</div>

      <div class="sub-label">P&L Ownership & Category Strategy</div>
      <div class="bul">Full category P&L responsibility — revenue planning, margin structure, commission model, vendor profitability across premium appliance, built-in kitchen, wellness, audio, and specialty retail segments</div>
      <div class="bul">Drove <b>+11.6% YoY revenue growth (2026)</b> through vendor mix optimization, pricing strategy, and new brand activation programs</div>

      <div class="sub-label">Vendor Negotiation & Commercial Terms</div>
      <div class="bul">Closed a <b>5-year stalled lease negotiation with Lotte Hi-mart at +23% rental increase</b> — largest Hi-mart renewal in the national network; coordinated across legal, operations, and retail partner teams</div>
      <div class="bul">Renegotiated commission structures during vendor onboarding, improving blended category gross margin; rebalanced premium vs. mid-tier assortment via contribution margin analysis</div>

      <div class="sub-label">Activation & Influencer-Linked Commerce</div>
      <div class="bul">Managed Lunar New Year Health Appliance Campaign across <b>9 brands simultaneously</b> — display, pop-up, and online in parallel
        <div class="badges"><span class="badge">$4M GMV</span><span class="badge">111.4% of target</span><span class="badge">+12.1% YoY</span></div>
      </div>
      <div class="bul">Developed 2 Zespa-exclusive massage chair models; partnered with ReviewMachine (Korea's #1 CE YouTuber, 200K subs) for influencer-led group buy
        <div class="badges"><span class="badge">$157K revenue</span><span class="badge">70 units sold out</span><span class="badge">Margin +2%p</span></div>
      </div>
      <div class="bul">Recruited Baekjo Sink (premium built-in) after 5 months sourcing; ran parallel influencer group buy alongside pop-up
        <div class="badges"><span class="badge">$130K GMV</span><span class="badge">$40K online + $90K in-store</span></div>
      </div>

      <div class="sub-label">Data-Driven Decision Making</div>
      <div class="bul">Weekly sell-through, ASP, and contribution margin reviews; pricing and promo calendar adjustments based on performance variance</div>
      <div class="bul">Led annual JBP sessions with strategic vendors; built Excel financial models (Pivot, VLOOKUP, Scenario Analysis) — 5+ years advanced Excel</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tl-card">
      <div class="tl-role">Buyer, Home & Living</div>
      <div class="tl-company">Lotte Outlet HQ</div>
      <div class="tl-period">JAN 2023 – JUL 2025</div>
      <div class="tl-scope">$160M+ annual revenue &nbsp;·&nbsp; 21 locations &nbsp;·&nbsp; 134 brands (Furniture, Bedding, Kitchenware, Tableware, Home Décor, Appliances)</div>

      <div class="sub-label">High-Impact Brand Activation</div>
      <div class="bul"><b>Asahi Super Dry Draft Beer Can pop-up</b> — Korea's first retail activation of this kind; 13 press features + organic coverage by @busanunnie (355K followers); zero paid media; became internal company benchmark
        <div class="badges"><span class="badge">$120K revenue</span><span class="badge">6,000 transactions</span><span class="badge">1,300+ new customers</span><span class="badge">14 days</span></div>
      </div>
      <div class="bul">Recruited Kim Gane Super pop-up (cult-favorite F&amp;B brand known for viral queues) — channel-first in any Korean dept store or outlet; built business case from scratch, coordinated installation and experience design</div>
      <div class="bul">Recruited <b>Daiso + Whose Fan Café</b> for Dongdaemun renewal using foreign visitor traffic data to identify unmet demand; managed full onboarding for both brands
        <div class="badges"><span class="badge">₩26.7억 revenue</span><span class="badge">₩1.8억 profit</span></div>
      </div>
      <div class="bul">Organized licensed IP pop-ups (Gaspard &amp; Lisa, Whosfan Café, Playmobil, Disney Fluffy Festival, Moomin, Shinkai Makoto Shop, Haribo Living) as channel differentiators — all featured in national media</div>

      <div class="sub-label">P&L & Portfolio Rebalancing</div>
      <div class="bul">Maintained <b>+6.3% YoY growth</b> across full portfolio (21 locations, 134 brands)</div>
      <div class="bul">Identified underperforming Samsung Electronics shop-in-shop, led tenant replacement — converted <b>negative contribution to positive operating profit</b></div>
      <div class="bul">Increased category commission by <b>+2–3%p</b> through margin code restructuring; secured +7% better terms with Daiso; normalized terms for Hyundai Livart; implemented management fee structure for Modern House</div>

      <div class="sub-label">Online Channel Activation</div>
      <div class="bul">Recruited Roborak, Deskr, and Jinus for online campaigns; resolved 4-month Deskr suspension through renegotiation
        <div class="badges"><span class="badge">Deskr ₩4.6억</span><span class="badge">Jinus ₩1.7억 annual</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tl-card">
      <div class="tl-role">Store Operations (Part Leader)</div>
      <div class="tl-company">Lotte Department Store — Dongtan Branch</div>
      <div class="tl-period">FEB 2022 – DEC 2022</div>
      <div class="bul">Managed in-store vendor performance and commercial execution across CE, Furniture, and Kitchen — display compliance monitoring, tenant management, real-time in-season execution response</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label" style="margin-top:40px;margin-bottom:14px">Early Career</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="tl-card">
      <div class="tl-role">Content & Data Strategy Intern</div>
      <div class="tl-company">Naver Corp — Korea's largest search & content platform</div>
      <div class="tl-period">JAN – APR 2021</div>
      <div class="bul">Managed content curation for <b>Naver Eohakdang</b> — diagnosed low engagement (&lt;1 daily view/user) via 6-month data analysis; identified preference for article-format &amp; spoken English, peak CTR at commute hours</div>
      <div class="bul">Executed 3 interventions: rebalanced content mix (60% video → 60% article), produced slang &amp; abbreviation series, surfaced quiz content at commute-hour top slot (1.5× CTR boost)
        <div class="badges"><span class="badge">+30% daily views</span><span class="badge">Within 3 months</span></div>
      </div>
    </div>
    <div class="tl-card">
      <div class="tl-role">Marketing & Content Strategy Intern</div>
      <div class="tl-company">Colley — IP licensing &amp; fandom commerce platform</div>
      <div class="tl-period">MAY – AUG 2021</div>
      <div class="bul">Increased user retention by <b>40%</b> through personalized push notification strategy; gained experience in IP monetization and community-driven retail ecosystems</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

# ── KEY PROJECTS ──────────────────────────────────────────────
with t_projects:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Highlights</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Key Projects</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-desc">End-to-end ownership, measurable results, national media impact.</div>', unsafe_allow_html=True)

    st.markdown('<div class="proj-grid">', unsafe_allow_html=True)

    st.markdown("""
    <div class="proj-card">
      <div class="proj-no">Project 01</div>
      <div class="proj-title">Built-in Kitchen Zone — Jamsil</div>
      <div class="proj-sub">Opening May 2026 · Gaggenau · Liebherr · Fhiaba · 9-month program</div>
      <div class="proj-badges">
        <span class="proj-badge">3 Global Brands</span>
        <span class="proj-badge">Sep 2024 → May 2026</span>
        <span class="proj-badge">Korea First</span>
      </div>
      <div class="proj-bul">Led full lifecycle from initial planning (Sep 2024) through construction (May 7) and coordinated opening (May 14) across 3 global brands</div>
      <div class="proj-bul"><b>Primary liaison</b> between brand partners, internal design teams, and construction vendors — resolved conflicts between global fixture/logo specs and department store standards</div>
      <div class="proj-bul">Reviewed &amp; approved interior proposals across all 3 brands; aligned spatial layout and tone-and-manner</div>
      <div class="proj-bul">Designed <b>repeat-visit engagement programs</b> (cooking classes, private events) to convert high-consideration shoppers</div>
    </div>

    <div class="proj-card">
      <div class="proj-no">Project 02</div>
      <div class="proj-title">Asahi Super Dry Draft Beer Can Pop-up</div>
      <div class="proj-sub">Korea's first retail activation of this kind · 14 days · Zero paid media</div>
      <div class="proj-badges">
        <span class="proj-badge">$120K Revenue</span>
        <span class="proj-badge">6,000 Txns</span>
        <span class="proj-badge">1,300+ New Customers</span>
        <span class="proj-badge">13 Press Features</span>
      </div>
      <div class="proj-bul">Proactively identified Asahi issue, secured exclusive pop-up rights; planned limited-release activation strategy for peak sell-through</div>
      <div class="proj-bul">Generated organic coverage by @busanunnie (355K followers) — <b>internal company benchmark for brand activation</b></div>
      <div class="proj-bul">46% of customers aged 25–35; drove significant new-customer acquisition at zero media cost</div>
    </div>

    <div class="proj-card">
      <div class="proj-no">Project 03</div>
      <div class="proj-title">Lunar New Year Health Appliance Campaign</div>
      <div class="proj-sub">9 brands simultaneously · Online + In-store</div>
      <div class="proj-badges">
        <span class="proj-badge">$4M GMV</span>
        <span class="proj-badge">111.4% of Target</span>
        <span class="proj-badge">+12.1% YoY</span>
      </div>
      <div class="proj-bul">Coordinated display programs, pop-up activations, and online group buys across 9 brands in parallel</div>
      <div class="proj-bul">Built cross-functional project trackers; maintained execution documentation across all 9 brand initiatives</div>
    </div>

    <div class="proj-card">
      <div class="proj-no">Project 04</div>
      <div class="proj-title">Dongdaemun District Renewal</div>
      <div class="proj-sub">Daiso + Whose Fan Café tenant recruitment · Foreign visitor data strategy</div>
      <div class="proj-badges">
        <span class="proj-badge">₩26.7억 Revenue</span>
        <span class="proj-badge">₩1.8억 Profit</span>
        <span class="proj-badge">Daiso ₩25억 Annual</span>
      </div>
      <div class="proj-bul">Conducted district-level demand analysis using foreign visitor traffic data — identified unmet demand for Daiso and K-POP fandom café</div>
      <div class="proj-bul">Recruited both tenants and managed full onboarding; Daiso strengthened with foreigner-preferred product sections (beauty, food, character items)</div>
      <div class="proj-bul">Whosfan Café launched artist invitation events and K-Dessert concept — first of its kind in the channel</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

# ── SKILLS ────────────────────────────────────────────────────
with t_skills:
    st.markdown('<div class="section section-alt">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Capabilities</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Core Competencies</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        for cat, skills in [
            ("Commercial & Financial", ["P&L Management", "Category Strategy & KPI Definition", "Margin Optimization", "Portfolio Rebalancing", "Vendor Financial Oversight", "Pricing & Promotional ROI"]),
            ("Activation & Merchandising", ["Pop-Up & Brand Activation", "IP Retail Program Management", "Influencer-Linked Commerce", "Visual Merchandising", "Traffic-Driving Event Planning", "Online + Offline Integration"]),
        ]:
            tags = "".join(f'<span class="skill-tag">{s}</span>' for s in skills)
            st.markdown(f'<div class="skill-block"><div class="skill-title">{cat}</div><div class="skill-tags">{tags}</div></div>', unsafe_allow_html=True)

    with col2:
        for cat, skills in [
            ("Vendor & Negotiation", ["Vendor Relationship Management", "Commercial Term Restructuring", "Joint Business Planning (JBP)", "Tenant Replacement Strategy", "Lease Negotiation", "New Brand / Merchant Sourcing"]),
            ("Analytics & Tools", ["Advanced Excel (Pivot, VLOOKUP, Scenario Analysis)", "Large Dataset Analysis", "Sell-Through & Inventory Monitoring", "Financial Modeling", "Consumer Insights", "AI Tools Integration"]),
        ]:
            tags = "".join(f'<span class="skill-tag">{s}</span>' for s in skills)
            st.markdown(f'<div class="skill-block"><div class="skill-title">{cat}</div><div class="skill-tags">{tags}</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── EDUCATION ─────────────────────────────────────────────────
with t_edu:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Academic</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Education</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="edu-card">
      <div class="edu-icon">🎓</div>
      <div>
        <div class="edu-degree">B.A. in European Culture & Russian Studies</div>
        <div class="edu-school">Chung-Ang University, Seoul</div>
        <div class="edu-period">MAR 2017 – AUG 2021</div>
        <div class="bul">Selected coursework: Marketing, Corporate Finance, Managerial Accounting, Consumer Behavior, Organizational Behavior, International Business</div>
      </div>
    </div>
    <div class="edu-card">
      <div class="edu-icon">✈️</div>
      <div>
        <div class="edu-degree">Exchange Student</div>
        <div class="edu-school">Higher School of Economics (HSE), St. Petersburg, Russia</div>
        <div class="edu-period">2020 EXCHANGE SEMESTER</div>
        <div class="bul">Economics and Business track at one of Russia's leading research universities</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <div>
    <div class="footer-name">Jiwon Kim</div>
    <div class="footer-sub">Retail Buyer &amp; Brand Activator · South Korea</div>
  </div>
  <div class="footer-links">
    <a class="footer-link" href="mailto:jiwonkimv@gmail.com">jiwonkimv@gmail.com</a>
    <a class="footer-link" href="tel:+821026573623">(+82) 10-2657-3623</a>
    <a class="share-btn" href="{linkedin}" target="_blank">🔗 LinkedIn Profile</a>
  </div>
</div>
""", unsafe_allow_html=True)
