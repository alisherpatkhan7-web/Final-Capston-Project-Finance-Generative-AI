import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import pandas as pd

# --- 1. CONFIGURATION ---
API_KEY = "AIzaSyC2fnZFPq59Ly3AAyRCwZbZeCY74Lq6hgk" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI Stock Pro Analyst", layout="wide", page_icon="🚀")

# --- 2. ADVANCED UI (All Corners Colorful & High Contrast Fonts) ---
st.markdown("""
    <style>
    /* Full Background with Neon Border Effect */
    .stApp {
        background: radial-gradient(circle, #1a1a2e 0%, #0f0f1b 100%);
        color: #FFFFFF !important;
        border: 10px solid transparent;
        border-image: linear-gradient(45deg, #00d4ff, #ab63ff, #00ffcc, #ff00ff) 1;
    }
    
    /* Making all text Bright White for visibility */
    h1, h2, h3, p, span, label, .stMetric label {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* Metric Boxes - High Contrast Glass */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
    }
    
    /* Metric Delta (Percentage) Visibility */
    [data-testid="stMetricDelta"] svg { fill: white !important; }
    
    /* News Cards Styling */
    .news-card {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid rgba(0, 212, 255, 0.5);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        color: white !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 27, 0.9) !important;
        border-right: 2px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---

def fetch_data(ticker, period):
    try:
        df = yf.download(ticker, period=period)
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/(loss+0.00001))))
        return df
    except: return None

# --- 4. UI LAYOUT ---

st.markdown("<h1 style='text-align: center; font-size: 50px; text-shadow: 2px 2px #00d4ff;'>💎 AI STOCK PRO INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Live Market Analytics & Generative AI News Insights</p>", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.markdown("## ⚙️ CONFIG PANEL")
    ticker = st.text_input("ENTER TICKER:", "RELIANCE.NS")
    period = st.selectbox("TIMELINE:", ["6mo", "1y", "2y"])
    run_btn = st.button("🚀 ANALYZE NOW", use_container_width=True)

if run_btn:
    with st.spinner('Generating Colorful Visuals...'):
        df = fetch_data(ticker, period)
        
        if df is not None:
            # PHASE 1: TOP METRICS (High Visibility)
            last_p = float(df['Close'].iloc[-1])
            prev_p = float(df['Close'].iloc[-2])
            pct = ((last_p - prev_p) / prev_p) * 100
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("LIVE PRICE", f"₹{last_p:.2f}", f"{pct:+.2f}%")
            m2.metric("MOMENTUM (RSI)", f"{df['RSI'].iloc[-1]:.1f}")
            m3.metric("MARKET TREND", "BULLISH 📈" if last_p > df['MA20'].iloc[-1] else "BEARISH 📉")
            m4.metric("VOLATILITY", "STABLE" if abs(pct) < 2 else "HIGH")

            st.divider()

            # PHASE 2: VISUAL CHARTS & AI
            col_chart, col_ai = st.columns([2, 1])

            with col_chart:
                st.subheader("📊 PRICE ACTION & MOMENTUM")
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])
                
                # Main Price Trace
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="PRICE", line=dict(color='#00d4ff', width=3)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="TREND", line=dict(color='#ffaa00', dash='dot')), row=1, col=1)
                
                # RSI Trace
                fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI", line=dict(color='#ab63ff', width=2)), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                
                fig.update_layout(height=550, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

            with col_ai:
                st.subheader("🤖 AI SMART INSIGHTS")
                try:
                    news = yf.Ticker(ticker).news[:3]
                    if news:
                        for n in news:
                            title = n.get('title') or "Market Update"
                            st.markdown(f"<div class='news-card'><b>📰 {title}</b></div>", unsafe_allow_html=True)
                            
                            # AI call
                            try:
                                prompt = f"Quick 1-line impact of this stock news: {title}"
                                res = model.generate_content(prompt)
                                st.markdown(f"<p style='color:#00ffcc;'>✨ {res.text}</p>", unsafe_allow_html=True)
                            except:
                                st.warning("AI is busy.")
                    else:
                        st.info("No fresh news.")
                except:
                    st.error("News Load Error.")
        else:
            st.error("Invalid Symbol! Please use RELIANCE.NS or AAPL.")