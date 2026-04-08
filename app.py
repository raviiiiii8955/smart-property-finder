"""PropFinder AI — Premium SaaS Dashboard"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from auth import login, logout, sign_up, is_logged_in, add_favorite, remove_favorite, get_favorites
from nlp_parser import parse_query
from model import get_properties, filter_properties, get_scorer

st.set_page_config(page_title="PropFinder AI", page_icon="🏠", layout="wide",
                   initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap');
#MainMenu,header[data-testid="stHeader"],footer,.stDeployButton{display:none!important}
*,*::before,*::after{box-sizing:border-box}
html,body,[class*="css"]{font-family:'Inter',sans-serif}

/* ── Background ── */
.stApp{
  background:linear-gradient(135deg,#0d0b1e 0%,#111827 50%,#0f0c2a 100%);
  min-height:100vh
}
.main .block-container{padding:0 1.8rem 4rem;max-width:1480px}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0d0b1e 0%,#111130 100%)!important;
  border-right:1px solid rgba(255,255,255,.08)!important
}
section[data-testid="stSidebar"] *{color:#e5e7eb!important}
section[data-testid="stSidebar"] .stSelectbox>div>div,
section[data-testid="stSidebar"] .stMultiSelect>div>div{
  background:rgba(255,255,255,.06)!important;
  border-color:rgba(255,56,92,.30)!important;border-radius:10px!important
}

/* ── Keyframes ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes shimmer{0%,100%{background-position:0 50%}50%{background-position:100% 50%}}

/* ── Top nav ── */
.top-bar{
  display:flex;align-items:center;justify-content:space-between;
  padding:.8rem 0 .9rem;margin-bottom:1.4rem;
  border-bottom:1px solid rgba(255,255,255,.07)
}
.tb-brand{display:flex;align-items:center;gap:.7rem}
.tb-logo{
  width:36px;height:36px;border-radius:10px;
  background:linear-gradient(135deg,#FF385C,#e31c5f);
  display:flex;align-items:center;justify-content:center;
  font-family:'Plus Jakarta Sans',sans-serif;font-weight:900;font-size:.75rem;color:#fff;
  box-shadow:0 4px 16px rgba(255,56,92,.45)
}
.tb-name{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.15rem;font-weight:800;color:#f9fafb}
.tb-pill{
  font-size:.78rem;color:#9ca3af;
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.10);
  padding:.3rem .8rem;border-radius:20px
}

/* ── Auth ── */
.auth-wrap{display:flex;flex-direction:column;align-items:center;padding:2.5rem 0 1rem}
.auth-logo{
  width:52px;height:52px;border-radius:16px;
  background:linear-gradient(135deg,#FF385C,#e31c5f);
  display:flex;align-items:center;justify-content:center;
  font-family:'Plus Jakarta Sans',sans-serif;font-weight:900;font-size:1rem;color:#fff;
  box-shadow:0 6px 24px rgba(255,56,92,.5);margin-bottom:.9rem
}
.auth-h{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.55rem;font-weight:800;color:#f9fafb;margin-bottom:.25rem;text-align:center}
.auth-sub{font-size:.82rem;color:#6b7280;text-align:center;margin-bottom:1.6rem}
.auth-hint{
  margin-top:1rem;padding:.5rem 1rem;border-radius:10px;font-size:.74rem;
  color:#6b7280;background:rgba(255,56,92,.07);border:1px solid rgba(255,56,92,.18);text-align:center
}
.auth-stats{display:flex;gap:1rem;justify-content:center;margin-top:2.2rem;flex-wrap:wrap}
.astat{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
  border-radius:14px;padding:.9rem 1.6rem;text-align:center;min-width:130px
}
.astat-val{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.4rem;font-weight:800;color:#FF385C}
.astat-lbl{font-size:.65rem;color:#6b7280;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-top:.15rem}

/* ── Hero search ── */
.hero{
  background:linear-gradient(120deg,rgba(255,56,92,.18) 0%,rgba(99,102,241,.15) 50%,rgba(255,56,92,.12) 100%);
  border:1px solid rgba(255,56,92,.25);border-radius:24px;
  padding:2rem 2.4rem 1.8rem;margin-bottom:1.2rem;text-align:center;
  animation:fadeUp .5s ease both;
  box-shadow:0 8px 50px rgba(255,56,92,.12)
}
.hero-h{
  font-family:'Plus Jakarta Sans',sans-serif;font-size:2.4rem;font-weight:800;
  background:linear-gradient(110deg,#fff 0%,#fca5a5 40%,#f9a8d4 80%);
  background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:shimmer 5s ease infinite;margin-bottom:.35rem
}
.hero-sub{font-size:.9rem;color:#9ca3af;font-weight:400}

/* ── Metric tiles ── */
.mbar{display:grid;grid-template-columns:repeat(5,1fr);gap:.8rem;margin:1.1rem 0}
.mtile{
  border-radius:16px;padding:1rem .9rem;text-align:center;
  transition:transform .2s;position:relative;overflow:hidden
}
.mtile:hover{transform:translateY(-3px)}
.mtile::before{content:'';position:absolute;inset:0;border-radius:16px;background:linear-gradient(135deg,rgba(255,255,255,.09) 0%,rgba(255,255,255,.0) 60%)}
.mt1{background:linear-gradient(135deg,#7f1d1d,#ef4444);border:1px solid rgba(252,165,165,.25);box-shadow:0 4px 20px rgba(239,68,68,.30)}
.mt2{background:linear-gradient(135deg,#1e1b4b,#4f46e5);border:1px solid rgba(165,180,252,.25);box-shadow:0 4px 20px rgba(79,70,229,.30)}
.mt3{background:linear-gradient(135deg,#064e3b,#10b981);border:1px solid rgba(110,231,183,.25);box-shadow:0 4px 20px rgba(16,185,129,.25)}
.mt4{background:linear-gradient(135deg,#7c2d12,#f97316);border:1px solid rgba(253,186,116,.25);box-shadow:0 4px 20px rgba(249,115,22,.25)}
.mt5{background:linear-gradient(135deg,#4a044e,#a21caf);border:1px solid rgba(240,171,252,.25);box-shadow:0 4px 20px rgba(162,28,175,.30)}
.mval{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:800;color:#fff}
.mlbl{font-size:.62rem;color:rgba(255,255,255,.65);margin-top:.2rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase}

/* ── Property card (Airbnb-style) ── */
.pcard{
  background:rgba(17,17,48,.75);
  border:1px solid rgba(255,255,255,.08);
  border-radius:20px;overflow:hidden;margin-bottom:1.1rem;
  transition:transform .25s ease,box-shadow .25s ease,border-color .25s;
  animation:fadeUp .4s ease both;position:relative
}
.pcard:hover{
  transform:translateY(-6px);
  box-shadow:0 24px 60px rgba(0,0,0,.5),0 0 0 1px rgba(255,56,92,.25);
  border-color:rgba(255,56,92,.30)
}
.pimg{position:relative;height:195px;overflow:hidden}
.pimg img{width:100%;height:100%;object-fit:cover;transition:transform .4s ease;display:block}
.pcard:hover .pimg img{transform:scale(1.05)}
.pimg-overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(10,10,29,.90) 0%,transparent 52%)}
.ptags{position:absolute;top:10px;left:10px;display:flex;gap:4px;flex-wrap:wrap}
.ptag{font-size:.62rem;font-weight:700;padding:3px 8px;border-radius:20px;backdrop-filter:blur(8px)}
.ptag-hot{background:rgba(239,68,68,.85);color:#fff}
.ptag-new{background:rgba(99,102,241,.85);color:#fff}
.ptag-rtm{background:rgba(16,185,129,.85);color:#fff}
.ptag-star{background:rgba(245,158,11,.85);color:#fff}
.ptag-rera{background:rgba(6,182,212,.85);color:#fff}
.ptag-drop{background:rgba(236,72,153,.85);color:#fff}
.pprice{
  position:absolute;bottom:10px;left:13px;
  font-family:'Plus Jakarta Sans',sans-serif;font-size:1.15rem;font-weight:800;color:#fff;
  text-shadow:0 2px 10px rgba(0,0,0,.8)
}
.pscore{
  position:absolute;bottom:10px;right:11px;
  background:linear-gradient(135deg,#FF385C,#e31c5f);
  color:#fff;font-weight:800;border-radius:8px;padding:2px 9px;font-size:.78rem
}
.pbody{padding:.85rem 1.1rem .95rem}
.pbuilder{font-size:.7rem;color:#FF385C;font-weight:700;margin-bottom:.2rem;letter-spacing:.03em}
.ptitle{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.95rem;font-weight:700;color:#f9fafb;margin-bottom:.18rem;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.ploc{font-size:.72rem;color:#6b7280;margin-bottom:.55rem}
.ppills{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:.5rem}
.ppill{
  background:rgba(255,56,92,.10);border:1px solid rgba(255,56,92,.22);
  border-radius:7px;padding:2px 8px;font-size:.69rem;color:#fca5a5;font-weight:600
}
.pams{margin:.1rem 0 .45rem;line-height:1.9}
.pam{
  display:inline-block;font-size:.6rem;font-weight:700;
  border-radius:20px;padding:2px 7px;margin:2px;
  background:rgba(99,102,241,.14);border:1px solid rgba(99,102,241,.28);color:#a5b4fc
}
.pfoot{
  border-top:1px solid rgba(255,255,255,.06);padding-top:.52rem;margin-top:.38rem;
  display:flex;justify-content:space-between;align-items:center;
  font-size:.7rem;color:#4b5563
}
.pagent{color:#8b5cf6;font-weight:600}
.ppsf{color:#4b5563}

/* ── Section header ── */
.shdr{
  font-family:'Plus Jakarta Sans',sans-serif;font-size:1.25rem;font-weight:800;color:#f9fafb;
  display:flex;align-items:center;gap:.5rem;margin:1.2rem 0 .9rem
}
.shdr::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(255,56,92,.35),transparent);margin-left:.6rem}

/* ── Sidebar brand ── */
.sbbrand{padding:1.2rem .9rem .6rem;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:.5rem}
.sbrow{display:flex;align-items:center;gap:.55rem;margin-bottom:.5rem}
.sblogo{
  width:28px;height:28px;border-radius:7px;
  background:linear-gradient(135deg,#FF385C,#e31c5f);
  display:flex;align-items:center;justify-content:center;
  font-family:'Plus Jakarta Sans',sans-serif;font-weight:900;font-size:.65rem;color:#fff
}
.sbname{font-family:'Plus Jakarta Sans',sans-serif;font-size:.95rem;font-weight:800;color:#f9fafb!important}
.sbuser{font-size:.72rem;color:#6b7280!important}
.sbsec{font-size:.62rem!important;color:#4b5563!important;font-weight:700!important;letter-spacing:.09em!important;text-transform:uppercase!important;padding:.15rem 0 .35rem!important;margin-top:.35rem!important}

/* ── EMI ── */
.emipanel{
  background:linear-gradient(135deg,rgba(255,56,92,.08),rgba(99,102,241,.07));
  border:1px solid rgba(255,56,92,.20);border-radius:18px;padding:1.4rem
}
.emiamt{
  font-family:'Plus Jakarta Sans',sans-serif;font-size:2.2rem;font-weight:800;
  background:linear-gradient(90deg,#FF385C,#f97316);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  text-align:center;padding:.3rem 0
}
.emirow{display:flex;justify-content:space-between;font-size:.79rem;color:#9ca3af;padding:.32rem 0;border-bottom:1px solid rgba(255,255,255,.05)}
.emirow:last-child{border:none}

/* ── Widgets ── */
.stTextInput>div>div>input{
  background:rgba(255,255,255,.06)!important;
  border:1px solid rgba(255,255,255,.14)!important;
  border-radius:10px!important;color:#f9fafb!important;
  font-size:.88rem!important;padding:.52rem .9rem!important;
  transition:border-color .2s,box-shadow .2s!important
}
.stTextInput>div>div>input:focus{border-color:#FF385C!important;box-shadow:0 0 0 3px rgba(255,56,92,.18)!important}
.stTextInput>div>div>input::placeholder{color:#4b5563!important}
.stSelectbox>div>div,.stMultiSelect>div>div{
  background:rgba(255,255,255,.06)!important;border-color:rgba(255,255,255,.14)!important;
  border-radius:10px!important;color:#f9fafb!important
}
.stTextInput label,.stSelectbox label,.stMultiSelect label,
.stSlider label,.stNumberInput label{color:#d1d5db!important;font-weight:600!important;font-size:.8rem!important}
.stButton>button{
  background:linear-gradient(135deg,#FF385C,#e31c5f)!important;
  color:#fff!important;border:none!important;border-radius:10px!important;
  font-weight:700!important;font-family:'Plus Jakarta Sans',sans-serif!important;
  padding:.48rem 1.3rem!important;font-size:.86rem!important;
  transition:transform .18s,box-shadow .18s,opacity .18s!important;
  box-shadow:0 3px 16px rgba(255,56,92,.35)!important
}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 26px rgba(255,56,92,.5)!important;opacity:.95!important}
.stTabs [data-baseweb="tab"]{color:#6b7280!important;font-weight:600!important;font-size:.84rem!important}
.stTabs [aria-selected="true"]{color:#f9fafb!important;font-weight:700!important}
.stTabs [data-baseweb="tab-highlight"]{background:#FF385C!important}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.04)!important;border-radius:12px!important;padding:3px!important}
[data-testid="stExpander"]{background:rgba(255,255,255,.03)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:12px!important}
.stAlert{border-radius:11px!important}
h1,h2,h3,h4{color:#f9fafb!important;font-family:'Plus Jakarta Sans',sans-serif!important}
p,li{color:#d1d5db!important}
hr{border-color:rgba(255,255,255,.08)!important}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────
def fmt(lakh):
    return f"₹{lakh/100:.2f} Cr" if lakh >= 100 else f"₹{lakh:.1f} L"

def emi(p, r, n):
    p *= 1e5; r /= 1200; n *= 12
    return p/n if r==0 else p*r*(1+r)**n/((1+r)**n-1)

def tags_html(tags):
    import re
    m={"Hot Deal":"ptag-hot","New Launch":"ptag-new","Ready to Move":"ptag-rtm",
       "Top Rated":"ptag-star","RERA Registered":"ptag-rera","Price Drop":"ptag-drop",
       "Hot Deal 🔥":"ptag-hot","New Launch 🚀":"ptag-new","Ready to Move ✅":"ptag-rtm",
       "Top Rated ⭐":"ptag-star","Price Drop 💰":"ptag-drop"}
    cl=lambda t: re.sub(r'[\U00010000-\U0010ffff\U00002600-\U000027BF\U0001F300-\U0001FAFF]','',t).strip()
    return "".join(f'<span class="ptag {m.get(t,"ptag-new")}">{cl(t)}</span>' for t in tags[:3])

def clayout(title=""):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9ca3af",family="Inter"),
        title=dict(text=title,font=dict(color="#f9fafb",size=14,family="Plus Jakarta Sans")),
        margin=dict(l=8,r=8,t=38,b=8),
        xaxis=dict(gridcolor="rgba(255,255,255,.05)",zerolinecolor="rgba(255,255,255,.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,.05)",zerolinecolor="rgba(255,255,255,.05)"),
    )


# ── AUTH ──────────────────────────────────────────────────────────────────────
def render_auth():
    st.markdown('<style>.main .block-container{max-width:960px;padding:0 2rem 3rem}</style>',unsafe_allow_html=True)
    _,mid,_ = st.columns([1,1.1,1])
    with mid:
        st.markdown("""
        <div class="auth-wrap">
          <div class="auth-logo">PF</div>
          <div class="auth-h">Welcome to PropFinder AI</div>
          <div class="auth-sub">India's smartest property search platform</div>
        </div>""",unsafe_allow_html=True)
        t1,t2 = st.tabs(["Sign In","Create Account"])
        with t1:
            st.markdown('<div style="height:.5rem"></div>',unsafe_allow_html=True)
            u=st.text_input("Username",key="liu",placeholder="Enter your username")
            p=st.text_input("Password",type="password",key="lip",placeholder="Enter your password")
            if st.button("Sign In →",key="btnli",use_container_width=True):
                if u and p:
                    ok,msg=login(u,p)
                    if ok: st.rerun()
                    else: st.error(msg)
                else: st.warning("Please fill all fields.")
            st.markdown('<div class="auth-hint">Demo — Username: <b style="color:#fca5a5">demo</b> &nbsp;/&nbsp; Password: <b style="color:#fca5a5">demo123</b></div>',unsafe_allow_html=True)
        with t2:
            st.markdown('<div style="height:.5rem"></div>',unsafe_allow_html=True)
            fn=st.text_input("Full Name",key="sufn",placeholder="Your full name")
            su=st.text_input("Username",key="suu",placeholder="Choose a username")
            sp=st.text_input("Password",type="password",key="sup",placeholder="Min 6 characters")
            if st.button("Create Account →",key="btnsu",use_container_width=True):
                if fn and su and sp:
                    ok,msg=sign_up(su,sp,fn)
                    if ok: st.success(msg+" Please sign in.")
                    else: st.error(msg)
                else: st.warning("Please fill all fields.")

    st.markdown("""
    <div class="auth-stats">
      <div class="astat"><div class="astat-val">200+</div><div class="astat-lbl">Listings</div></div>
      <div class="astat"><div class="astat-val">15</div><div class="astat-lbl">Cities</div></div>
      <div class="astat"><div class="astat-val">25+</div><div class="astat-lbl">Builders</div></div>
      <div class="astat"><div class="astat-val">AI</div><div class="astat-lbl">Powered</div></div>
    </div>""",unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        user=st.session_state.get("full_name","User")
        st.markdown(f"""
        <div class="sbbrand">
          <div class="sbrow">
            <div class="sblogo">PF</div>
            <div class="sbname">PropFinder AI</div>
          </div>
          <div class="sbuser">Signed in as <b style="color:#fca5a5!important">{user}</b></div>
        </div>""",unsafe_allow_html=True)

        st.markdown('<div class="sbsec">Navigation</div>',unsafe_allow_html=True)
        page=st.radio("nav",["Search","Analytics","Saved Properties","EMI Calculator"],
                      key="navp",label_visibility="collapsed")

        st.markdown('<div class="sbsec" style="margin-top:.8rem">Filters</div>',unsafe_allow_html=True)
        ap=get_properties()
        city  =st.selectbox("City",              ["All Cities"]  +sorted(ap["city"].unique()),key="sbc")
        ptype =st.selectbox("Property Type",     ["All Types"]   +sorted(ap["property_type"].unique()),key="sbt")
        bldr  =st.selectbox("Builder/Developer", ["All Builders"]+sorted(ap["builder"].unique()),key="sbb")
        price =st.slider("Budget (Lakhs)",0,1000,(0,500),10,key="sbp")
        beds  =st.multiselect("Bedrooms (BHK)",[1,2,3,4,5],key="sbbd")
        status=st.multiselect("Possession",["Ready to Move","Under Construction","New Launch","Resale"],key="sbst")

        st.markdown("<hr>",unsafe_allow_html=True)
        fc=len(get_favorites())
        st.markdown(f'<div style="font-size:.73rem;color:#4b5563;text-align:center;margin-bottom:.5rem">{fc} saved</div>',unsafe_allow_html=True)
        if st.button("Sign Out",use_container_width=True,key="btnlo"):
            logout();st.rerun()

        pm={"Search":"Search","Analytics":"Analytics","Saved Properties":"Favorites","EMI Calculator":"EMI Calculator"}
        return pm[page],{"city":city,"property_type":ptype,"builder":bldr,"price_range":price,"beds":beds,"status":status}


# ── CARD ──────────────────────────────────────────────────────────────────────
def render_card(row,score=None):
    is_fav=row["id"] in get_favorites()
    am="".join(f'<span class="pam">{a}</span>' for a in row["amenities"][:5])
    sh=f'<div class="pscore">{score}/10</div>' if score else ""
    st.markdown(f"""
    <div class="pcard">
      <div class="pimg">
        <img src="{row['image_url']}" alt="{row['title']}" loading="lazy">
        <div class="pimg-overlay"></div>
        <div class="ptags">{tags_html(row.get('tags',[]))}</div>
        <div class="pprice">{fmt(row['price_lakh'])}</div>{sh}
      </div>
      <div class="pbody">
        <div class="pbuilder">{row['builder']}</div>
        <div class="ptitle" title="{row['title']}">{row['title']}</div>
        <div class="ploc">{row['locality']}, {row['city']} &middot; {row['status']}</div>
        <div class="ppills">
          <span class="ppill">{row['beds']} BHK</span>
          <span class="ppill">{row['baths']} Bath</span>
          <span class="ppill">{row['area_sqft']:,} sqft</span>
          <span class="ppill">&#9733; {row['rating']}</span>
          <span class="ppill">Fl. {row['floor']}</span>
        </div>
        <div class="pams">{am}</div>
        <div class="pfoot">
          <span class="pagent">{row['agent']}</span>
          <span class="ppsf">₹{row['price_psf']:,}/sqft &middot; {row['year_built']}</span>
        </div>
      </div>
    </div>""",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("♡ Unsave" if is_fav else "♡ Save",key=f"fv{row['id']}",use_container_width=True):
            remove_favorite(row["id"]) if is_fav else add_favorite(row["id"])
            st.rerun()
    with c2:
        with st.expander("Details"):
            st.markdown(f"**Description:** {row['description']}")
            st.markdown(f"**RERA:** `{row['rera']}`")


# ── FILTER LOGIC ──────────────────────────────────────────────────────────────
def filt(df,sf):
    if sf["city"] not in ("All","All Cities"):      df=df[df["city"]==sf["city"]]
    if sf["property_type"] not in ("All","All Types"): df=df[df["property_type"]==sf["property_type"]]
    if sf["builder"] not in ("All","All Builders"): df=df[df["builder"]==sf["builder"]]
    lo,hi=sf["price_range"]
    df=df[(df["price_lakh"]>=lo)&(df["price_lakh"]<=hi)]
    if sf["beds"]:   df=df[df["beds"].isin(sf["beds"])]
    if sf["status"]: df=df[df["status"].isin(sf["status"])]
    return df.reset_index(drop=True)


# ── SEARCH ────────────────────────────────────────────────────────────────────
def render_search(sf):
    user=st.session_state.get("full_name","User")
    st.markdown(f"""
    <div class="top-bar">
      <div class="tb-brand">
        <div class="tb-logo">PF</div>
        <div class="tb-name">PropFinder AI</div>
      </div>
      <div class="tb-pill">{user}</div>
    </div>""",unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
      <div class="hero-h">Find Your Dream Home</div>
      <div class="hero-sub">Describe what you want in plain English — our AI understands you</div>
    </div>""",unsafe_allow_html=True)

    query=st.text_input("",placeholder="e.g. 3 BHK flat in Mumbai under ₹1.5 Cr with swimming pool",
                        key="nlpq",label_visibility="collapsed")
    c1,c2,c3=st.columns([3,1,1])
    with c1: clicked=st.button("Search Properties",key="btns",use_container_width=True)
    with c2:
        if st.button("Try Example",key="btne",use_container_width=True):
            st.session_state["nlpq"]="2 BHK flat in Bangalore under 80 lakh with pool"
            st.rerun()
    with c3:
        if st.button("Clear",key="btnr",use_container_width=True):
            st.session_state.pop("last_nlp","");st.rerun()

    nlf={}
    if clicked and query:
        nlf=parse_query(query);st.session_state["last_nlp"]=nlf
        if nlf:
            chips="  ·  ".join(f"{k.replace('_',' ').title()}: {v}" for k,v in nlf.items() if k!="keywords")
            st.markdown(f'<div style="margin:.35rem 0 .7rem;padding:.5rem 1rem;background:rgba(255,56,92,.08);border-left:3px solid #FF385C;border-radius:9px;font-size:.79rem;color:#fca5a5">AI Filters: {chips}</div>',unsafe_allow_html=True)
    elif "last_nlp" in st.session_state:
        nlf=st.session_state["last_nlp"]

    df=filter_properties(nlf) if nlf else get_properties()
    df=filt(df,sf)
    scorer=get_scorer()
    if not df.empty:
        df=df.copy();df["score"]=scorer.score(df,nlf or {})
        df=df.sort_values("score",ascending=False).reset_index(drop=True)

    # Metrics
    st.markdown(f"""
    <div class="mbar">
      <div class="mtile mt1"><div class="mval">{len(df)}</div><div class="mlbl">Found</div></div>
      <div class="mtile mt2"><div class="mval">{fmt(df['price_lakh'].mean() if not df.empty else 0)}</div><div class="mlbl">Avg Price</div></div>
      <div class="mtile mt3"><div class="mval">{int(df['area_sqft'].mean()) if not df.empty else 0:,}</div><div class="mlbl">Avg Sqft</div></div>
      <div class="mtile mt4"><div class="mval">{df['rating'].mean() if not df.empty else 0:.1f}</div><div class="mlbl">Avg Rating</div></div>
      <div class="mtile mt5"><div class="mval">₹{int(df['price_psf'].mean()) if not df.empty else 0:,}</div><div class="mlbl">Price/sqft</div></div>
    </div>""",unsafe_allow_html=True)

    if df.empty:
        st.warning("No properties match. Try broadening your filters.");return

    sc1,sc2=st.columns([4,1])
    with sc1: st.markdown(f'<div style="font-size:.8rem;color:#6b7280;padding-top:.5rem">Showing {len(df)} properties</div>',unsafe_allow_html=True)
    with sc2: sort=st.selectbox("Sort",["AI Score","Price ↑","Price ↓","Rating","Area","Newest"],key="srt",label_visibility="collapsed")
    sm={"Price ↑":("price_lakh",True),"Price ↓":("price_lakh",False),"Rating":("rating",False),"Area":("area_sqft",False),"Newest":("year_built",False)}
    if sort in sm: c,a=sm[sort];df=df.sort_values(c,ascending=a).reset_index(drop=True)

    for i in range(0,len(df),3):
        cols=st.columns(3)
        for j,(_,row) in enumerate(df.iloc[i:i+3].iterrows()):
            with cols[j]: render_card(row,score=round(row.get("score",0),1))


