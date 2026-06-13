import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Stock On Korea",
    page_icon="📈",
    layout="wide"
)

menu = st.sidebar.selectbox(
    "메뉴 선택",
    [
        "📈 주식/증권",
        "⚽ 스포츠"
    ]
)

if menu == "📈 주식/증권":

    st.title("📈 AI 주식 분석기")

    st.info(
        """
        🇰🇷 대한민국 주식 안내

        대한민국의 주식을 분석하시려면
        티커번호 뒤에 .KS를 붙여서 입력해주시기 바랍니다.

        예시:
        • 삼성전자 → 005930.KS
        • SK하이닉스 → 000660.KS
        • NAVER → 035420.KS
        • 카카오 → 035720.KS
        """
    )

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

            st.subheader("📰 최신 관련 뉴스")

            try:
                news_list = stock.news

                if news_list:
                    for news in news_list[:10]:
                        title = news.get("title", "제목 없음")
                        publisher = news.get("publisher", "출처 없음")
                        link = news.get("link", "#")

                        st.markdown(f"### {title}")
                        st.write(f"📰 {publisher}")
                        st.markdown(f"[기사 보기]({link})")
                        st.divider()
                else:
                    st.info("뉴스를 찾을 수 없습니다.")

            except Exception as e:
                st.error(f"뉴스 오류: {e}")

        except Exception as e:
            st.error(f"오류 발생: {e}")



st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:14px;">
    <b>Stock On Korea</b><br>
    개발자 : 이시형, 송민준, 이동기, 문주원, 지혜성<br><br>

    © 2026 Stock On Korea. All Rights Reserved.<br>

    본 웹사이트의 디자인, 코드, 분석 결과 화면 및 콘텐츠는
    저작권법의 보호를 받습니다.<br>

    개발자의 사전 허가 없이 무단 복제, 배포, 수정 및 상업적 이용을 금지합니다.<br>

    본 서비스에서 제공하는 정보는 투자 참고용이며,
    투자에 대한 최종 책임은 이용자 본인에게 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)

if menu == "⚽ 스포츠":

    import requests

    st.title("⚽ Stock On Korea 스포츠 센터")

    sport = st.selectbox(
        "종목 선택",
        ["축구", "야구", "농구"]
    )

    if sport == "축구":

        st.header("⚽ EPL 최근 경기 결과")

        url = "https://www.thesportsdb.com/api/v1/json/123/eventspastleague.php?id=4328"

        try:
            response = requests.get(url)
            data = response.json()

            events = data.get("events")

            if events:
                for match in events[:10]:
                    home = match.get("strHomeTeam", "Unknown")
                    away = match.get("strAwayTeam", "Unknown")

                    home_score = match.get("intHomeScore", "-")
                    away_score = match.get("intAwayScore", "-")

                    st.write(
                        f"⚽ {home} {home_score} : {away_score} {away}"
                    )
            else:
                st.warning("경기 데이터를 불러오지 못했습니다.")

        except Exception as e:
            st.error(f"오류: {e}")

    elif sport == "야구":

        st.header("⚾ MLB 최근 경기")

        url = "https://www.thesportsdb.com/api/v1/json/123/eventspastleague.php?id=4424"

        try:
            response = requests.get(url)
            data = response.json()

            events = data.get("events")

            if events:
                for match in events[:10]:
                    home = match.get("strHomeTeam", "Unknown")
                    away = match.get("strAwayTeam", "Unknown")

                    home_score = match.get("intHomeScore", "-")
                    away_score = match.get("intAwayScore", "-")

                    st.write(
                        f"⚾ {home} {home_score} : {away_score} {away}"
                    )
            else:
                st.warning("경기 데이터를 찾을 수 없습니다.")

        except Exception as e:
            st.error(f"오류: {e}")

    elif sport == "농구":

        st.header("🏀 NBA")

        st.info("NBA API 연동 예정")


st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:14px;">
    <b>Stock On Korea</b><br>
    개발자 : 이시형, 송민준, 이동기, 문주원, 지혜성<br><br>

    © 2026 Stock On Korea. All Rights Reserved.<br>

    본 웹사이트의 디자인, 코드, 분석 결과 화면 및 콘텐츠는
    저작권법의 보호를 받습니다.<br>

    개발자의 사전 허가 없이 무단 복제, 배포, 수정 및 상업적 이용을 금지합니다.<br>

    본 서비스에서 제공하는 정보는 투자 참고용이며,
    투자에 대한 최종 책임은 이용자 본인에게 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)
