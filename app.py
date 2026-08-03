from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).parent
DATA = ROOT / "data"

st.set_page_config(
    page_title="미국 글로벌 헤게모니 TOP30",
    page_icon="H30",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root { --cyan:#22d3ee; --purple:#a78bfa; --line:#24354d; }
    .stApp { background: radial-gradient(circle at 82% -10%, #12365d 0, transparent 28%), #07101c; }
    [data-testid="stHeader"] { background: rgba(7,16,28,.86); }
    .block-container { max-width: 1420px; padding-top: 2.2rem; padding-bottom: 3rem; }
    h1, h2, h3, p, label, [data-testid="stMetricLabel"] { color: #ecf3fb; }
    .hero-kicker { color:var(--cyan); letter-spacing:.18em; font-size:.72rem; font-weight:700; }
    .hero-title { font-size:3.1rem; line-height:1.08; letter-spacing:-.05em; font-weight:700; margin:.7rem 0 1rem; }
    .hero-title span { color:var(--cyan); }
    .hero-copy { color:#9aabc1; max-width:800px; line-height:1.75; }
    .period-grid { display:grid; grid-template-columns:1fr 48px 1fr; align-items:stretch; margin:1.7rem 0 1.1rem; }
    .period-card { border:1px solid var(--line); background:linear-gradient(145deg,#0e1c2d,#0a1625); padding:1.15rem 1.3rem; }
    .period-card.purple { border-top:2px solid var(--purple); }
    .period-card.cyan { border-top:2px solid var(--cyan); }
    .period-card b { display:block; color:#eef5fc; font-size:1.05rem; margin:.3rem 0; }
    .period-card small { color:#7f91a8; }
    .period-card em { font-style:normal; font-size:.68rem; letter-spacing:.12em; color:#71859f; }
    .not-equal { display:grid; place-items:center; color:#58708c; font-size:1.3rem; }
    .data-note { border-left:3px solid var(--purple); background:rgba(167,139,250,.06); padding:.85rem 1rem; color:#a99cbe; font-size:.8rem; line-height:1.6; }
    .live-note { border-left:3px solid var(--cyan); background:rgba(34,211,238,.05); padding:.85rem 1rem; color:#91aabd; font-size:.8rem; line-height:1.6; }
    .audit-note { border:1px solid #6b5228; background:rgba(245,158,11,.055); padding:1rem 1.1rem; color:#d1aa68; font-size:.82rem; line-height:1.65; }
    [data-testid="stMetric"] { background:linear-gradient(145deg,#0e1c2d,#0a1625); border:1px solid var(--line); padding:1rem 1.1rem; }
    [data-testid="stMetricValue"] { color:#edf5fc; }
    [data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--line); }
    .footer { margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1rem; color:#5d718a; font-size:.7rem; letter-spacing:.08em; }
    @media(max-width:700px) {
      .hero-title { font-size:2.1rem; }
      .period-grid { grid-template-columns:1fr; gap:.6rem; }
      .not-equal { display:none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_current() -> pd.DataFrame:
    df = pd.read_csv(DATA / "current_index.csv", parse_dates=["일자"])
    return df.sort_values("일자")


@st.cache_data
def load_constituents() -> pd.DataFrame:
    return pd.read_csv(DATA / "constituents.csv")


def max_drawdown(series: pd.Series) -> float:
    return float((series / series.cummax() - 1).min() * 100)


current = load_current()
constituents = load_constituents()
latest = current.iloc[-1]
current_return = (latest["지수"] / current.iloc[0]["지수"] - 1) * 100
spy_return = (latest["SPY지수"] / current.iloc[0]["SPY지수"] - 1) * 100

st.markdown('<div class="hero-kicker">AMERICAN GLOBAL HEGEMONY TOP30 INDEX</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">정책 수혜의 흐름을<br><span>지수로 추적합니다.</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-copy">S&amp;P500 기업의 정책축·10-K 정책 문맥·미국 매출 순도를 결합한 동일가중 30종목 지수입니다. 과거 백테스트와 현재 공식 지수를 명확히 분리해 표시합니다.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="period-grid">
      <div class="period-card purple"><em>HISTORICAL · APPROX.</em><b>7년 백테스트</b><small>2019.07 — 2026.06 · 7개 빈티지</small></div>
      <div class="not-equal">≠</div>
      <div class="period-card cyan"><em>CURRENT · OFFICIAL</em><b>현재 공식 지수</b><small>2026.07.01 — 현재 · 기준값 1,000</small></div>
    </div>
    """,
    unsafe_allow_html=True,
)

overview, backtest, live, holdings, methodology = st.tabs(
    ["Overview", "7년 백테스트", "현재 지수", "구성종목", "방법론·감사"]
)

with overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("현재 지수", f"{latest['지수']:,.2f}", f"{current_return:+.2f}%")
    c2.metric("SPY 대비", f"{current_return - spy_return:+.2f}%p")
    c3.metric("7년 백테스트", "+123.6%", "SPY +144.4%")
    c4.metric("최종 구성", "30종목", "동일가중 3.33%")

    st.subheader("2026년 7월 1일 이후 공식 지수")
    chart = current.set_index("일자")[["지수", "SPY지수"]]
    st.line_chart(chart, color=["#22d3ee", "#94a3b8"], height=390)
    st.markdown(
        f'<div class="live-note">최신 데이터: {latest["일자"].strftime("%Y-%m-%d")} 종가 · 동일가중 가격지수 · 배당 미반영 · 백테스트 구간과 연결하지 않음</div>',
        unsafe_allow_html=True,
    )

    st.subheader("2026 정책축 구성")
    sector_counts = constituents.groupby("정책축", sort=False).size().rename("종목수")
    st.bar_chart(sector_counts, horizontal=True, color="#22d3ee", height=330)

with backtest:
    st.subheader("2019.07 — 2026.07 백테스트 성과")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("누적수익", "+123.6%", "SPY +144.4%")
    c2.metric("CAGR", "12.0%", "SPY 13.4%")
    c3.metric("최대낙폭", "−32%", "SPY −32%")
    c4.metric("샤프", "0.43", "SPY 0.51")

    returns = pd.DataFrame(
        {"누적수익(%)": [123.6, 144.4]}, index=["H30", "SPY"]
    )
    st.bar_chart(returns, horizontal=True, color="#a78bfa", height=260)
    st.markdown(
        '<div class="data-note">7년 성과는 누적수익 역산·반올림 근사치입니다. 일별 에쿼티커브가 확정되기 전까지 선 그래프로 표시하지 않습니다. 정체성은 초과수익보다는 ‘정책 베타 + 약세장 방어’에 가깝습니다.</div>',
        unsafe_allow_html=True,
    )

    st.subheader("연도별 정책축 구성 변화")
    sector_history = pd.read_csv(DATA / "sector_history.csv").set_index("연도")
    st.bar_chart(sector_history, stack=True, height=430)
    st.caption("매년 30종목 · 정책축당 최대 6종목 · 2019~2025 빈티지")

with live:
    st.subheader("현재 공식 지수")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("최신 종가", f"{latest['지수']:,.2f}", latest["일자"].strftime("%Y-%m-%d"))
    c2.metric("출시 후 수익률", f"{current_return:+.2f}%")
    c3.metric("SPY 대비", f"{current_return - spy_return:+.2f}%p")
    c4.metric("최대낙폭", f"{max_drawdown(current['지수']):.2f}%")
    st.line_chart(current.set_index("일자")[["지수", "SPY지수"]], color=["#22d3ee", "#94a3b8"], height=470)
    st.dataframe(
        current.sort_values("일자", ascending=False),
        hide_index=True,
        width="stretch",
        column_config={
            "일자": st.column_config.DateColumn("일자", format="YYYY-MM-DD"),
            "지수": st.column_config.NumberColumn("H30", format="%.4f"),
            "SPY지수": st.column_config.NumberColumn("SPY", format="%.4f"),
        },
    )

with holdings:
    st.subheader("최종 30종목과 정책 수혜")
    search_col, axis_col = st.columns([2, 1])
    query = search_col.text_input("종목 검색", placeholder="티커·기업명·수혜 내용")
    axes = axis_col.multiselect("정책축", constituents["정책축"].drop_duplicates().tolist())

    filtered = constituents.copy()
    if query:
        mask = filtered.astype(str).apply(
            lambda row: row.str.contains(query, case=False, na=False).any(), axis=1
        )
        filtered = filtered[mask]
    if axes:
        filtered = filtered[filtered["정책축"].isin(axes)]

    shown = filtered.copy()
    shown["주요 정책 수혜"] = "• " + shown["수혜1"] + "\n• " + shown["수혜2"]
    shown["감사"] = shown["감사"].fillna("—")
    st.dataframe(
        shown[["순위", "티커", "기업명", "정책축", "총점", "주요 정책 수혜", "감사"]],
        hide_index=True,
        width="stretch",
        height=690,
        column_config={
            "순위": st.column_config.NumberColumn("순위", width="small"),
            "티커": st.column_config.TextColumn("티커", width="small"),
            "기업명": st.column_config.TextColumn("기업명", width="medium"),
            "정책축": st.column_config.TextColumn("정책축", width="small"),
            "총점": st.column_config.NumberColumn("총점", width="small"),
            "주요 정책 수혜": st.column_config.TextColumn("주요 정책 수혜", width="large"),
            "감사": st.column_config.TextColumn("감사", width="medium"),
        },
    )
    st.caption("감사 표시는 편출을 의미하지 않으며, 정책 문맥 또는 축 정합성을 추가 공시해야 하는 종목입니다.")

with methodology:
    st.subheader("방법론")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**01 · 유니버스**")
        st.write("매년 6월 30일 현재 S&P500 구성종목을 당시 시점 기준으로 복원합니다.")
    with c2:
        st.markdown("**02 · 채점**")
        st.write("영역가중 + 정책정렬 + 미국 매출 순도 − 중국감점으로 계산합니다.")
    with c3:
        st.markdown("**03 · 구성**")
        st.write("30종목 동일가중, 정책축당 최대 6종목, 다음 달 첫 영업일부터 적용합니다.")
    with c4:
        st.markdown("**04 · 구간 분리**")
        st.write("2026년 6월까지는 백테스트, 7월 1일부터는 공식 지수로 분리합니다.")

    st.markdown(
        '<div class="audit-note"><b>위원회 조정</b><br>EQT→EOG · INCY→ABBV · SHW→DD<br><br><b>감사 플래그</b><br>BRK.B: 금융 축과 에너지 자회사 수혜 근거 불일치 · EOG: 해외 onshore 문맥 포함 · MRK/ABBV: IRA 약가협상 문맥 · DD: IRA 자사주 소비세 오계상 검토</div>',
        unsafe_allow_html=True,
    )
    st.download_button(
        "방법론 요약 다운로드",
        data=(ROOT / "methodology.txt").read_text(encoding="utf-8"),
        file_name="H30_방법론_요약.txt",
        mime="text/plain",
    )

st.markdown(
    '<div class="footer">INDEX TEAM 1 · AMERICAN GLOBAL HEGEMONY TOP30 · Research prototype · Not investment advice</div>',
    unsafe_allow_html=True,
)