# ── ANALYTICS ─────────────────────────────────────────────────────────────────
def render_analytics():
    st.markdown('<div class="shdr">Market Analytics</div>',unsafe_allow_html=True)
    df=get_properties()
    t1,t2,t3,t4=st.tabs(["Pricing","City Insights","Supply Mix","Trends"])

    def ch(fig,title=""):
        fig.update_layout(**clayout(title))
        st.plotly_chart(fig,use_container_width=True)

    with t1:
        c1,c2=st.columns(2)
        with c1:
            f=px.histogram(df,x="price_lakh",nbins=35,color_discrete_sequence=["#FF385C"],labels={"price_lakh":"Price (L)"})
            f.update_traces(marker_line_color="rgba(0,0,0,0)",opacity=.85);ch(f,"Price Distribution")
        with c2:
            f=px.scatter(df,x="area_sqft",y="price_lakh",color="property_type",size="rating",size_max=13,
                         hover_data=["city","builder","beds"],color_discrete_sequence=px.colors.qualitative.Vivid)
            ch(f,"Area vs Price")
        f=px.box(df,x="beds",y="price_lakh",color="beds",color_discrete_sequence=px.colors.sequential.Plasma)
        f.update_layout(**clayout("Price by BHK"),showlegend=False)
        st.plotly_chart(f,use_container_width=True)

    with t2:
        cdf=df.groupby("city").agg(count=("id","count"),avg_price=("price_lakh","mean"),
            avg_rating=("rating","mean"),avg_psf=("price_psf","mean")).reset_index().sort_values("avg_price",ascending=False)
        c1,c2=st.columns(2)
        with c1:
            f=go.Figure(go.Bar(x=cdf["city"],y=cdf["avg_price"].round(1),
                marker=dict(color=cdf["avg_price"],colorscale="Reds",line=dict(width=0)),
                text=cdf["avg_price"].round(0).astype(int),textposition="outside",textfont=dict(color="#9ca3af",size=10)))
            f.update_layout(**clayout("Avg Price by City (L)"),xaxis_tickangle=-40);st.plotly_chart(f,use_container_width=True)
        with c2:
            f=go.Figure(go.Bar(x=cdf["city"],y=cdf["avg_psf"].round(0),
                marker=dict(color=cdf["avg_psf"],colorscale="Teal"),
                text=cdf["avg_psf"].round(0).astype(int),textposition="outside",textfont=dict(color="#9ca3af",size=10)))
            f.update_layout(**clayout("Avg ₹/sqft by City"),xaxis_tickangle=-40);st.plotly_chart(f,use_container_width=True)
        f=go.Figure(go.Scatterpolar(r=cdf["avg_rating"].values,theta=cdf["city"].values,
            fill="toself",fillcolor="rgba(255,56,92,.18)",line=dict(color="#FF385C")))
        f.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",radialaxis=dict(color="#4b5563",gridcolor="rgba(255,255,255,.05)")),
            paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#9ca3af"),
            title=dict(text="City Ratings Radar",font=dict(color="#f9fafb",size=14)))
        st.plotly_chart(f,use_container_width=True)

    with t3:
        c1,c2=st.columns(2)
        with c1:
            tc=df["property_type"].value_counts().reset_index();tc.columns=["type","count"]
            f=go.Figure(go.Pie(labels=tc["type"],values=tc["count"],hole=.5,
                marker=dict(colors=px.colors.qualitative.Vivid,line=dict(color="#0d0b1e",width=2)),textfont=dict(size=11,color="#f9fafb")))
            f.update_layout(paper_bgcolor="rgba(0,0,0,0)",legend=dict(font=dict(color="#9ca3af")),
                title=dict(text="Property Type Mix",font=dict(color="#f9fafb",size=14)))
            st.plotly_chart(f,use_container_width=True)
        with c2:
            sc=df["status"].value_counts().reset_index();sc.columns=["status","count"]
            f=go.Figure(go.Pie(labels=sc["status"],values=sc["count"],hole=.5,
                marker=dict(colors=["#6ee7b7","#93c5fd","#c4b5fd","#fca5a5"],line=dict(color="#0d0b1e",width=2)),textfont=dict(size=11,color="#f9fafb")))
            f.update_layout(paper_bgcolor="rgba(0,0,0,0)",legend=dict(font=dict(color="#9ca3af")),
                title=dict(text="Status Mix",font=dict(color="#f9fafb",size=14)))
            st.plotly_chart(f,use_container_width=True)
        bc=df["beds"].value_counts().sort_index().reset_index();bc.columns=["bhk","count"]
        f=px.bar(bc,x="bhk",y="count",color="bhk",color_continuous_scale="Reds",labels={"bhk":"BHK","count":"Listings"})
        f.update_layout(showlegend=False,**clayout("Bedroom Distribution"));st.plotly_chart(f,use_container_width=True)

    with t4:
        yr=df.groupby("year_built").agg(count=("id","count"),avg_p=("price_lakh","mean")).reset_index()
        f=go.Figure(go.Scatter(x=yr["year_built"],y=yr["avg_p"],mode="lines+markers",
            line=dict(color="#FF385C",width=3),marker=dict(size=7,color="#fca5a5"),name="Avg Price"))
        f.update_layout(**clayout("Avg Price Trend by Build Year"));st.plotly_chart(f,use_container_width=True)
        tb=df.groupby("builder")["price_lakh"].mean().sort_values(ascending=False).head(10).reset_index()
        f=px.bar(tb,y="builder",x="price_lakh",orientation="h",color="price_lakh",color_continuous_scale="Reds",
                 labels={"price_lakh":"Avg Price (L)","builder":"Builder"})
        f.update_layout(showlegend=False,**clayout("Top 10 Builders by Avg Price"))
        f.update_yaxes(autorange="reversed")
        st.plotly_chart(f,use_container_width=True)


