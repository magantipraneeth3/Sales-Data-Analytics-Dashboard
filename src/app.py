import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PRANEETH SALES ANALYTICS DASHBOARD — PREMIUM EDITION
# ============================================================

st.set_page_config(
    page_title="Praneeth Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- THEME ----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --bg:#171A2B;
    --bg2:#1B1F33;
    --panel:#20243A;
    --panel2:#252A43;
    --border:rgba(255,255,255,.07);
    --text:#F7F8FC;
    --muted:#9299B2;
    --purple:#7567F5;
    --purple2:#9B8CFF;
    --cyan:#65D4D2;
    --green:#51D6B2;
    --orange:#FFB86B;
    --pink:#F47BAA;
    --red:#FF7272;
}

*{font-family:'Inter',sans-serif;}
.stApp{
    background:
      radial-gradient(circle at 80% -10%,rgba(117,103,245,.18),transparent 30%),
      radial-gradient(circle at 10% 110%,rgba(101,212,210,.06),transparent 30%),
      var(--bg);
    color:var(--text);
}
.block-container{max-width:1480px;padding:1.1rem 2rem 3rem;}
#MainMenu, footer{visibility:hidden;}
header{background:transparent!important;}
[data-testid="stHeader"]{background:transparent!important;}

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#141727 0%,#171A2B 100%);
    border-right:1px solid rgba(255,255,255,.06);
}
section[data-testid="stSidebar"]>div{padding:1rem .7rem;}
section[data-testid="stSidebar"] *{color:#E9EBF4;}
section[data-testid="stSidebar"] h1{font-size:18px!important;font-weight:800!important;}
section[data-testid="stSidebar"] .stCaption{color:#858CA6!important;}
section[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.07)!important;}

section[data-testid="stSidebar"] div[role="radiogroup"]{gap:4px;}
section[data-testid="stSidebar"] div[role="radiogroup"] label{
    padding:9px 10px;border-radius:9px;transition:.18s;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(117,103,245,.15);
}

div[data-testid="stMetric"]{
    background:linear-gradient(145deg,#22263D,#1E2237);
    border:1px solid var(--border);
    border-radius:14px;
    padding:14px 16px;
    min-height:108px;
    box-shadow:0 12px 30px rgba(0,0,0,.18);
}
div[data-testid="stMetricLabel"]{
    color:#8E95AD!important;
    font-size:10px!important;
    text-transform:uppercase;
    letter-spacing:.8px;
    font-weight:700!important;
}
div[data-testid="stMetricValue"]{
    color:#F7F8FC!important;
    font-size:24px!important;
    font-weight:800!important;
}
div[data-testid="stMetricDelta"]{font-size:10px!important;}

div[data-testid="stPlotlyChart"]{
    background:linear-gradient(145deg,#20243A,#1E2236);
    border:1px solid var(--border);
    border-radius:15px;
    padding:4px;
    box-shadow:0 12px 30px rgba(0,0,0,.14);
}

.stButton button,.stDownloadButton button{
    background:linear-gradient(135deg,#7567F5,#5F51DC)!important;
    border:0!important;border-radius:9px!important;
    color:white!important;font-weight:700!important;
}
.stButton button:hover,.stDownloadButton button:hover{
    box-shadow:0 8px 22px rgba(117,103,245,.3);
}

div[data-baseweb="select"]>div,
div[data-testid="stDateInput"] input{
    background:#20243A!important;
    color:#F7F8FC!important;
    border-color:rgba(255,255,255,.08)!important;
}
div[data-testid="stDataFrame"]{
    border:1px solid var(--border);
    border-radius:13px;
    overflow:hidden;
}
hr{border-color:rgba(255,255,255,.07)!important;}

.hero{
    background:
      radial-gradient(circle at 90% 20%,rgba(117,103,245,.27),transparent 27%),
      linear-gradient(135deg,#242846,#1D2137);
    border:1px solid rgba(255,255,255,.07);
    border-radius:18px;
    padding:24px 26px;
    box-shadow:0 18px 45px rgba(0,0,0,.22);
    margin-bottom:18px;
}
.hero-title{font-size:28px;font-weight:800;color:#fff;letter-spacing:-.8px;}
.hero-subtitle{color:#949BB3;font-size:12px;margin-top:5px;}
.live{
    display:inline-block;margin-top:13px;padding:5px 10px;border-radius:999px;
    background:rgba(81,214,178,.10);color:#51D6B2;font-size:10px;font-weight:800;
    border:1px solid rgba(81,214,178,.2);
}
.section-kicker{color:#7F87A2;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:1.1px;}
.section-title{color:#F7F8FC;font-size:19px;font-weight:800;margin:2px 0 12px;}
.mini-card{
    background:linear-gradient(145deg,#22263D,#1D2135);
    border:1px solid var(--border);border-radius:13px;padding:15px;
    min-height:105px;box-shadow:0 10px 25px rgba(0,0,0,.12);
}
.mini-label{color:#858CA5;font-size:10px;text-transform:uppercase;font-weight:700;}
.mini-value{color:#F7F8FC;font-size:21px;font-weight:800;margin-top:6px;}
.mini-note{color:#5ED6B3;font-size:10px;margin-top:4px;}
.insight{
    background:linear-gradient(145deg,#22263D,#1E2236);
    border:1px solid var(--border);border-left:3px solid var(--purple);
    border-radius:12px;padding:13px 15px;margin-bottom:9px;
}
.insight b{color:#F7F8FC;font-size:12px;}
.insight span{color:#8E95AD;font-size:11px;}
.badge{
    display:inline-block;padding:4px 8px;border-radius:999px;
    background:rgba(117,103,245,.13);color:#A99FFF;font-size:9px;font-weight:800;
}
.footer{color:#666D84;text-align:center;font-size:10px;margin-top:35px;padding-top:15px;border-top:1px solid rgba(255,255,255,.06);}
</style>
""", unsafe_allow_html=True)

PURPLE="#7567F5"
PURPLE2="#9B8CFF"
CYAN="#65D4D2"
GREEN="#51D6B2"
ORANGE="#FFB86B"
PINK="#F47BAA"
RED="#FF7272"

def money(x):
    x=float(x)
    if abs(x)>=1_000_000_000: return f"₹{x/1_000_000_000:.2f}B"
    if abs(x)>=1_000_000: return f"₹{x/1_000_000:.2f}M"
    if abs(x)>=1_000: return f"₹{x/1_000:.1f}K"
    return f"₹{x:,.0f}"

def pct(x): return f"{x:.1f}%"

def chart(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#20243A",
        font=dict(family="Inter",color="#9CA3B8",size=10),
        margin=dict(l=30,r=25,t=25,b=30),
        hoverlabel=dict(bgcolor="#121522",font_color="#fff"),
        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10)),
        xaxis=dict(showgrid=False,zeroline=False,color="#7F87A2"),
        yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,.055)",zeroline=False,color="#7F87A2")
    )
    return fig

def title(kicker, title):
    st.markdown(f'<div class="section-kicker">{kicker}</div><div class="section-title">{title}</div>',unsafe_allow_html=True)

# ------------------------- DATA -----------------------------

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_FILE=BASE_DIR/"data"/"processed"/"clean_sales_data.csv"
FORECAST_FILE=BASE_DIR/"outputs"/"monthly_forecast.csv"
METRICS_FILE=BASE_DIR/"outputs"/"sales_prediction_metrics.csv"

if not DATA_FILE.exists():
    st.error("Dataset not found. Run `python3 src/data_cleaning.py` first.")
    st.stop()

@st.cache_data
def load_data():
    d=pd.read_csv(DATA_FILE)
    d["Sale_Date"]=pd.to_datetime(d["Sale_Date"],errors="coerce")
    for c in ["Quantity_Sold","Unit_Cost","Unit_Price","Discount","Revenue","Profit"]:
        if c in d: d[c]=pd.to_numeric(d[c],errors="coerce").fillna(0)
    # Rebuild economics consistently.
    d["Revenue"]=d["Quantity_Sold"]*d["Unit_Price"]
    d["Cost"]=d["Quantity_Sold"]*d["Unit_Cost"]
    d["Profit"]=d["Revenue"]-d["Cost"]
    d["Profit_Margin"]=np.where(d["Revenue"]!=0,d["Profit"]/d["Revenue"]*100,0)
    d["Month_Start"]=d["Sale_Date"].dt.to_period("M").dt.to_timestamp()
    return d

df=load_data()

# ------------------------- SIDEBAR --------------------------

with st.sidebar:
    st.markdown("### ◉ PRANEETH")
    st.caption("SALES ANALYTICS")
    st.divider()

    page=st.radio(
        "Navigation",
        ["🏠 Executive Overview","📈 Sales Analytics","🔮 Forecast & Targets",
         "📦 Product Intelligence","👥 Customer Intelligence","🏆 Team Performance",
         "🧭 Geo & Channel","🔎 Data Explorer","💡 Insights & Alerts"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**GLOBAL FILTERS**")

    min_date=df.Sale_Date.min().date()
    max_date=df.Sale_Date.max().date()
    dates=st.date_input("Date range",(min_date,max_date),min_value=min_date,max_value=max_date)

    def multi(label,col):
        vals=sorted(df[col].dropna().unique().tolist())
        return st.multiselect(label,vals,default=vals)

    regions=multi("Region","Region")
    categories=multi("Category","Product_Category")
    channels=multi("Channel","Sales_Channel")
    reps=multi("Sales Rep","Sales_Rep")
    customer_types=multi("Customer Type","Customer_Type")

    st.divider()
    st.caption(f"{len(df):,} source transactions")
    st.caption(f"{min_date:%d %b %Y} → {max_date:%d %b %Y}")

# Apply filters
data=df.copy()
if isinstance(dates,(tuple,list)) and len(dates)==2:
    data=data[(data.Sale_Date>=pd.Timestamp(dates[0]))&(data.Sale_Date<=pd.Timestamp(dates[1]))]
data=data[
    data.Region.isin(regions)&
    data.Product_Category.isin(categories)&
    data.Sales_Channel.isin(channels)&
    data.Sales_Rep.isin(reps)&
    data.Customer_Type.isin(customer_types)
]
if data.empty:
    st.warning("No records match the current filters.")
    st.stop()

# ------------------------- HEADER ---------------------------

st.markdown("""
<div class="hero">
  <div class="hero-title">Praneeth Sales Analytics Dashboard</div>
  <div class="hero-subtitle">Executive command center for revenue, profitability, forecasting and sales performance</div>
  <span class="live">● LIVE DATA</span>
</div>
""",unsafe_allow_html=True)

revenue=data.Revenue.sum()
profit=data.Profit.sum()
orders=len(data)
units=data.Quantity_Sold.sum()
margin=profit/revenue*100 if revenue else 0
aov=revenue/orders if orders else 0

k1,k2,k3,k4,k5,k6=st.columns(6)
for col,label,value in [
    (k1,"Revenue",money(revenue)),
    (k2,"Gross Profit",money(profit)),
    (k3,"Orders",f"{orders:,}"),
    (k4,"Units Sold",f"{units:,.0f}"),
    (k5,"Profit Margin",pct(margin)),
    (k6,"Avg Order Value",money(aov))
]:
    with col: st.metric(label,value)

# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page=="🏠 Executive Overview":
    st.markdown("<br>",unsafe_allow_html=True)
    title("PERFORMANCE","Revenue, Profit & Growth")

    monthly=data.groupby("Month_Start").agg(
        Revenue=("Revenue","sum"),Profit=("Profit","sum"),Orders=("Product_ID","count")
    ).reset_index()

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=monthly.Month_Start,y=monthly.Revenue,name="Revenue",
                             mode="lines+markers",line=dict(color=PURPLE,width=3),marker=dict(size=6),
                             fill="tozeroy",fillcolor="rgba(117,103,245,.10)"))
    fig.add_trace(go.Scatter(x=monthly.Month_Start,y=monthly.Profit,name="Profit",
                             mode="lines+markers",line=dict(color=CYAN,width=3),marker=dict(size=6)))
    chart(fig,400)
    fig.update_yaxes(tickprefix="₹",tickformat=",.2s")
    st.plotly_chart(fig,use_container_width=True)

    c1,c2,c3=st.columns([1.1,1.1,.8])
    with c1:
        title("REGION","Revenue by Region")
        r=data.groupby("Region").Revenue.sum().sort_values()
        f=px.bar(x=r.values,y=r.index,orientation="h")
        f.update_traces(marker_color=PURPLE,text=[money(x) for x in r.values],textposition="outside")
        chart(f,320); f.update_xaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)
    with c2:
        title("CATEGORY","Revenue by Category")
        c=data.groupby("Product_Category").Revenue.sum().sort_values(ascending=False)
        f=px.bar(x=c.index,y=c.values,text=c.values)
        f.update_traces(marker_color=CYAN,texttemplate="₹%{y:.2s}",textposition="outside")
        chart(f,320); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)
    with c3:
        title("CHANNEL","Sales Mix")
        ch=data.groupby("Sales_Channel").Revenue.sum().reset_index()
        f=px.pie(ch,names="Sales_Channel",values="Revenue",hole=.68)
        f.update_traces(marker=dict(colors=[PURPLE,CYAN,PINK]),textinfo="label+percent")
        chart(f,320)
        st.plotly_chart(f,use_container_width=True)

    c1,c2=st.columns(2)
    with c1:
        title("TREND","Orders by Month")
        f=px.area(monthly,x="Month_Start",y="Orders")
        f.update_traces(line_color=ORANGE,fillcolor="rgba(255,184,107,.10)")
        chart(f,300)
        st.plotly_chart(f,use_container_width=True)
    with c2:
        title("MARGIN","Profit Margin by Category")
        cm=data.groupby("Product_Category").agg(Revenue=("Revenue","sum"),Profit=("Profit","sum")).reset_index()
        cm["Margin"]=np.where(cm.Revenue!=0,cm.Profit/cm.Revenue*100,0)
        f=px.bar(cm.sort_values("Margin"),x="Margin",y="Product_Category",orientation="h")
        f.update_traces(marker_color=GREEN,texttemplate="%{x:.1f}%",textposition="outside")
        chart(f,300); f.update_xaxes(ticksuffix="%")
        st.plotly_chart(f,use_container_width=True)

# ============================================================
# SALES ANALYTICS
# ============================================================

elif page=="📈 Sales Analytics":
    title("ANALYTICS","Sales Performance Center")
    monthly=data.groupby("Month_Start").agg(Revenue=("Revenue","sum"),Profit=("Profit","sum"),Orders=("Product_ID","count"),Units=("Quantity_Sold","sum")).reset_index()

    tabs=st.tabs(["Revenue & Profit","Discount Analysis","Payment & Channel","Daily Performance"])

    with tabs[0]:
        f=go.Figure()
        f.add_trace(go.Bar(x=monthly.Month_Start,y=monthly.Revenue,name="Revenue",marker_color=PURPLE))
        f.add_trace(go.Scatter(x=monthly.Month_Start,y=monthly.Profit,name="Profit",mode="lines+markers",line=dict(color=GREEN,width=3)))
        chart(f,430); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)

    with tabs[1]:
        disc=data.groupby("Discount").agg(Revenue=("Revenue","sum"),Margin=("Profit_Margin","mean")).reset_index()
        disc["Discount %"]=disc["Discount"]*100
        f=px.scatter(disc,x="Discount %",y="Revenue",size="Margin",color="Margin",color_continuous_scale=["#7567F5","#65D4D2","#51D6B2"])
        chart(f,400); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)
        st.caption("Use this view to identify whether deeper discounts are associated with stronger revenue.")

    with tabs[2]:
        a,b=st.columns(2)
        with a:
            p=data.groupby("Payment_Method").Revenue.sum().sort_values()
            f=px.bar(x=p.values,y=p.index,orientation="h")
            f.update_traces(marker_color=CYAN)
            chart(f,350); f.update_xaxes(tickprefix="₹",tickformat=",.2s")
            st.plotly_chart(f,use_container_width=True)
        with b:
            p=data.groupby("Sales_Channel").agg(Revenue=("Revenue","sum"),Profit=("Profit","sum")).reset_index()
            f=px.bar(p,x="Sales_Channel",y=["Revenue","Profit"],barmode="group")
            f.update_traces(marker_color=PURPLE)
            chart(f,350); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
            st.plotly_chart(f,use_container_width=True)

    with tabs[3]:
        daily=data.groupby("Sale_Date").agg(Revenue=("Revenue","sum"),Orders=("Product_ID","count")).reset_index()
        f=px.line(daily,x="Sale_Date",y="Revenue",markers=True)
        f.update_traces(line_color=CYAN)
        chart(f,400); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)

# ============================================================
# FORECAST & TARGETS
# ============================================================

elif page=="🔮 Forecast & Targets":
    title("PREDICTIVE ANALYTICS","Forecast & Target Center")

    if FORECAST_FILE.exists():
        fc=pd.read_csv(FORECAST_FILE)
        fc["Date"]=pd.to_datetime(fc["Date"])
        actual=fc[fc["Type"].astype(str).str.lower().eq("actual")]
        future=fc[~fc["Type"].astype(str).str.lower().eq("actual")]

        f=go.Figure()
        if not actual.empty:
            f.add_trace(go.Scatter(x=actual.Date,y=actual.Revenue,name="Actual",mode="lines+markers",line=dict(color=PURPLE,width=3)))
        if not future.empty:
            f.add_trace(go.Scatter(x=future.Date,y=future.Revenue,name="Forecast",mode="lines+markers",line=dict(color=CYAN,width=3,dash="dash")))
        chart(f,430); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)

        if not future.empty:
            next_forecast=future.Revenue.sum()
            last_actual=actual.Revenue.tail(3).mean() if not actual.empty else 0
            q1,q2,q3=st.columns(3)
            q1.metric("Forecast Revenue",money(next_forecast))
            q2.metric("Forecast Periods",f"{len(future)}")
            q3.metric("vs Recent Avg",pct((next_forecast/(last_actual*len(future))-1)*100) if last_actual else "0%")

    target=st.number_input("Set revenue target",min_value=0.0,value=float(max(revenue,1)*1.10),step=100000.0)
    progress=min(revenue/target,1) if target else 0
    st.progress(progress)
    a,b,c=st.columns(3)
    a.metric("Current Revenue",money(revenue))
    b.metric("Target",money(target))
    c.metric("Gap",money(max(target-revenue,0)))

    if METRICS_FILE.exists():
        m=pd.read_csv(METRICS_FILE).iloc[0]
        st.markdown("<br>",unsafe_allow_html=True)
        title("MODEL HEALTH","Prediction Model Performance")
        a,b,c=st.columns(3)
        a.metric("MAE",f"{m.get('MAE',0):,.2f}")
        b.metric("RMSE",f"{m.get('RMSE',0):,.2f}")
        c.metric("R²",f"{m.get('R2',0):.4f}")

# ============================================================
# PRODUCT INTELLIGENCE
# ============================================================

elif page=="📦 Product Intelligence":
    title("PORTFOLIO","Product Intelligence")

    p=data.groupby("Product_ID").agg(
        Revenue=("Revenue","sum"),Profit=("Profit","sum"),Units=("Quantity_Sold","sum")
    ).reset_index()
    p["Margin"]=np.where(p.Revenue!=0,p.Profit/p.Revenue*100,0)

    a,b=st.columns(2)
    with a:
        top=p.nlargest(12,"Revenue").sort_values("Revenue")
        f=px.bar(top,x="Revenue",y="Product_ID",orientation="h")
        f.update_traces(marker_color=PURPLE)
        chart(f,450); f.update_xaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)
    with b:
        f=px.scatter(p,x="Revenue",y="Profit",size="Units",color="Margin",hover_name="Product_ID",
                     color_continuous_scale=["#F47BAA","#7567F5","#51D6B2"])
        chart(f,450); f.update_xaxes(tickprefix="₹",tickformat=",.2s"); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)

    title("PRODUCT TABLE","Sortable Product Performance")
    st.dataframe(p.sort_values("Revenue",ascending=False),use_container_width=True,hide_index=True)

# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

elif page=="👥 Customer Intelligence":
    title("CUSTOMERS","Customer Intelligence")

    cust=data.groupby("Customer_Type").agg(
        Revenue=("Revenue","sum"),Profit=("Profit","sum"),Orders=("Product_ID","count"),Units=("Quantity_Sold","sum")
    ).reset_index()
    cust["AOV"]=cust.Revenue/cust.Orders
    cust["Margin"]=np.where(cust.Revenue!=0,cust.Profit/cust.Revenue*100,0)

    a,b=st.columns(2)
    with a:
        f=px.bar(cust,x="Customer_Type",y="Revenue",text="Revenue")
        f.update_traces(marker_color=PURPLE,texttemplate="₹%{y:.2s}",textposition="outside")
        chart(f,350); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)
    with b:
        f=px.bar(cust,x="Customer_Type",y="AOV",text="AOV")
        f.update_traces(marker_color=CYAN,texttemplate="₹%{y:.2s}",textposition="outside")
        chart(f,350); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)

    st.dataframe(cust,use_container_width=True,hide_index=True)

# ============================================================
# TEAM PERFORMANCE
# ============================================================

elif page=="🏆 Team Performance":
    title("PEOPLE","Sales Representative Leaderboard")

    team=data.groupby("Sales_Rep").agg(
        Revenue=("Revenue","sum"),Profit=("Profit","sum"),Orders=("Product_ID","count"),Units=("Quantity_Sold","sum")
    ).reset_index()
    team["Margin"]=np.where(team.Revenue!=0,team.Profit/team.Revenue*100,0)
    team["AOV"]=team.Revenue/team.Orders
    team=team.sort_values("Revenue",ascending=False)
    team["Rank"]=range(1,len(team)+1)

    top=team.head(3)
    a,b,c=st.columns(3)
    for col,(_,r),medal in zip([a,b,c],top.iterrows(),["🥇","🥈","🥉"]):
        with col:
            st.markdown(f'<div class="mini-card"><div class="mini-label">{medal} RANK {int(r.Rank)}</div><div class="mini-value">{r.Sales_Rep}</div><div class="mini-note">{money(r.Revenue)} revenue · {r.Margin:.1f}% margin</div></div>',unsafe_allow_html=True)

    f=px.bar(team.sort_values("Revenue"),x="Revenue",y="Sales_Rep",orientation="h",text="Revenue")
    f.update_traces(marker_color=PURPLE,texttemplate="₹%{x:.2s}",textposition="outside")
    chart(f,470); f.update_xaxes(tickprefix="₹",tickformat=",.2s")
    st.plotly_chart(f,use_container_width=True)
    st.dataframe(team,use_container_width=True,hide_index=True)

# ============================================================
# GEO & CHANNEL
# ============================================================

elif page=="🧭 Geo & Channel":
    title("DISTRIBUTION","Geography & Channel Intelligence")

    geo=data.groupby("Region").agg(Revenue=("Revenue","sum"),Profit=("Profit","sum"),Orders=("Product_ID","count")).reset_index()
    geo["Margin"]=geo.Profit/geo.Revenue*100

    a,b=st.columns(2)
    with a:
        f=px.bar(geo.sort_values("Revenue"),x="Revenue",y="Region",orientation="h")
        f.update_traces(marker_color=PURPLE)
        chart(f,380); f.update_xaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)
    with b:
        f=px.scatter(geo,x="Revenue",y="Profit",size="Orders",color="Margin",text="Region",
                     color_continuous_scale=["#F47BAA","#7567F5","#51D6B2"])
        f.update_traces(textposition="top center")
        chart(f,380); f.update_xaxes(tickprefix="₹",tickformat=",.2s"); f.update_yaxes(tickprefix="₹",tickformat=",.2s")
        st.plotly_chart(f,use_container_width=True)

    st.dataframe(geo.sort_values("Revenue",ascending=False),use_container_width=True,hide_index=True)

# ============================================================
# DATA EXPLORER
# ============================================================

elif page=="🔎 Data Explorer":
    title("DATA","Interactive Data Explorer")
    search=st.text_input("Search rows by Product ID, Sales Rep, Region or Category")
    view=data.copy()
    if search:
        mask=view.astype(str).apply(lambda s:s.str.contains(search,case=False,na=False)).any(axis=1)
        view=view[mask]

    numeric=view.select_dtypes(include=np.number).columns.tolist()
    selected_cols=st.multiselect("Columns",view.columns.tolist(),default=view.columns.tolist()[:10])
    if selected_cols: view=view[selected_cols]

    st.caption(f"Showing {len(view):,} filtered rows")
    st.dataframe(view,use_container_width=True,hide_index=True,height=500)

    csv=view.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Export Filtered CSV",csv,"praneeth_sales_filtered.csv","text/csv")

# ============================================================
# INSIGHTS & ALERTS
# ============================================================

else:
    title("DECISION SUPPORT","Insights & Alerts")

    region=data.groupby("Region").Revenue.sum().sort_values(ascending=False)
    cat=data.groupby("Product_Category").Revenue.sum().sort_values(ascending=False)
    rep=data.groupby("Sales_Rep").Revenue.sum().sort_values(ascending=False)

    insights=[
        ("🌎 Leading Region",f"{region.index[0]} contributes {money(region.iloc[0])} in revenue."),
        ("📦 Leading Category",f"{cat.index[0]} is the highest-revenue category at {money(cat.iloc[0])}."),
        ("🏆 Top Sales Rep",f"{rep.index[0]} leads the filtered period with {money(rep.iloc[0])}."),
        ("💰 Overall Margin",f"Current filtered profit margin is {margin:.1f}%."),
    ]
    for head,body in insights:
        st.markdown(f'<div class="insight"><b>{head}</b><br><span>{body}</span></div>',unsafe_allow_html=True)

    low_margin=data.groupby("Product_Category").agg(Revenue=("Revenue","sum"),Profit=("Profit","sum")).reset_index()
    low_margin["Margin"]=low_margin.Profit/low_margin.Revenue*100
    low=low_margin.sort_values("Margin").iloc[0]

    if low.Margin<10:
        st.warning(f"⚠️ Attention: {low.Product_Category} has the lowest category margin at {low.Margin:.1f}%. Review pricing, cost and discount levels.")

    high_discount=data[data.Discount>=0.20]
    if not high_discount.empty:
        st.info(f"🎯 {len(high_discount):,} transactions use discounts of 20% or more. Review whether these discounts are improving volume enough to justify margin pressure.")

    st.subheader("Category Profitability")
    f=px.bar(low_margin.sort_values("Margin"),x="Margin",y="Product_Category",orientation="h")
    f.update_traces(marker_color=GREEN,texttemplate="%{x:.1f}%",textposition="outside")
    chart(f,380); f.update_xaxes(ticksuffix="%")
    st.plotly_chart(f,use_container_width=True)

# ------------------------- EXPORT ----------------------------

st.divider()
a,b=st.columns([4,1])
with a:
    st.markdown("**Praneeth Sales Analytics Dashboard**  \nFiltered data, predictive analytics and executive reporting in one place.")
with b:
    csv=data.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Export CSV",csv,"praneeth_sales_filtered.csv","text/csv",use_container_width=True)

st.markdown('<div class="footer">PRANEETH SALES ANALYTICS DASHBOARD · Streamlit · Pandas · Plotly · Machine Learning</div>',unsafe_allow_html=True)