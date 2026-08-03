from pathlib import Path

import altair as alt
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
    :root { --cyan:#32c9e8; --purple:#9b8afb; --line:#21334a; --surface:#0b1727; --surface-2:#0e1d30; --muted:#8fa1b8; }
    .stApp { background: radial-gradient(circle at 88% -5%, rgba(32,91,143,.34) 0, transparent 26%), radial-gradient(circle at 4% 18%, rgba(93,71,150,.14) 0, transparent 24%), #060e19; }
    [data-testid="stHeader"] { background: rgba(6,14,25,.82); backdrop-filter: blur(14px); }
    .block-container { max-width: 1320px; padding-top: 1.35rem; padding-bottom: 3rem; }
    h1, h2, h3, p, label, [data-testid="stMetricLabel"] { color: #ecf3fb; }
    .hero-panel { display:grid; grid-template-columns:minmax(0,1.55fr) minmax(260px,.65fr); gap:1.5rem; align-items:end; border:1px solid var(--line); border-radius:18px; background:linear-gradient(135deg,rgba(14,29,48,.94),rgba(8,19,33,.96)); padding:1.65rem 1.8rem; box-shadow:0 22px 60px rgba(0,0,0,.18); }
    .hero-kicker { color:var(--cyan); letter-spacing:.17em; font-size:.68rem; font-weight:700; }
    .hero-title { font-size:2.55rem; line-height:1.08; letter-spacing:-.045em; font-weight:720; margin:.55rem 0 .7rem; }
    .hero-title span { color:var(--cyan); }
    .hero-copy { color:#9eb0c5; max-width:760px; line-height:1.65; font-size:.92rem; }
    .hero-live { border-left:1px solid var(--line); padding-left:1.5rem; }
    .live-status { display:flex; align-items:center; gap:.45rem; color:#92a6bc; letter-spacing:.08em; font-size:.67rem; text-transform:uppercase; }
    .live-dot { width:7px; height:7px; border-radius:50%; background:var(--cyan); box-shadow:0 0 12px rgba(50,201,232,.9); }
    .hero-index { color:#f4f8fc; font-size:2.4rem; letter-spacing:-.04em; font-weight:700; margin:.35rem 0 .05rem; }
    .hero-change { color:var(--cyan); font-size:.9rem; font-weight:650; }
    .hero-date { color:#6f849c; font-size:.72rem; margin-top:.35rem; }
    .period-grid { display:grid; grid-template-columns:1fr 1fr; gap:.8rem; margin:1rem 0 1.1rem; }
    .period-card { border:1px solid var(--line); border-radius:12px; background:rgba(10,23,39,.76); padding:.9rem 1.05rem; }
    .period-card.purple { border-left:3px solid var(--purple); }
    .period-card.cyan { border-left:3px solid var(--cyan); }
    .period-card b { display:block; color:#eef5fc; font-size:.95rem; margin:.2rem 0; }
    .period-card small { color:#788ca5; }
    .period-card em { font-style:normal; font-size:.62rem; letter-spacing:.13em; color:#7388a1; }
    .section-label { color:var(--cyan); letter-spacing:.13em; font-size:.65rem; font-weight:700; margin-bottom:.2rem; text-transform:uppercase; }
    .section-title { color:#f0f6fc; font-size:1.24rem; font-weight:700; letter-spacing:-.02em; margin-bottom:.2rem; }
    .section-copy { color:#7f93aa; font-size:.8rem; margin-bottom:.85rem; }
    .data-note { border:1px solid rgba(155,138,251,.28); border-radius:10px; background:rgba(155,138,251,.055); padding:.8rem .95rem; color:#afa4c7; font-size:.78rem; line-height:1.6; }
    .live-note { border:1px solid rgba(50,201,232,.25); border-radius:10px; background:rgba(50,201,232,.045); padding:.8rem .95rem; color:#91aabd; font-size:.78rem; line-height:1.6; }
    .audit-note { border:1px solid #6b5228; background:rgba(245,158,11,.055); padding:1rem 1.1rem; color:#d1aa68; font-size:.82rem; line-height:1.65; }
    [data-testid="stMetric"] { background:linear-gradient(145deg,var(--surface-2),var(--surface)); border:1px solid var(--line); border-radius:12px; padding:.9rem 1rem; min-height:112px; }
    [data-testid="stMetricLabel"] { color:#8ea2b9; font-size:.78rem; }
    [data-testid="stMetricValue"] { color:#edf5fc; letter-spacing:-.035em; }
    [data-testid="stMetricDelta"] { font-size:.76rem; }
    [data-testid="stVegaLiteChart"] { background:rgba(10,23,39,.68); border:1px solid var(--line); border-radius:14px; padding:.6rem .55rem .15rem; }
    [data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
    [data-baseweb="tab-list"] { gap:.25rem; background:rgba(10,23,39,.72); border:1px solid var(--line); border-radius:12px; padding:.3rem; }
    [data-baseweb="tab"] { border-radius:8px; padding:.55rem .95rem; }
    [data-baseweb="tab"][aria-selected="true"] { background:#14263c; }
    [data-baseweb="tab-highlight"] { display:none; }
    hr { border-color:var(--line); }
    .footer { margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1rem; color:#5d718a; font-size:.7rem; letter-spacing:.08em; }
    @media(max-width:800px) {
      .hero-panel { grid-template-columns:1fr; padding:1.25rem; }
      .hero-live { border-left:0; border-top:1px solid var(--line); padding:1rem 0 0; }
      .hero-title { font-size:2rem; }
      .period-grid { grid-template-columns:1fr; gap:.6rem; }
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


def performance_frame(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    prepared["H30 누적수익률"] = (prepared["지수"] / prepared["지수"].iloc[0] - 1) * 100
    prepared["SPY 누적수익률"] = (prepared["SPY지수"] / prepared["SPY지수"].iloc[0] - 1) * 100
    prepared["H30 일간등락"] = prepared["지수"].pct_change() * 100
    prepared["등락"] = prepared["H30 일간등락"].map(
        lambda value: "상승" if pd.notna(value) and value >= 0 else "하락"
    )
    return prepared


def cumulative_return_chart(df: pd.DataFrame, height: int = 390) -> alt.Chart:
    long = df.melt(
        id_vars="일자",
        value_vars=["H30 누적수익률", "SPY 누적수익률"],
        var_name="시리즈",
        value_name="누적수익률",
    )
    long["시리즈"] = long["시리즈"].str.replace(" 누적수익률", "", regex=False)
    y_min = float(long["누적수익률"].min())
    y_max = float(long["누적수익률"].max())
    padding = max((y_max - y_min) * 0.13, 0.25)
    domain = [y_min - padding, y_max + padding]

    zero_line = alt.Chart(pd.DataFrame({"기준": [0]})).mark_rule(
        color="#53657a", strokeDash=[4, 4], strokeWidth=1
    ).encode(y="기준:Q")
    lines = (
        alt.Chart(long)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=34), strokeWidth=2.6)
        .encode(
            x=alt.X("일자:T", title=None, axis=alt.Axis(format="%m/%d", grid=False, labelColor="#8194aa")),
            y=alt.Y(
                "누적수익률:Q",
                title="기준일 대비 (%)",
                scale=alt.Scale(domain=domain, zero=False, nice=False),
                axis=alt.Axis(format="+.1f", grid=True, gridColor="#1c2d43", labelColor="#8194aa", titleColor="#8194aa"),
            ),
            color=alt.Color(
                "시리즈:N",
                title=None,
                scale=alt.Scale(domain=["H30", "SPY"], range=["#32c9e8", "#8b9bb0"]),
                legend=alt.Legend(orient="top", direction="horizontal", labelColor="#a7b6c8"),
            ),
            tooltip=[
                alt.Tooltip("일자:T", title="일자", format="%Y-%m-%d"),
                alt.Tooltip("시리즈:N", title="지수"),
                alt.Tooltip("누적수익률:Q", title="누적수익률", format="+.2f"),
            ],
        )
    )
    return (zero_line + lines).properties(height=height).configure_view(strokeOpacity=0)


def daily_return_chart(df: pd.DataFrame, height: int = 170) -> alt.Chart:
    daily = df.dropna(subset=["H30 일간등락"])
    bars = (
        alt.Chart(daily)
        .mark_bar(size=12, cornerRadius=2)
        .encode(
            x=alt.X("일자:T", title=None, axis=alt.Axis(format="%m/%d", grid=False, labelColor="#8194aa")),
            y=alt.Y(
                "H30 일간등락:Q",
                title="일간 등락 (%)",
                scale=alt.Scale(zero=True),
                axis=alt.Axis(format="+.1f", grid=True, gridColor="#1c2d43", labelColor="#8194aa", titleColor="#8194aa"),
            ),
            color=alt.Color(
                "등락:N",
                title=None,
                scale=alt.Scale(domain=["상승", "하락"], range=["#32c9e8", "#f07178"]),
                legend=alt.Legend(orient="top", direction="horizontal", labelColor="#a7b6c8"),
            ),
            tooltip=[
                alt.Tooltip("일자:T", title="일자", format="%Y-%m-%d"),
                alt.Tooltip("H30 일간등락:Q", title="일간 등락률", format="+.2f"),
            ],
        )
    )
    return bars.properties(height=height).configure_view(strokeOpacity=0)


def section_header(label: str, title: str, copy: str) -> None:
    st.markdown(
        f'<div class="section-label">{label}</div><div class="section-title">{title}</div><div class="section-copy">{copy}</div>',
        unsafe_allow_html=True,
    )


current = load_current()
constituents = load_constituents()
performance = performance_frame(current)
latest = current.iloc[-1]
current_return = (latest["지수"] / current.iloc[0]["지수"] - 1) * 100
spy_return = (latest["SPY지수"] / current.iloc[0]["SPY지수"] - 1) * 100
daily_moves = performance["H30 일간등락"].dropna()
best_day = float(daily_moves.max())
worst_day = float(daily_moves.min())
positive_ratio = float((daily_moves > 0).mean() * 100)

st.markdown(
    f"""
    <div class="hero-panel">
      <div>
        <div class="hero-kicker">AMERICAN GLOBAL HEGEMONY TOP30 INDEX</div>
        <div class="hero-title">정책 수혜의 흐름을<br><span>지수로 추적합니다.</span></div>
        <div class="hero-copy">S&amp;P500 기업의 정책축·10-K 정책 문맥·미국 매출 순도를 결합한 동일가중 30종목 지수입니다. 백테스트와 공식 산출 구간을 분리해 추적합니다.</div>
      </div>
      <div class="hero-live">
        <div class="live-status"><span class="live-dot"></span>Official index</div>
        <div class="hero-index">{latest['지수']:,.2f}</div>
        <div class="hero-change">{current_return:+.2f}% · SPY 대비 {current_return - spy_return:+.2f}%p</div>
        <div class="hero-date">{latest['일자'].strftime('%Y-%m-%d')} 종가 · 기준값 1,000</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="period-grid">
      <div class="period-card purple"><em>HISTORICAL · APPROX.</em><b>7년 백테스트</b><small>2019.07 — 2026.06 · 7개 빈티지</small></div>
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

    section_header("Official track", "공식 지수 누적수익률", "기준일을 0%로 두고 실제 등락 범위만 확대해 표시합니다.")
    st.altair_chart(cumulative_return_chart(performance, 370), width="stretch")
    st.markdown(
        f'<div class="live-note">최신 데이터: {latest["일자"].strftime("%Y-%m-%d")} 종가 · 동일가중 가격지수 · 배당 미반영 · 백테스트 구간과 연결하지 않음</div>',
        unsafe_allow_html=True,
    )

    section_header("Composition", "2026 정책축 구성", "최종 30종목의 정책축별 편입 수입니다.")
    sector_counts = constituents.groupby("정책축", sort=False).size().rename("종목수")
    sector_df = sector_counts.reset_index()
    sector_chart = (
        alt.Chart(sector_df)
        .mark_bar(color="#32c9e8", cornerRadiusEnd=4, height=18)
        .encode(
            x=alt.X("종목수:Q", title=None, axis=alt.Axis(tickMinStep=1, gridColor="#1c2d43", labelColor="#8194aa")),
            y=alt.Y("정책축:N", title=None, sort=None, axis=alt.Axis(labelColor="#a7b6c8", labelLimit=240)),
            tooltip=["정책축:N", "종목수:Q"],
        )
        .properties(height=300)
        .configure_view(strokeOpacity=0)
    )
    st.altair_chart(sector_chart, width="stretch")

with backtest:
    section_header("Historical · Approx.", "2019.07 — 2026.06 백테스트 성과", "확정된 7개 빈티지를 기준으로 한 근사 성과 요약입니다.")
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
    section_header("Current · Official", "2026년 7월 공식 지수", "누적 방향과 일간 진폭을 분리해 표시합니다.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("최신 종가", f"{latest['지수']:,.2f}", latest["일자"].strftime("%Y-%m-%d"))
    c2.metric("출시 후 수익률", f"{current_return:+.2f}%")
    c3.metric("SPY 대비", f"{current_return - spy_return:+.2f}%p")
    c4.metric("최대낙폭", f"{max_drawdown(current['지수']):.2f}%")

    section_header("Cumulative", "기준일 대비 누적수익률", "Y축을 실제 관측 범위로 확대해 H30과 SPY의 상대 흐름을 비교합니다.")
    st.altair_chart(cumulative_return_chart(performance, 430), width="stretch")

    section_header("Daily range", "H30 일간 등락률", "상승일과 하락일의 진폭을 별도 막대로 확인합니다.")
    st.altair_chart(daily_return_chart(performance), width="stretch")

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("기간 고점", f"{current['지수'].max():,.2f}")
    p2.metric("기간 저점", f"{current['지수'].min():,.2f}")
    p3.metric("최대 일간 등락", f"{best_day:+.2f}%", f"최저 {worst_day:+.2f}%")
    p4.metric("상승일 비중", f"{positive_ratio:.1f}%", f"{int((daily_moves > 0).sum())}/{len(daily_moves)}일")

    st.markdown('<div class="live-note">누적수익률 차트는 0% 기준선을 중심으로 관측 구간을 확대합니다. 원지수는 아래 표에서 소수점 네 자리까지 확인할 수 있습니다.</div>', unsafe_allow_html=True)
    st.dataframe(
        performance[["일자", "지수", "SPY지수", "H30 누적수익률", "H30 일간등락"]].sort_values("일자", ascending=False),
        hide_index=True,
        width="stretch",
        column_config={
            "일자": st.column_config.DateColumn("일자", format="YYYY-MM-DD"),
            "지수": st.column_config.NumberColumn("H30", format="%.4f"),
            "SPY지수": st.column_config.NumberColumn("SPY", format="%.4f"),
            "H30 누적수익률": st.column_config.NumberColumn("누적수익률", format="%+.2f%%"),
            "H30 일간등락": st.column_config.NumberColumn("일간등락", format="%+.2f%%"),
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
