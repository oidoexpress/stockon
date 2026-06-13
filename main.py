import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="AI 주식 분석기",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI 주식 분석기")

ticker = st.text_input(
    "주식 티커 입력 (예: AAPL, TSLA, NVDA)",
    "AAPL"
).upper()

if st.button("분석하기"):

    try:
        stock = yf.Ticker(ticker)

        info = stock.info

        st.subheader(f"{info.get('longName', ticker)}")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "현재가",
            f"${info.get('currentPrice', 'N/A')}"
        )

        col2.metric(
            "시가총액",
            f"${info.get('marketCap', 0):,}"
        )

        col3.metric(
            "PER",
            info.get('trailingPE', 'N/A')
        )

        data = stock.history(period="1y")

        st.subheader("📊 최근 1년 주가")

        data["MA20"] = data["Close"].rolling(20).mean()
        data["MA50"] = data["Close"].rolling(50).mean()

        st.line_chart(
            data[["Close", "MA20", "MA50"]]
        )

        high = data["High"].max()
        low = data["Low"].min()

        st.subheader("📌 핵심 지표")

        st.write(f"1년 최고가 : ${high:.2f}")
        st.write(f"1년 최저가 : ${low:.2f}")

        current = data["Close"].iloc[-1]
        ma20 = data["MA20"].iloc[-1]

        st.subheader("🤖 AI 투자 의견")

        if current > ma20:
            st.success(
                "현재 주가가 20일 이동평균선 위에 있습니다. 단기 상승 추세입니다."
            )
        else:
            st.warning(
                "현재 주가가 20일 이동평균선 아래에 있습니다. 단기 약세 추세입니다."
            )

        st.subheader("🏢 회사 소개")

        st.write(
            info.get(
                "longBusinessSummary",
                "회사 정보 없음"
            )
        )

    except Exception as e:
        st.error(f"오류 발생: {e}")
