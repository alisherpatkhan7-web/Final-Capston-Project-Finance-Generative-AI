import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import pandas as pd


try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY")
except:
    API_KEY = None

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

st.set_page_config(page_title="AI Stock Pro Analyst", layout="wide", page_icon="🚀")


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Space+Mono:wght@400;700&display=swap');
    
    /* Light Premium Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 50%, #e8ebff 100%);
        color: #1a1a3a !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Title Styling */
    h1 {
        color: #1a1a3a !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        letter-spacing: 2px !important;
        background: linear-gradient(135deg, #4a7c99, #6b5b95, #2c8c99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 3s ease-in-out infinite;
    }

    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(74, 124, 153, 0.2); }
        50% { text-shadow: 0 0 40px rgba(107, 91, 149, 0.2); }
    }
    
    /* Headings */
    h2, h3, h4 {
        color: #2c3e70 !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
    }

    p, span, label {
        color: #4a5f7f !important;
        font-weight: 400 !important;
    }

    /* Premium Metric Boxes with Glass Morphism - Light */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(107, 91, 149, 0.08), rgba(74, 124, 153, 0.08)) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(74, 124, 153, 0.2) !important;
        border-radius: 25px !important;
        padding: 30px !important;
        box-shadow: 0 8px 32px rgba(74, 124, 153, 0.1), inset 0 0 20px rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        background: linear-gradient(135deg, rgba(107, 91, 149, 0.15), rgba(74, 124, 153, 0.15)) !important;
        border-color: rgba(74, 124, 153, 0.4) !important;
        box-shadow: 0 12px 48px rgba(74, 124, 153, 0.2), inset 0 0 30px rgba(255, 255, 255, 0.9);
    }

    /* Metric Label & Value */
    [data-testid="stMetricLabel"] {
        color: #4a7c99 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase;
    }

    [data-testid="stMetricValue"] {
        color: #2c5f99 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Metric Delta (Percentage) */
    [data-testid="stMetricDelta"] {
        color: #2c5f99 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] svg { fill: #2c5f99 !important; }
    
    /* Premium News Cards - Light */
    .news-card {
        background: linear-gradient(135deg, rgba(74, 124, 153, 0.08), rgba(107, 91, 149, 0.08)) !important;
        backdrop-filter: blur(15px) !important;
        border: 2px solid rgba(74, 124, 153, 0.2) !important;
        border-radius: 18px !important;
        padding: 20px !important;
        margin-bottom: 18px !important;
        color: #1a1a3a !important;
        box-shadow: 0 8px 24px rgba(74, 124, 153, 0.08), inset 0 0 15px rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }

    .news-card:hover {
        border-color: rgba(74, 124, 153, 0.4) !important;
        box-shadow: 0 12px 36px rgba(74, 124, 153, 0.15), inset 0 0 20px rgba(255, 255, 255, 0.9);
        background: linear-gradient(135deg, rgba(74, 124, 153, 0.15), rgba(107, 91, 149, 0.12)) !important;
        transform: translateY(-5px);
    }

    .news-card b {
        color: #2c5f99 !important;
        font-weight: 700 !important;
    }
    
    /* Premium Sidebar - Light */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(248, 249, 255, 0.98), rgba(240, 242, 255, 0.95)) !important;
        border-right: 2px solid rgba(74, 124, 153, 0.2);
        backdrop-filter: blur(10px);
    }

    section[data-testid="stSidebar"] [data-testid="stDecoratedTextInput"] {
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1.5px solid rgba(74, 124, 153, 0.25) !important;
        border-radius: 12px !important;
        color: #1a1a3a !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSelectbox"] {
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1.5px solid rgba(74, 124, 153, 0.25) !important;
        border-radius: 12px !important;
    }

    /* Premium Button - Light */
    button {
        background: linear-gradient(135deg, #4a7c99, #6b5b95) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 12px 25px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(74, 124, 153, 0.2);
    }

    button:hover {
        box-shadow: 0 8px 40px rgba(74, 124, 153, 0.4), 0 0 30px rgba(107, 91, 149, 0.3);
        transform: translateY(-2px);
        background: linear-gradient(135deg, #5a8ca9, #7b6ba5) !important;
    }

    /* Divider Enhancement */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(74, 124, 153, 0.3), transparent);
    }

    /* Subheader Style */
    h3[data-testid="stHeading"] {
        background: linear-gradient(135deg, #4a7c99, #6b5b95);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Input Fields */
    input {
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1.5px solid rgba(74, 124, 153, 0.25) !important;
        color: #1a1a3a !important;
        border-radius: 12px !important;
    }

    input:focus {
        border-color: rgba(74, 124, 153, 0.5) !important;
        box-shadow: 0 0 20px rgba(74, 124, 153, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)



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



st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <h1 style='margin: 0; font-size: 3.5rem; background: linear-gradient(135deg, #4a7c99, #6b5b95, #2c8c99); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>💎 AI STOCK PRO INTELLIGENCE</h1>
        <p style='text-align: center; font-size: 1.2rem; color: #4a7c99; margin-top: 15px; letter-spacing: 1px;'>⚡ Live Market Analytics & Generative AI News Insights ⚡</p>
        <p style='text-align: center; font-size: 0.9rem; color: #2c5f99; margin-top: 8px;'>Real-time Stock Analysis • AI-Powered Predictions • Market Intelligence</p>
    </div>
""", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h2 style='color: #2c5f99; font-size: 1.5rem; margin: 0;'>⚙️ CONFIG PANEL</h2>
            <p style='color: #4a7c99; font-size: 0.85rem; margin-top: 8px;'>Customize your analysis</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    ticker = st.text_input("🔍 Enter Stock Ticker:", "RELIANCE.NS", placeholder="e.g., RELIANCE.NS, AAPL")
    period = st.selectbox("📅 Select Timeline:", ["6mo", "1y", "2y"], index=0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🚀 ANALYZE NOW", use_container_width=True, key="analyze_btn")

if run_btn:
    with st.spinner('Generating Colorful Visuals...'):
        df = fetch_data(ticker, period)
        
        if df is not None:
           
            last_p = float(df['Close'].iloc[-1])
            prev_p = float(df['Close'].iloc[-2])
            pct = ((last_p - prev_p) / prev_p) * 100
            
            st.markdown("""
                <div style='text-align: center; margin-bottom: 20px;'>
                    <h3 style='color: #2c5f99; font-size: 1.2rem; letter-spacing: 1px;'>📊 MARKET METRICS DASHBOARD</h3>
                </div>
            """, unsafe_allow_html=True)
            
            m1, m2, m3, m4 = st.columns(4, gap="medium")
            
            with m1:
                m1.metric("LIVE PRICE", f"₹{last_p:.2f}", f"{pct:+.2f}%")
            with m2:
                m2.metric("MOMENTUM (RSI)", f"{df['RSI'].iloc[-1]:.1f}", "⚡")
            with m3:
                trend_text = "BULLISH 📈" if last_p > df['MA20'].iloc[-1] else "BEARISH 📉"
                m3.metric("MARKET TREND", trend_text, "-")
            with m4:
                vol_status = "STABLE" if abs(pct) < 2 else "HIGH"
                m4.metric("VOLATILITY", vol_status, "✓")

            st.markdown("<br>", unsafe_allow_html=True)
            st.divider()
            st.markdown("<br>", unsafe_allow_html=True)

          
            col_chart, col_ai = st.columns([2, 1], gap="large")

            with col_chart:
                st.markdown("""
                    <div style='background: rgba(74, 124, 153, 0.08); border-left: 4px solid #4a7c99; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                        <h3 style='color: #2c5f99; margin: 0; font-size: 1.3rem;'>📊 PRICE ACTION & MOMENTUM</h3>
                        <p style='color: #4a7c99; margin: 5px 0 0 0; font-size: 0.9rem;'>Interactive Technical Analysis</p>
                    </div>
                """, unsafe_allow_html=True)
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])
                
                
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="PRICE", line=dict(color='#4a7c99', width=3)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="TREND (MA20)", line=dict(color='#e07a5f', dash='dot', width=2)), row=1, col=1)
                
             
                fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI (14)", line=dict(color='#6b5b95', width=2)), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="rgba(220, 100, 100, 0.5)", row=2, col=1, annotation_text="Overbought")
                fig.add_hline(y=30, line_dash="dash", line_color="rgba(100, 150, 100, 0.5)", row=2, col=1, annotation_text="Oversold")
                
                fig.update_xaxes(gridcolor='rgba(100, 100, 150, 0.15)')
                fig.update_yaxes(gridcolor='rgba(100, 100, 150, 0.15)')
                fig.update_layout(height=600, template="plotly", paper_bgcolor='rgba(248, 249, 255, 0.8)', plot_bgcolor='rgba(255, 255, 255, 0.5)', 
                                hovermode='x unified', margin=dict(l=50, r=50, t=50, b=50))
                st.plotly_chart(fig, use_container_width=True)

            with col_ai:
                st.markdown("""
                    <div style='background: rgba(107, 91, 149, 0.08); border-left: 4px solid #6b5b95; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                        <h3 style='color: #2c5f99; margin: 0; font-size: 1.3rem;'>🤖 AI INSIGHTS</h3>
                        <p style='color: #4a7c99; margin: 5px 0 0 0; font-size: 0.9rem;'>Powered by Gemini AI</p>
                    </div>
                """, unsafe_allow_html=True)
                
                try:
                    news = yf.Ticker(ticker).news[:3]
                    if news:
                        for i, n in enumerate(news, 1):
                            title = n.get('title') or "Market Update"
                            st.markdown(f"""
                                <div class='news-card'>
                                    <b>📰 {i}. {title[:60]}...</b>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # AI call
                            try:
                                prompt = f"Quick 1-line impact of this stock news: {title}"
                                if model is not None:
                                    res = model.generate_content(prompt)
                                    st.markdown(f"<p style='color:#2c5f99; padding: 10px; background: rgba(74, 124, 153, 0.08); border-radius: 8px; margin-top: 8px;'>✨ {res.text}</p>", unsafe_allow_html=True)
                                else:
                                    st.info("🔑 Configure GOOGLE_API_KEY in Streamlit secrets for AI insights")
                            except:
                                st.warning("🔄 AI is processing...")
                    else:
                        st.info("📡 No recent news available")
                except:
                    st.error("❌ News Load Error")
        else:
            st.error("❌ Invalid Symbol! Please try RELIANCE.NS, INFY.NS, or AAPL")
            st.markdown("""
                <div style='background: rgba(220, 100, 100, 0.08); border: 2px solid rgba(220, 100, 100, 0.2); border-radius: 12px; padding: 20px; text-align: center;'>
                    <p style='color: #c9714c; font-size: 1rem;'>📝 Tip: Use proper ticker symbols</p>
                    <p style='color: #4a7c99; font-size: 0.9rem;'>Indian stocks: Add .NS or .BO suffix (e.g., RELIANCE.NS)</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("""
    <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, rgba(74, 124, 153, 0.08), rgba(107, 91, 149, 0.08)); border-radius: 15px; margin-top: 30px;'>
        <p style='color: #2c5f99; font-size: 1rem; margin: 5px 0; font-weight: 700;'>💡 AI STOCK PRO INTELLIGENCE</p>
        <p style='color: #4a7c99; font-size: 0.85rem; margin: 5px 0;'>Powered by Gemini AI • Real-time Data • Advanced Analytics</p>
        <p style='color: #808080; font-size: 0.75rem; margin-top: 15px;'>⚠️ Disclaimer: For educational purposes only. Always consult a financial advisor before trading.</p>
    </div>
""", unsafe_allow_html=True)