# ── FAVORITES ─────────────────────────────────────────────────────────────────
def render_favorites():
    st.markdown('<div class="shdr">Saved Properties</div>',unsafe_allow_html=True)
    favs=get_favorites()
    if not favs:
        st.info("No saved properties yet. Browse listings and click ♡ Save.");return
    df=get_properties();fdf=df[df["id"].isin(favs)].reset_index(drop=True)
    st.markdown(f'<div style="font-size:.8rem;color:#6b7280;margin-bottom:.8rem">{len(fdf)} saved listing{"s" if len(fdf)!=1 else ""}</div>',unsafe_allow_html=True)
    for i in range(0,len(fdf),3):
        cols=st.columns(3)
        for j,(_,row) in enumerate(fdf.iloc[i:i+3].iterrows()):
            with cols[j]: render_card(row)


# ── EMI ───────────────────────────────────────────────────────────────────────
def render_emi():
    st.markdown('<div class="shdr">Home Loan EMI Calculator</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2,gap="large")
    with c1:
        pp=st.number_input("Property Price (Lakhs)",10.0,2000.0,80.0,5.0,key="emipp")
        dp=st.slider("Down Payment (%)",10,50,20,5,key="emidp")
        rt=st.slider("Interest Rate (% p.a.)",6.0,15.0,8.5,.25,key="emirat")
        yr=st.slider("Loan Tenure (Years)",5,30,20,1,key="emiyr")
        loan=pp*(1-dp/100);mo=emi(loan,rt,yr);tot=mo*yr*12;intr=tot-loan*1e5
        st.markdown(f"""
        <div class="emipanel" style="margin-top:1rem">
          <div style="font-size:.68rem;color:#6b7280;text-align:center;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.2rem">Monthly EMI</div>
          <div class="emiamt">₹{mo:,.0f}</div>
          <div style="text-align:center;font-size:.76rem;color:#6b7280;margin-bottom:.9rem">per month for {yr} years</div>
          <div class="emirow"><span>Loan Amount</span><span style="color:#a5b4fc;font-weight:700">₹{loan:.1f} L</span></div>
          <div class="emirow"><span>Total Interest</span><span style="color:#fca5a5;font-weight:700">₹{intr/1e5:.1f} L</span></div>
          <div class="emirow"><span>Total Payment</span><span style="color:#6ee7b7;font-weight:700">₹{tot/1e5:.1f} L</span></div>
        </div>""",unsafe_allow_html=True)
    with c2:
        f=go.Figure(go.Pie(labels=["Principal","Interest"],values=[round(loan*1e5),round(intr)],hole=.55,
            textfont=dict(color="#f9fafb"),
            marker=dict(colors=["#6ee7b7","#FF385C"],line=dict(color="#0d0b1e",width=3))))
        f.update_layout(paper_bgcolor="rgba(0,0,0,0)",legend=dict(font=dict(color="#9ca3af")),
            annotations=[dict(text="Loan<br>Split",x=.5,y=.5,font=dict(color="#f9fafb",size=12),showarrow=False)])
        st.plotly_chart(f,use_container_width=True)
        months=list(range(1,yr*12+1));bal=loan*1e5;r=rt/1200;bals=[]
        for _ in months:
            bal=max(0,bal-(mo-bal*r));bals.append(bal/1e5)
        f2=go.Figure(go.Scatter(x=months,y=bals,fill="tozeroy",
            fillcolor="rgba(255,56,92,.12)",line=dict(color="#FF385C",width=2.5)))
        f2.update_layout(**clayout("Outstanding Balance Over Time"))
        f2.update_xaxes(title_text="Month")
        f2.update_yaxes(title_text="Balance (L)")
        st.plotly_chart(f2,use_container_width=True)


# ── MAIN ──────────────────────────────────────────────────────────────────────
def ensure_demo():
    import os
    if not os.path.exists(os.path.join(os.path.dirname(__file__),"users.json")):
        sign_up("demo","demo123","Demo User")

def main():
    ensure_demo()
    if not is_logged_in():
        render_auth();return
    page,sf=render_sidebar()
    if   page=="Search":         render_search(sf)
    elif page=="Analytics":      render_analytics()
    elif page=="Favorites":      render_favorites()
    elif page=="EMI Calculator": render_emi()

if __name__=="__main__":
    main()