import streamlit as st

st.set_page_config(
    page_title="Jiwon Kim — Portfolio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #F5F2ED;
    color: #1A1612;
}
.main { background: #F5F2ED; }
.main > div { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── HERO ── */
.hero {
    background: #1A1612;
    color: #F5F2ED;
    padding: 80px 10% 60px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(212,175,80,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #D4AF50;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.hero-name {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(52px, 8vw, 96px);
    line-height: 1;
    letter-spacing: -2px;
    color: #F5F2ED;
    margin-bottom: 8px;
}
.hero-name em {
    font-style: italic;
    color: #D4AF50;
}
.hero-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 16px;
    font-weight: 300;
    color: rgba(245,242,237,0.6);
    letter-spacing: 1px;
    margin-bottom: 40px;
}
.hero-contact {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
    margin-bottom: 40px;
}
.hero-contact a {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: rgba(245,242,237,0.5);
    text-decoration: none;
    letter-spacing: 1px;
    border-bottom: 1px solid rgba(245,242,237,0.15);
    padding-bottom: 2px;
    transition: color .2s, border-color .2s;
}
.hero-contact a:hover { color: #D4AF50; border-color: #D4AF50; }
.hero-stats {
    display: flex;
    gap: 48px;
    flex-wrap: wrap;
    padding-top: 40px;
    border-top: 1px solid rgba(245,242,237,0.1);
}
.hero-stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 36px;
    color: #D4AF50;
    line-height: 1;
}
.hero-stat-label {
    font-size: 11px;
    color: rgba(245,242,237,0.4);
    letter-spacing: 1px;
    margin-top: 4px;
}

/* ── NAV TABS ── */
.nav-strip {
    background: #1A1612;
    border-top: 1px solid rgba(245,242,237,0.08);
    padding: 0 10%;
    display: flex;
    gap: 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

/* ── SECTION WRAPPER ── */
.section { padding: 64px 10%; }
.section-alt { background: #EDE9E2; }
.section-dark { background: #1A1612; color: #F5F2ED; }

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #D4AF50;
    margin-bottom: 12px;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(28px, 4vw, 44px);
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 40px;
}
.section-dark .section-title { color: #F5F2ED; }

/* ── EXPERIENCE CARDS ── */
.exp-card {
    border-left: 2px solid #D4AF50;
    padding: 28px 32px;
    margin-bottom: 24px;
    background: white;
    position: relative;
}
.exp-card::before {
    content: '';
    position: absolute;
    left: -6px; top: 28px;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #D4AF50;
}
.exp-role {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: #1A1612;
    margin-bottom: 2px;
}
.exp-company {
    font-size: 13px;
    font-weight: 600;
    color: #D4AF50;
    letter-spacing: .5px;
    margin-bottom: 4px;
}
.exp-period {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #999;
    letter-spacing: 1px;
    margin-bottom: 12px;
}
.exp-portfolio {
    font-size: 11px;
    color: #888;
    background: #F5F2ED;
    padding: 6px 12px;
    border-radius: 2px;
    margin-bottom: 16px;
    font-family: 'Space Mono', monospace;
    letter-spacing: .5px;
}
.exp-subsection {
    font-size: 11px;
    font-weight: 700;
    color: #D4AF50;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 18px 0 10px;
}
.bullet {
    font-size: 13px;
    color: #333;
    line-height: 1.7;
    padding-left: 16px;
    position: relative;
    margin-bottom: 8px;
}
.bullet::before {
    content: '▸';
    position: absolute;
    left: 0;
    color: #D4AF50;
    font-size: 10px;
    top: 3px;
}
.bullet b { color: #1A1612; font-weight: 600; }

/* ── PROJECT CARDS ── */
.project-card {
    background: #1A1612;
    color: #F5F2ED;
    padding: 28px 32px;
    margin-bottom: 16px;
    border-left: 2px solid #D4AF50;
}
.project-title {
    font-family: 'DM Serif Display', serif;
    font-size: 18px;
    color: #F5F2ED;
    margin-bottom: 4px;
}
.project-meta {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #D4AF50;
    letter-spacing: 1px;
    margin-bottom: 14px;
}
.project-bullet {
    font-size: 13px;
    color: rgba(245,242,237,0.75);
    line-height: 1.7;
    padding-left: 16px;
    position: relative;
    margin-bottom: 8px;
}
.project-bullet::before {
    content: '▸';
    position: absolute;
    left: 0;
    color: #D4AF50;
    font-size: 10px;
    top: 3px;
}
.project-bullet b { color: #F5F2ED; }

/* ── KPI PILLS ── */
.kpi-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 12px 0 4px;
}
.kpi {
    background: #F5F2ED;
    border: 1px solid #D4AF50;
    color: #1A1612;
    padding: 5px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .5px;
}
.kpi-dark {
    background: rgba(212,175,80,0.1);
    border: 1px solid rgba(212,175,80,0.4);
    color: #D4AF50;
    padding: 5px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .5px;
}

/* ── SKILLS GRID ── */
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
    margin-top: 8px;
}
.skill-item {
    background: white;
    border-left: 2px solid #D4AF50;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 500;
    color: #1A1612;
    letter-spacing: .3px;
}

/* ── PROFILE TEXT ── */
.profile-text {
    font-size: 15px;
    line-height: 1.85;
    color: #333;
    max-width: 800px;
}
.profile-text strong { color: #1A1612; }

/* ── DIVIDER ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, #D4AF50 0%, transparent 100%);
    margin: 32px 0;
    max-width: 200px;
}

/* ── EDUCATION ── */
.edu-card {
    background: white;
    padding: 24px 28px;
    border-top: 2px solid #D4AF50;
    margin-bottom: 12px;
}
.edu-degree {
    font-family: 'DM Serif Display', serif;
    font-size: 17px;
    margin-bottom: 2px;
}
.edu-school {
    font-size: 13px;
    color: #D4AF50;
    font-weight: 600;
    margin-bottom: 4px;
}
.edu-period {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #999;
    letter-spacing: 1px;
}

/* ── FOOTER ── */
.footer {
    background: #0E0C0A;
    color: rgba(245,242,237,0.3);
    padding: 40px 10%;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
}

/* streamlit element resets */
div[data-testid="stMarkdownContainer"] > div { all: unset; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">◈ Portfolio</div>
  <div class="hero-name">Jiwon <em>Kim</em></div>
  <div class="hero-title">Retail Merchandising &amp; Brand Activation &nbsp;·&nbsp; South Korea</div>
  <div class="hero-contact">
    <a href="tel:+821026573623">(+82) 10-2657-3623</a>
    <a href="mailto:jiwonkimv@gmail.com">jiwonkimv@gmail.com</a>
    <a href="https://linkedin.com/in/jiwon-kim-673244226" target="_blank">LinkedIn →</a>
  </div>
  <div class="hero-stats">
    <div>
      <div class="hero-stat-num">5+</div>
      <div class="hero-stat-label">Years Experience</div>
    </div>
    <div>
      <div class="hero-stat-num">$350M+</div>
      <div class="hero-stat-label">GMV Managed</div>
    </div>
    <div>
      <div class="hero-stat-num">50+</div>
      <div class="hero-stat-label">Brand Partners</div>
    </div>
    <div>
      <div class="hero-stat-num">37</div>
      <div class="hero-stat-label">Locations</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── NAV TABS ─────────────────────────────────────────────────
tab_profile, tab_experience, tab_projects, tab_skills, tab_education = st.tabs([
    "Profile", "Experience", "Key Projects", "Skills", "Education"
])

# ── PROFILE ──────────────────────────────────────────────────
with tab_profile:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">About</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Turning Retail Space<br>into Brand Experience</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="profile-text">
      Retail merchandising and brand activation professional with <strong>5+ years</strong> of experience
      managing multi-brand programs across <strong>50+ locations</strong> in Korea's consumer electronics
      and lifestyle retail landscape.<br><br>
      Proven track record in executing pop-up and in-store display programs, managing vendor and agency
      relationships, and driving measurable sell-through results through disciplined project management
      and on-the-ground execution.<br><br>
      Deep familiarity with the South Korean CE retail environment — including <strong>Lotte Hi-mart</strong>,
      department store shop-in-shop formats, and omni-channel activations. Passionate about bringing
      emerging technology products to life in-store through compelling physical experiences.
    </p>
    <div class="gold-divider"></div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background:white;padding:24px 28px;border-top:2px solid #D4AF50">
          <div style="font-family:'DM Serif Display',serif;font-size:32px;color:#D4AF50">$4M</div>
          <div style="font-size:13px;color:#555;margin-top:4px">Single campaign GMV<br>111% of target, +12.1% YoY</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:white;padding:24px 28px;border-top:2px solid #D4AF50">
          <div style="font-family:'DM Serif Display',serif;font-size:32px;color:#D4AF50">+30%</div>
          <div style="font-size:13px;color:#555;margin-top:4px">Daily views via data-driven<br>content curation at Naver</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background:white;padding:24px 28px;border-top:2px solid #D4AF50">
          <div style="font-family:'DM Serif Display',serif;font-size:32px;color:#D4AF50">+23%</div>
          <div style="font-size:13px;color:#555;margin-top:4px">Rental increase closed<br>on 5-year stalled negotiation</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── EXPERIENCE ───────────────────────────────────────────────
with tab_experience:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Career</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Experience</div>', unsafe_allow_html=True)

    # CE Buyer
    st.markdown("""
    <div class="exp-card">
      <div class="exp-role">Buyer, Consumer Electronics (GL)</div>
      <div class="exp-company">Lotte Department Store HQ</div>
      <div class="exp-period">AUG 2025 – PRESENT</div>
      <div class="exp-portfolio">$190M+ annual GMV &nbsp;|&nbsp; 37 locations &nbsp;|&nbsp; 50+ brands &nbsp;|&nbsp; Partner: Lotte Hi-mart (450+ stores nationwide)</div>

      <div class="exp-subsection">Retail Display Program Management</div>
      <div class="bullet">Planned and executed built-in kitchen pop-up (Baekjo Sink) — led full lifecycle from brand sourcing through in-store installation over 5 months
        <div class="kpi-row"><span class="kpi">$130K GMV</span><span class="kpi">$40K online + $90K in-store</span><span class="kpi">Busan relay confirmed May 2026</span></div>
      </div>
      <div class="bullet">Managed end-to-end execution of Lunar New Year Health Appliance Campaign across <b>9 brands simultaneously</b> — display programs, pop-up activations, and online promotions in parallel
        <div class="kpi-row"><span class="kpi">$4M GMV</span><span class="kpi">111.4% of target</span><span class="kpi">+12.1% YoY</span></div>
      </div>
      <div class="bullet">Designed and executed influencer-linked product launch for Zespa exclusive massage chair models — coordinated display setup, demo placement, and creator content in tandem
        <div class="kpi-row"><span class="kpi">$157K revenue</span><span class="kpi">70 units sold out</span><span class="kpi">Margin +2%p above avg</span></div>
      </div>

      <div class="exp-subsection">Lotte Hi-mart Partnership & CE Retail Operations</div>
      <div class="bullet">Served as <b>primary commercial liaison to Lotte Hi-mart</b> (450+ stores) — managed lease terms, display space negotiations, and in-store execution standards</div>
      <div class="bullet">Closed a 5-year stalled lease negotiation at <b>+23% rental increase</b> — largest Hi-mart renewal in the national network; coordinated across legal, operations, and retail partner teams</div>
      <div class="bullet">Drove <b>+11.6% YoY revenue growth (2026)</b> through vendor mix optimization, display space reallocation, and new brand activation programs</div>

      <div class="exp-subsection">Vendor & Agency Coordination</div>
      <div class="bullet">Led annual Joint Business Planning (JBP) sessions with <b>50+ strategic brand partners</b> — managed promotional calendars, display investment planning, and KPI tracking</div>
      <div class="bullet">Coordinated cross-functional teams (marketing, creative, ops, logistics) to deliver concurrent in-store programs on time and on budget</div>
      <div class="bullet">Managed dual-channel P&amp;L (in-store + online); tracked sell-through, ASP, and promotional ROI weekly via advanced Excel</div>
    </div>
    """, unsafe_allow_html=True)

    # Home & Living Buyer
    st.markdown("""
    <div class="exp-card">
      <div class="exp-role">Buyer, Home &amp; Living</div>
      <div class="exp-company">Lotte Outlet HQ</div>
      <div class="exp-period">JAN 2023 – JUL 2025</div>
      <div class="exp-portfolio">$160M+ annual revenue &nbsp;|&nbsp; 21 locations &nbsp;|&nbsp; 134 brands (Furniture, Kitchenware, Home Décor, Appliances)</div>

      <div class="exp-subsection">High-Impact Brand Activation & Pop-Up Execution</div>
      <div class="bullet">Conceived and executed <b>Asahi Super Dry pop-up</b> — Korea's first-ever retail activation of this kind; generated <b>13 press features with zero paid media spend</b>; became internal company benchmark
        <div class="kpi-row"><span class="kpi">$120K revenue</span><span class="kpi">6,000 transactions</span><span class="kpi">1,300+ new customers</span><span class="kpi">14 days</span></div>
      </div>
      <div class="bullet">Recruited and launched <b>Kim Gane Super pop-up</b> (channel-first in Korean department store/outlet retail) — built business case from scratch, coordinated installation and in-store experience design</div>
      <div class="bullet">Led Dongdaemun district renewal: recruited 2 new tenants (<b>Daiso, Whose Fan Café</b>) using foreign visitor traffic data to identify demand gap; managed end-to-end onboarding for both brands</div>

      <div class="exp-subsection">Category Strategy & Retail Performance</div>
      <div class="bullet">Maintained <b>+6.3% YoY growth</b> across full portfolio (21 locations, 134 brands) through assortment optimization and display-driven sell-through improvement</div>
      <div class="bullet">Identified underperforming Samsung shop-in-shop and led tenant replacement — redesigned space allocation, converting negative contribution to <b>positive operating profit</b></div>
      <div class="bullet">Managed display budgets and vendor commercial terms across 134 brands; increased category commission by <b>+2–3%p</b> through margin code restructuring</div>
    </div>
    """, unsafe_allow_html=True)

    # Store Ops
    st.markdown("""
    <div class="exp-card">
      <div class="exp-role">Store Operations (Part Leader)</div>
      <div class="exp-company">Lotte Department Store — Dongtan Branch</div>
      <div class="exp-period">FEB 2022 – DEC 2022</div>
      <div class="bullet">Managed in-store vendor performance and commercial execution across CE, Furniture, and Kitchen categories — hands-on display compliance monitoring, tenant management, and real-time in-season execution response</div>
    </div>
    """, unsafe_allow_html=True)

    # Early Career
    st.markdown('<div class="section-label" style="margin-top:40px">Early Career</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="exp-card">
      <div class="exp-role">Content &amp; Data Strategy Intern</div>
      <div class="exp-company">Naver — Korea's largest search &amp; content platform</div>
      <div class="exp-period">JAN – APR 2021</div>
      <div class="bullet">Managed content curation for <b>Naver Eohakdang</b> — diagnosed low engagement (&lt;1 daily view/user) by analyzing 6 months of content data; identified user preference for article-format and spoken English content, and peak engagement during commute hours</div>
      <div class="bullet">Executed 3 data-driven interventions: (1) rebalanced content mix 60% video → 60% article; (2) produced original spoken-English content (slang &amp; abbreviations series); (3) surfaced quiz content at top placement during commute hours when CTR was <b>1.5× higher</b>
        <div class="kpi-row"><span class="kpi">+30% daily view increase</span><span class="kpi">Within 3 months</span></div>
      </div>
    </div>

    <div class="exp-card">
      <div class="exp-role">Marketing &amp; Content Strategy Intern</div>
      <div class="exp-company">Colley — IP licensing &amp; commerce platform</div>
      <div class="exp-period">MAY – AUG 2021</div>
      <div class="bullet">Increased user retention by <b>40%</b> through personalized push notification strategy; gained experience in IP licensing and brand partnership environments</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── KEY PROJECTS ─────────────────────────────────────────────
with tab_projects:
    st.markdown('<div class="section section-alt">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Highlights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Projects</div>', unsafe_allow_html=True)

    # Built-in Kitchen Zone
    st.markdown("""
    <div class="project-card">
      <div class="project-title">Built-in Kitchen Zone — Jamsil</div>
      <div class="project-meta">OPENING MAY 2026 &nbsp;·&nbsp; GAGGENAU &nbsp;·&nbsp; LIEBHERR &nbsp;·&nbsp; FHIABA &nbsp;·&nbsp; 9-MONTH PROGRAM</div>
      <div class="project-bullet">Led <b>end-to-end development</b> of a premium multi-brand built-in kitchen zone from initial planning (Sep 2024) through construction (May 7) and coordinated opening (May 14) across 3 global brands</div>
      <div class="project-bullet">Served as <b>primary liaison between brand partners, internal design teams, and construction vendors</b> — resolved conflicts between global brand fixture/logo specifications and department store design standards</div>
      <div class="project-bullet">Reviewed and approved interior design proposals across adjacent brands, aligning spatial layout, fixture standards, and tone-and-manner across the zone</div>
      <div class="project-bullet">Designed <b>repeat-visit engagement programs</b> (cooking classes, private invitation events) to drive hands-on product experience and support conversion for high-consideration, high-price-point purchases</div>
    </div>
    """, unsafe_allow_html=True)

    # Asahi
    st.markdown("""
    <div class="project-card">
      <div class="project-title">Asahi Super Dry Draft Beer Can Pop-up</div>
      <div class="project-meta">KOREA'S FIRST RETAIL ACTIVATION OF ITS KIND &nbsp;·&nbsp; 14 DAYS &nbsp;·&nbsp; ZERO PAID MEDIA</div>
      <div class="kpi-row" style="margin-bottom:14px">
        <span class="kpi-dark">$120K Revenue</span>
        <span class="kpi-dark">6,000 Transactions</span>
        <span class="kpi-dark">1,300+ New Customers</span>
        <span class="kpi-dark">13 Press Features</span>
      </div>
      <div class="project-bullet">Created an experience-driven retail environment combining product sampling, storytelling, and interactive engagement</div>
      <div class="project-bullet">Managed vendor coordination, display setup, and in-store execution end-to-end — became <b>internal company benchmark for brand activation</b></div>
    </div>
    """, unsafe_allow_html=True)

    # Health Campaign
    st.markdown("""
    <div class="project-card">
      <div class="project-title">Lunar New Year Health Appliance Campaign</div>
      <div class="project-meta">9 BRANDS SIMULTANEOUSLY &nbsp;·&nbsp; MULTI-CHANNEL</div>
      <div class="kpi-row" style="margin-bottom:14px">
        <span class="kpi-dark">$4M GMV</span>
        <span class="kpi-dark">111.4% of Target</span>
        <span class="kpi-dark">+12.1% YoY</span>
      </div>
      <div class="project-bullet">Coordinated simultaneous in-store display programs, pop-up activations, and online promotions across 9 brands in parallel</div>
    </div>
    """, unsafe_allow_html=True)

    # Zespa
    st.markdown("""
    <div class="project-card">
      <div class="project-title">Zespa Product Launch Activation</div>
      <div class="project-meta">INFLUENCER-LINKED &nbsp;·&nbsp; EXCLUSIVE MODELS</div>
      <div class="kpi-row" style="margin-bottom:14px">
        <span class="kpi-dark">$157K Revenue</span>
        <span class="kpi-dark">70 Units Sold Out</span>
        <span class="kpi-dark">Margin +2%p Above Avg</span>
      </div>
      <div class="project-bullet">Executed influencer-linked in-store activation — coordinated display setup, demo unit placement, and creator content in tandem</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── SKILLS ───────────────────────────────────────────────────
with tab_skills:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Capabilities</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Core Competencies</div>', unsafe_allow_html=True)

    categories = {
        "Activation & Display": [
            "Pop-Up & Display Program Management",
            "In-Store Execution & Compliance",
            "Visual Merchandising Strategy",
            "Retail Layout & Flow Optimization",
        ],
        "Commercial & Strategy": [
            "CE Retail Partner Management",
            "Budget & P&L Management",
            "Sell-Through & KPI Analysis",
            "Promotional ROI Tracking",
        ],
        "Operations & Tools": [
            "Project Tracking & Reporting",
            "Advanced Excel (Pivot, Scenario Analysis)",
            "AI Tools Integration",
            "Omni-Channel Activation",
        ],
        "Stakeholder Management": [
            "Vendor & Agency Coordination",
            "Cross-Functional Collaboration",
            "New Brand / Merchant Sourcing",
            "Consumer Insights & Analytics",
        ],
    }

    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]
    for i, (cat, skills) in enumerate(categories.items()):
        with cols[i]:
            st.markdown(f'<div style="margin-bottom:24px"><div class="exp-subsection" style="margin-top:0">{cat}</div>', unsafe_allow_html=True)
            for skill in skills:
                st.markdown(f'<div class="skill-item">{skill}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── EDUCATION ────────────────────────────────────────────────
with tab_education:
    st.markdown('<div class="section section-alt">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Academic</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Education</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="edu-card">
      <div class="edu-degree">B.A. in Russian Studies</div>
      <div class="edu-school">Chung-Ang University</div>
      <div class="edu-period">MAR 2017 – AUG 2021</div>
      <div style="margin-top:12px">
        <div class="bullet">Relevant coursework: Marketing, Corporate Finance, Managerial Accounting, Consumer Behavior, Organizational Behavior, International Business</div>
      </div>
    </div>

    <div class="edu-card">
      <div class="edu-degree">Exchange Student</div>
      <div class="edu-school">Higher School of Economics (HSE), St. Petersburg, Russia</div>
      <div class="edu-period">EXCHANGE SEMESTER</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span>◈ JIWON KIM &nbsp;·&nbsp; RETAIL MERCHANDISING &amp; BRAND ACTIVATION</span>
  <span>jiwonkimv@gmail.com &nbsp;·&nbsp; (+82) 10-2657-3623</span>
</div>
""", unsafe_allow_html=True)
