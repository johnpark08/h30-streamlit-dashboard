from html import escape
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import altair as alt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).parent
DATA = ROOT / "data"

st.set_page_config(
    page_title="미국 글로벌 헤게모니 TOP30",
    page_icon="T30",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root { --cyan:#0797ad; --purple:#7568d7; --line:#dbe4ee; --surface:#ffffff; --surface-2:#f8fafc; --muted:#66788e; --ink:#132238; }
    .stApp { background:radial-gradient(circle at 86% -8%, rgba(53,183,202,.16) 0, transparent 25%), radial-gradient(circle at 3% 14%, rgba(117,104,215,.08) 0, transparent 22%), #f4f7fb; color:var(--ink); font-family:Inter,Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    [data-testid="stHeader"] { background:rgba(244,247,251,.84); backdrop-filter:blur(16px); border-bottom:1px solid rgba(219,228,238,.7); }
    .block-container, [data-testid="stMainBlockContainer"] { max-width:1180px !important; width:calc(100% - 2rem) !important; margin-inline:auto !important; padding-top:1.35rem; padding-bottom:3rem; box-sizing:border-box; }
    h1, h2, h3, p, label, [data-testid="stMetricLabel"] { color:var(--ink); }
    .hero-panel { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(220px,.55fr); gap:1.5rem; align-items:end; border:1px solid #d8e5ed; border-radius:20px; background:linear-gradient(120deg,#ffffff 0%,#ffffff 58%,#edf9fb 100%); padding:1.75rem 1.9rem; box-shadow:0 18px 48px rgba(48,74,103,.09); }
    .hero-kicker { color:var(--cyan); letter-spacing:.17em; font-size:.68rem; font-weight:700; }
    .hero-title { font-size:2.55rem; line-height:1.08; letter-spacing:-.045em; font-weight:720; margin:.55rem 0 .7rem; }
    .hero-title span { color:#078aa0; }
    .hero-copy { color:#60748a; max-width:660px; line-height:1.65; font-size:.92rem; }
    .hero-live { border-left:1px solid var(--line); padding-left:1.5rem; }
    .live-status { display:flex; align-items:center; gap:.45rem; color:#6c8096; letter-spacing:.08em; font-size:.67rem; text-transform:uppercase; }
    .live-dot { width:7px; height:7px; border-radius:50%; background:#0aa1b7; box-shadow:0 0 0 4px rgba(10,161,183,.12); }
    .hero-index { color:#15263c; font-size:2.4rem; letter-spacing:-.04em; font-weight:700; margin:.35rem 0 .05rem; }
    .hero-change { color:#078aa0; font-size:.9rem; font-weight:650; }
    .hero-date { color:#7a8da1; font-size:.72rem; margin-top:.35rem; }
    .profile-toolbar { display:flex; justify-content:flex-end; align-items:center; min-height:42px; color:#6f8195; font-size:.74rem; }
    .profile-toolbar b { color:#1b3047; font-weight:700; }
    [data-testid="stDownloadButton"] > button { min-height:42px; border:1px solid #cddde8; border-radius:9px; background:#ffffff; color:#087e91; font-weight:650; box-shadow:0 5px 14px rgba(48,74,103,.04); }
    [data-testid="stDownloadButton"] > button:hover { border-color:#0797ad; color:#087e91; }
    .index-spec-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); overflow:hidden; margin:.1rem 0 1.15rem; border:1px solid #d7e2eb; border-top:3px solid #0797ad; border-radius:12px; background:#ffffff; box-shadow:0 8px 24px rgba(48,74,103,.045); }
    .index-spec { min-height:92px; padding:.9rem 1rem; border-right:1px solid #e2e9f0; border-bottom:1px solid #e2e9f0; }
    .index-spec:nth-child(3n) { border-right:0; }
    .index-spec:nth-last-child(-n+3) { border-bottom:0; }
    .spec-label { display:block; margin-bottom:.42rem; color:#6f8298; font-size:.67rem; font-weight:650; letter-spacing:.04em; }
    .spec-value { display:flex; flex-wrap:wrap; align-items:center; gap:.38rem; color:#1b2d43; font-size:.9rem; font-weight:700; }
    .spec-chip { display:inline-flex; align-items:center; border:1px solid #d6e3eb; border-radius:7px; background:#f6fafc; padding:.28rem .48rem; color:#31536b; font-size:.72rem; font-weight:650; }
    .spec-note { color:#789; font-size:.69rem; font-weight:500; }
    .period-grid { display:grid; grid-template-columns:1fr 1fr; gap:.8rem; margin:1rem 0 1.1rem; }
    .period-card { border:1px solid var(--line); border-radius:13px; background:rgba(255,255,255,.82); padding:.9rem 1.05rem; box-shadow:0 6px 18px rgba(48,74,103,.045); }
    .period-card.purple { border-left:3px solid var(--purple); }
    .period-card.cyan { border-left:3px solid var(--cyan); }
    .period-card b { display:block; color:#1b2d43; font-size:.95rem; margin:.2rem 0; }
    .period-card small { color:#71849a; }
    .period-card em { font-style:normal; font-size:.62rem; letter-spacing:.13em; color:#73859a; }
    .section-label { color:var(--cyan); letter-spacing:.13em; font-size:.65rem; font-weight:700; margin-bottom:.2rem; text-transform:uppercase; }
    .section-title { color:#17283e; font-size:1.24rem; font-weight:700; letter-spacing:-.02em; margin-bottom:.2rem; }
    .section-copy { color:#718399; font-size:.8rem; margin-bottom:.85rem; }
    .data-note { border:1px solid rgba(117,104,215,.2); border-radius:11px; background:#f6f4ff; padding:.8rem .95rem; color:#625b89; font-size:.78rem; line-height:1.6; }
    .live-note { border:1px solid rgba(7,151,173,.2); border-radius:11px; background:#edf9fb; padding:.8rem .95rem; color:#52717a; font-size:.78rem; line-height:1.6; }
    .audit-note { border:1px solid #efd79a; border-radius:11px; background:#fff9e9; padding:1rem 1.1rem; color:#795e28; font-size:.82rem; line-height:1.65; }
    .holdings-summary { display:flex; flex-wrap:wrap; align-items:center; gap:.55rem; margin:.15rem 0 1rem; color:#6a7e94; font-size:.75rem; }
    .holdings-summary b { color:#173047; font-size:.86rem; }
    .summary-dot { width:3px; height:3px; border-radius:50%; background:#9aabbb; }
    .holding-card { --accent:#0797ad; position:relative; min-height:195px; margin-bottom:.8rem; overflow:hidden; border:1px solid var(--line); border-top:3px solid var(--accent); border-radius:15px; background:linear-gradient(145deg,#ffffff 0%,#fbfdff 100%); padding:1rem 1.1rem 1.05rem; box-shadow:0 9px 24px rgba(48,74,103,.055); }
    .holding-card.axis-ai { --accent:#7568d7; }
    .holding-card.axis-defense { --accent:#4d79bf; }
    .holding-card.axis-energy { --accent:#d88946; }
    .holding-card.axis-materials { --accent:#a97355; }
    .holding-card.axis-bio { --accent:#42a079; }
    .holding-card.axis-finance { --accent:#61758d; }
    .holding-head { display:flex; align-items:center; justify-content:space-between; gap:.75rem; }
    .holding-rank { color:#91a0b0; font-size:.68rem; font-weight:700; letter-spacing:.11em; }
    .axis-chip { border:1px solid color-mix(in srgb, var(--accent) 28%, white); border-radius:999px; background:color-mix(in srgb, var(--accent) 9%, white); padding:.25rem .55rem; color:var(--accent); font-size:.64rem; font-weight:700; }
    .holding-identity { display:flex; align-items:flex-end; justify-content:space-between; gap:.8rem; margin:.7rem 0 .25rem; }
    .holding-ticker { color:#14273d; font-size:1.48rem; font-weight:760; letter-spacing:-.035em; line-height:1; }
    .holding-score { color:#60748a; font-size:.67rem; white-space:nowrap; }
    .holding-company { color:#667b91; font-size:.77rem; min-height:1.2rem; }
    .benefit-list { display:grid; gap:.42rem; margin:.8rem 0 0; padding-top:.75rem; border-top:1px solid #e7edf3; }
    .benefit-item { display:flex; align-items:flex-start; gap:.48rem; color:#3f5369; font-size:.76rem; line-height:1.45; }
    .benefit-bullet { flex:0 0 auto; width:5px; height:5px; margin-top:.42rem; border-radius:50%; background:var(--accent); }
    [data-testid="stMetric"] { background:#ffffff; border:1px solid var(--line); border-radius:13px; padding:.9rem 1rem; min-height:112px; box-shadow:0 8px 22px rgba(48,74,103,.055); }
    [data-testid="stMetricLabel"] { color:#718399; font-size:.78rem; }
    [data-testid="stMetricValue"] { color:#17283e; letter-spacing:-.035em; }
    [data-testid="stMetricDelta"] { font-size:.76rem; }
    [data-testid="stVegaLiteChart"] { box-sizing:border-box; width:100%; overflow:hidden; background:#ffffff; border:1px solid var(--line); border-radius:14px; padding:.8rem 1.15rem .55rem; box-shadow:0 8px 24px rgba(48,74,103,.045); }
    [data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; box-shadow:0 8px 24px rgba(48,74,103,.04); }
    [data-baseweb="tab-list"] { gap:.25rem; background:rgba(255,255,255,.82); border:1px solid var(--line); border-radius:12px; padding:.3rem; box-shadow:0 6px 18px rgba(48,74,103,.04); }
    [data-baseweb="tab"] { border-radius:8px; padding:.55rem .95rem; color:#53677e; }
    [data-baseweb="tab"][aria-selected="true"] { background:#eaf6f8; color:#0b7181; }
    [data-baseweb="tab-highlight"] { display:none; }
    [data-baseweb="input"] > div, [data-baseweb="select"] > div { background:#ffffff; border-color:var(--line); }
    [data-testid="stCaptionContainer"] { color:#73859a; }
    hr { border-color:var(--line); }
    .footer { margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1rem; color:#7a8ca0; font-size:.7rem; letter-spacing:.08em; }
    @media(max-width:800px) {
      .hero-panel { grid-template-columns:1fr; padding:1.25rem; }
      .hero-live { border-left:0; border-top:1px solid var(--line); padding:1rem 0 0; }
      .hero-title { font-size:2rem; }
      .period-grid { grid-template-columns:1fr; gap:.6rem; }
      .index-spec-grid { grid-template-columns:1fr; }
      .index-spec, .index-spec:nth-child(3n), .index-spec:nth-last-child(-n+3) { border-right:0; border-bottom:1px solid #e2e9f0; }
      .index-spec:last-child { border-bottom:0; }
      .holding-card { min-height:auto; }
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


@st.cache_data
def load_backtest() -> pd.DataFrame:
    df = pd.read_csv(DATA / "backtest_weekly.csv", encoding="utf-8-sig")
    df = df.rename(columns={"룰유니버스_3년체인": "T30"})
    df["일자"] = pd.to_datetime(df["일자"])
    return df[df["일자"] <= pd.Timestamp("2026-06-29")].sort_values("일자")


def max_drawdown(series: pd.Series) -> float:
    return float((series / series.cummax() - 1).min() * 100)


def performance_frame(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    prepared["T30 누적수익률"] = (prepared["지수"] / prepared["지수"].iloc[0] - 1) * 100
    prepared["SPY 누적수익률"] = (prepared["SPY지수"] / prepared["SPY지수"].iloc[0] - 1) * 100
    prepared["T30 일간등락"] = prepared["지수"].pct_change() * 100
    prepared["등락"] = prepared["T30 일간등락"].map(
        lambda value: "상승" if pd.notna(value) and value >= 0 else "하락"
    )
    return prepared


def backtest_performance_frame(df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    prepared["T30 누적수익률"] = (prepared["T30"] / prepared["T30"].iloc[0] - 1) * 100
    prepared["SPY 누적수익률"] = (prepared["SPY"] / prepared["SPY"].iloc[0] - 1) * 100
    return prepared


def period_stats(df: pd.DataFrame, column: str) -> dict[str, float]:
    returns = df[column].pct_change().dropna()
    total_return = float(df[column].iloc[-1] / df[column].iloc[0] - 1)
    years = float((df["일자"].iloc[-1] - df["일자"].iloc[0]).days / 365.25)
    cagr = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0.0
    volatility = float(returns.std() * (52**0.5)) if len(returns) > 1 else 0.0
    sharpe = float(returns.mean() / returns.std() * (52**0.5)) if len(returns) > 1 and returns.std() else 0.0
    return {
        "total_return": total_return * 100,
        "cagr": cagr * 100,
        "volatility": volatility * 100,
        "mdd": max_drawdown(df[column]),
        "sharpe": sharpe,
    }


def padded_date_domain(dates: pd.Series) -> list:
    ordered = pd.Series(pd.to_datetime(dates).dropna().unique()).sort_values()
    if len(ordered) < 2:
        padding = pd.Timedelta(days=1)
    else:
        typical_interval = pd.Timedelta(ordered.diff().dropna().median())
        padding = max(typical_interval * 1.25, pd.Timedelta(days=1))
    return [
        (ordered.iloc[0] - padding).to_pydatetime(),
        (ordered.iloc[-1] + padding).to_pydatetime(),
    ]


def cumulative_return_chart(
    df: pd.DataFrame, height: int = 390, date_format: str = "%m/%d"
) -> alt.Chart:
    long = df.melt(
        id_vars="일자",
        value_vars=["T30 누적수익률", "SPY 누적수익률"],
        var_name="시리즈",
        value_name="누적수익률",
    )
    long["시리즈"] = long["시리즈"].str.replace(" 누적수익률", "", regex=False)
    y_min = float(long["누적수익률"].min())
    y_max = float(long["누적수익률"].max())
    padding = max((y_max - y_min) * 0.13, 0.25)
    domain = [y_min - padding, y_max + padding]
    date_domain = padded_date_domain(long["일자"])

    zero_line = alt.Chart(pd.DataFrame({"기준": [0]})).mark_rule(
        color="#a0adba", strokeDash=[4, 4], strokeWidth=1
    ).encode(y="기준:Q")
    lines = (
        alt.Chart(long)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=34), strokeWidth=2.6)
        .encode(
            x=alt.X(
                "일자:T",
                title=None,
                scale=alt.Scale(domain=date_domain),
                axis=alt.Axis(format=date_format, grid=False, labelColor="#64748b"),
            ),
            y=alt.Y(
                "누적수익률:Q",
                title="기준일 대비 (%)",
                scale=alt.Scale(domain=domain, zero=False, nice=False),
                axis=alt.Axis(format="+.1f", grid=True, gridColor="#e5ebf1", labelColor="#64748b", titleColor="#64748b"),
            ),
            color=alt.Color(
                "시리즈:N",
                title=None,
                scale=alt.Scale(domain=["T30", "SPY"], range=["#078fa5", "#8291a3"]),
                legend=alt.Legend(orient="top", direction="horizontal", labelColor="#526176"),
            ),
            tooltip=[
                alt.Tooltip("일자:T", title="일자", format="%Y-%m-%d"),
                alt.Tooltip("시리즈:N", title="지수"),
                alt.Tooltip("누적수익률:Q", title="누적수익률", format="+.2f"),
            ],
        )
    )
    return (zero_line + lines).properties(height=height).configure_view(strokeOpacity=0)


def index_point_chart(
    df: pd.DataFrame, height: int = 390, date_format: str = "%m/%d"
) -> alt.Chart:
    long = df.melt(
        id_vars="일자",
        value_vars=["지수", "SPY지수"],
        var_name="시리즈",
        value_name="지수 포인트",
    )
    long["시리즈"] = long["시리즈"].map({"지수": "T30", "SPY지수": "SPY"})
    y_min = float(long["지수 포인트"].min())
    y_max = float(long["지수 포인트"].max())
    padding = max((y_max - y_min) * 0.13, 2.0)
    domain = [y_min - padding, y_max + padding]
    date_domain = padded_date_domain(long["일자"])

    base_line = alt.Chart(pd.DataFrame({"기준": [1000]})).mark_rule(
        color="#a0adba", strokeDash=[4, 4], strokeWidth=1
    ).encode(y="기준:Q")
    lines = (
        alt.Chart(long)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=34), strokeWidth=2.6)
        .encode(
            x=alt.X(
                "일자:T",
                title=None,
                scale=alt.Scale(domain=date_domain),
                axis=alt.Axis(format=date_format, grid=False, labelColor="#64748b"),
            ),
            y=alt.Y(
                "지수 포인트:Q",
                title="지수 포인트",
                scale=alt.Scale(domain=domain, zero=False, nice=False),
                axis=alt.Axis(format=",.0f", grid=True, gridColor="#e5ebf1", labelColor="#64748b", titleColor="#64748b"),
            ),
            color=alt.Color(
                "시리즈:N",
                title=None,
                scale=alt.Scale(domain=["T30", "SPY"], range=["#078fa5", "#8291a3"]),
                legend=alt.Legend(orient="top", direction="horizontal", labelColor="#526176"),
            ),
            tooltip=[
                alt.Tooltip("일자:T", title="일자", format="%Y-%m-%d"),
                alt.Tooltip("시리즈:N", title="지수"),
                alt.Tooltip("지수 포인트:Q", title="지수 포인트", format=",.2f"),
            ],
        )
    )
    return (base_line + lines).properties(height=height).configure_view(strokeOpacity=0)


def regime_comparison_chart(df: pd.DataFrame, height: int = 250) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, width=34)
        .encode(
            x=alt.X("구간:N", title=None, sort=["트럼프 2기", "출범 이전"], axis=alt.Axis(labelAngle=0, labelColor="#526176")),
            xOffset="시리즈:N",
            y=alt.Y(
                "누적수익률:Q",
                title="누적수익률 (%)",
                axis=alt.Axis(format="+.0f", gridColor="#e5ebf1", labelColor="#64748b", titleColor="#64748b"),
            ),
            color=alt.Color(
                "시리즈:N",
                title=None,
                scale=alt.Scale(domain=["T30", "SPY"], range=["#0797ad", "#9aa8b7"]),
                legend=alt.Legend(orient="top", direction="horizontal", labelColor="#526176"),
            ),
            tooltip=["구간:N", "시리즈:N", alt.Tooltip("누적수익률:Q", format="+.2f")],
        )
        .properties(height=height)
        .configure_view(strokeOpacity=0)
    )


def daily_return_chart(df: pd.DataFrame, height: int = 170) -> alt.Chart:
    daily = df.dropna(subset=["T30 일간등락"])
    date_domain = padded_date_domain(daily["일자"])
    bars = (
        alt.Chart(daily)
        .mark_bar(size=12, cornerRadius=2)
        .encode(
            x=alt.X(
                "일자:T",
                title=None,
                scale=alt.Scale(domain=date_domain),
                axis=alt.Axis(format="%m/%d", grid=False, labelColor="#64748b"),
            ),
            y=alt.Y(
                "T30 일간등락:Q",
                title="일간 등락 (%)",
                scale=alt.Scale(zero=True),
                axis=alt.Axis(format="+.1f", grid=True, gridColor="#e5ebf1", labelColor="#64748b", titleColor="#64748b"),
            ),
            color=alt.Color(
                "등락:N",
                title=None,
                scale=alt.Scale(domain=["상승", "하락"], range=["#0797ad", "#d85f6c"]),
                legend=alt.Legend(orient="top", direction="horizontal", labelColor="#526176"),
            ),
            tooltip=[
                alt.Tooltip("일자:T", title="일자", format="%Y-%m-%d"),
                alt.Tooltip("T30 일간등락:Q", title="일간 등락률", format="+.2f"),
            ],
        )
    )
    return bars.properties(height=height).configure_view(strokeOpacity=0)


def section_header(label: str, title: str, copy: str) -> None:
    st.markdown(
        f'<div class="section-label">{label}</div><div class="section-title">{title}</div><div class="section-copy">{copy}</div>',
        unsafe_allow_html=True,
    )


AXIS_CARD_CLASS = {
    "반도체·AI": "axis-ai",
    "방위·우주": "axis-defense",
    "에너지": "axis-energy",
    "핵심소재": "axis-materials",
    "바이오": "axis-bio",
    "금융": "axis-finance",
}


def holding_card(row: pd.Series) -> str:
    rank = int(row["순위"])
    ticker = escape(str(row["티커"]))
    company = escape(str(row["기업명"]))
    axis = escape(str(row["정책축"]))
    score_value = float(row["총점"])
    score = f"{score_value:g}"
    benefit1 = escape(str(row["수혜1"]))
    benefit2 = escape(str(row["수혜2"]))
    axis_class = AXIS_CARD_CLASS.get(str(row["정책축"]), "")
    return f"""
    <div class="holding-card {axis_class}">
      <div class="holding-head">
        <span class="holding-rank">RANK {rank:02d}</span>
        <span class="axis-chip">{axis}</span>
      </div>
      <div class="holding-identity">
        <span class="holding-ticker">{ticker}</span>
        <span class="holding-score">총점 {score} · 동일가중 3.33%</span>
      </div>
      <div class="holding-company">{company}</div>
      <div class="benefit-list">
        <div class="benefit-item"><span class="benefit-bullet"></span><span>{benefit1}</span></div>
        <div class="benefit-item"><span class="benefit-bullet"></span><span>{benefit2}</span></div>
      </div>
    </div>
    """


current = load_current()
constituents = load_constituents()
backtest_data = load_backtest()
performance = performance_frame(current)
latest = current.iloc[-1]
today_kst = datetime.now(ZoneInfo("Asia/Seoul"))
today_label = f"{today_kst.year}년 {today_kst.month}월 {today_kst.day}일"
current_return = (latest["지수"] / current.iloc[0]["지수"] - 1) * 100
spy_return = (latest["SPY지수"] / current.iloc[0]["SPY지수"] - 1) * 100
daily_moves = performance["T30 일간등락"].dropna()
best_day = float(daily_moves.max())
worst_day = float(daily_moves.min())
positive_ratio = float((daily_moves > 0).mean() * 100)

TRUMP_START = pd.Timestamp("2025-01-21")
PRE_TRUMP_END = pd.Timestamp("2025-01-13")
BACKTEST_END = pd.Timestamp("2026-06-29")
trump_period = backtest_data[
    (backtest_data["일자"] >= TRUMP_START) & (backtest_data["일자"] <= BACKTEST_END)
]
pre_trump_period = backtest_data[backtest_data["일자"] <= PRE_TRUMP_END]
trump_h30_stats = period_stats(trump_period, "T30")
trump_spy_stats = period_stats(trump_period, "SPY")
pre_trump_h30_stats = period_stats(pre_trump_period, "T30")
pre_trump_spy_stats = period_stats(pre_trump_period, "SPY")

st.markdown(
    f"""
    <div class="hero-panel">
      <div>
        <div class="hero-kicker">AMERICAN GLOBAL HEGEMONY TOP30 INDEX</div>
        <div class="hero-title">미국 글로벌 헤게모니<br><span>TOP30 지수</span></div>
        <div class="hero-copy">미국 글로벌 헤게모니 TOP30 지수는 기준일 현재 S&amp;P500 구성종목을 대상으로 정책축 적합성, 10-K 정책 문맥, 미국 매출 순도를 평가해 30종목을 선정합니다. 종목은 동일가중으로 구성하고 정책축당 최대 6종목으로 제한하며, 배당을 반영하지 않는 가격지수로 산출합니다.</div>
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
    f"""
    <div class="period-grid">
      <div class="period-card purple"><em>PRIMARY BACKTEST · TRUMP 2.0</em><b>트럼프 2기 성과 {trump_h30_stats['total_return']:+.1f}%</b><small>2025.01.21 — 2026.06.29 · 주간 체인 지수</small></div>
      <div class="period-card cyan"><em>CURRENT · OFFICIAL</em><b>현재 공식 지수</b><small>2026.07.01 — 현재 · 기준값 1,000</small></div>
    </div>
    """,
    unsafe_allow_html=True,
)

overview, backtest_tab, live, holdings, methodology = st.tabs(
    ["Overview", "백테스트", "현재 지수", "구성종목", "방법론·감사"]
)

with overview:
    profile_download, profile_date = st.columns([1, 1])
    with profile_download:
        st.download_button(
            "▣ Methodology Summary",
            data=(ROOT / "methodology.txt").read_text(encoding="utf-8"),
            file_name="T30_방법론_요약.txt",
            mime="text/plain",
            key="overview_methodology_download",
        )
    with profile_date:
        st.markdown(
            f'<div class="profile-toolbar">공식 산출 개시일&nbsp; <b>2026.07.01</b>&nbsp;&nbsp;·&nbsp;&nbsp;데이터 기준일&nbsp; <b>{latest["일자"].strftime("%Y.%m.%d")}</b></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="index-spec-grid">
          <div class="index-spec"><span class="spec-label">지수 유형</span><div class="spec-value"><span class="spec-chip">Price Index</span><span class="spec-chip">Equal Weight</span></div></div>
          <div class="index-spec"><span class="spec-label">유니버스</span><div class="spec-value">S&amp;P 500 구성종목</div><span class="spec-note">매년 6월 30일 기준</span></div>
          <div class="index-spec"><span class="spec-label">벤치마크</span><div class="spec-value">SPY</div><span class="spec-note">S&amp;P 500 ETF</span></div>
          <div class="index-spec"><span class="spec-label">기준값</span><div class="spec-value">1,000</div><span class="spec-note">2026년 7월 1일</span></div>
          <div class="index-spec"><span class="spec-label">리밸런싱</span><div class="spec-value">연 1회</div><span class="spec-note">7월 첫 영업일 적용</span></div>
          <div class="index-spec"><span class="spec-label">구성 규칙</span><div class="spec-value">30종목</div><span class="spec-note">정책축당 최대 6종목 · 종목당 3.33%</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("현재 지수", f"{latest['지수']:,.2f}", f"{current_return:+.2f}%")
    c2.metric("SPY 대비", f"{current_return - spy_return:+.2f}%p")
    c3.metric("트럼프 2기 백테스트", f"{trump_h30_stats['total_return']:+.1f}%", f"SPY {trump_spy_stats['total_return']:+.1f}%", delta_color="off")
    c4.metric("최종 구성", "30종목", "동일가중 3.33%")

    section_header("Official track", "공식 지수 누적수익률", "기준일을 0%로 두고 실제 등락 범위만 확대해 표시합니다.")
    st.altair_chart(cumulative_return_chart(performance, 370), width="stretch")

    section_header("Index points", "공식 지수 점수(포인트)", "2026년 7월 1일을 1,000으로 두고 T30과 SPY의 원지수 수준을 비교합니다.")
    st.altair_chart(index_point_chart(current, 370), width="stretch")
    st.markdown(
        f'<div class="live-note">최신 데이터: {latest["일자"].strftime("%Y-%m-%d")} 종가 · 동일가중 가격지수 · 배당 미반영 · 백테스트 구간과 연결하지 않음</div>',
        unsafe_allow_html=True,
    )

    section_header("Composition", "2026 정책축 구성", "최종 30종목의 정책축별 편입 수입니다.")
    sector_counts = constituents.groupby("정책축", sort=False).size().rename("종목수")
    sector_df = sector_counts.reset_index()
    sector_chart = (
        alt.Chart(sector_df)
        .mark_bar(color="#0797ad", cornerRadiusEnd=4, height=18)
        .encode(
            x=alt.X("종목수:Q", title=None, axis=alt.Axis(tickMinStep=1, gridColor="#e5ebf1", labelColor="#64748b")),
            y=alt.Y("정책축:N", title=None, sort=None, axis=alt.Axis(labelColor="#526176", labelLimit=240)),
            tooltip=["정책축:N", "종목수:Q"],
        )
        .properties(height=300)
        .configure_view(strokeOpacity=0)
    )
    st.altair_chart(sector_chart, width="stretch")

with backtest_tab:
    section_header(
        "Primary regime · Trump 2.0",
        "기간을 선택해 보는 백테스트",
        "트럼프 2기 출범 이후를 기본 구간으로 두고, 이전 구간과 장기 근사치는 보조 정보로 분리했습니다.",
    )

    period_option = st.radio(
        "분석 구간",
        ["트럼프 2기", "출범 이전", "전체 3년", "직접 설정"],
        horizontal=True,
        help="주간 체인 지수의 관측 구간을 선택합니다.",
    )

    if period_option == "트럼프 2기":
        selected_start, selected_end = TRUMP_START, BACKTEST_END
        period_label = "트럼프 2기"
    elif period_option == "출범 이전":
        selected_start, selected_end = backtest_data["일자"].min(), PRE_TRUMP_END
        period_label = "출범 이전"
    elif period_option == "전체 3년":
        selected_start, selected_end = backtest_data["일자"].min(), BACKTEST_END
        period_label = "전체 3년"
    else:
        custom_range = st.date_input(
            "시작일 — 종료일",
            value=(TRUMP_START.date(), BACKTEST_END.date()),
            min_value=backtest_data["일자"].min().date(),
            max_value=BACKTEST_END.date(),
        )
        if isinstance(custom_range, (tuple, list)) and len(custom_range) == 2:
            selected_start, selected_end = map(pd.Timestamp, custom_range)
        else:
            selected_start, selected_end = TRUMP_START, BACKTEST_END
        period_label = "직접 설정"

    selected_period = backtest_data[
        (backtest_data["일자"] >= selected_start) & (backtest_data["일자"] <= selected_end)
    ]

    if len(selected_period) < 2:
        st.warning("성과를 계산하려면 서로 다른 주간 관측치가 2개 이상 필요합니다.")
    else:
        h30_stats = period_stats(selected_period, "T30")
        selected_spy_stats = period_stats(selected_period, "SPY")
        selected_performance = backtest_performance_frame(selected_period)

        st.caption(
            f"{period_label} · {selected_period['일자'].iloc[0].strftime('%Y-%m-%d')} — "
            f"{selected_period['일자'].iloc[-1].strftime('%Y-%m-%d')} · {len(selected_period)}주 관측"
        )
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("T30 누적수익", f"{h30_stats['total_return']:+.1f}%", f"SPY {selected_spy_stats['total_return']:+.1f}%", delta_color="off")
        c2.metric("CAGR", f"{h30_stats['cagr']:.1f}%", f"SPY {selected_spy_stats['cagr']:.1f}%", delta_color="off")
        c3.metric("최대낙폭", f"{h30_stats['mdd']:.1f}%", f"SPY {selected_spy_stats['mdd']:.1f}%", delta_color="off")
        c4.metric("연환산 변동성", f"{h30_stats['volatility']:.1f}%", f"SPY {selected_spy_stats['volatility']:.1f}%", delta_color="off")
        c5.metric("샤프", f"{h30_stats['sharpe']:.2f}", f"SPY {selected_spy_stats['sharpe']:.2f}", delta_color="off")

        section_header("Weekly chain", "선택 구간 누적수익률", "선택한 첫 관측치를 0%로 재설정해 T30과 SPY의 흐름을 비교합니다.")
        st.altair_chart(cumulative_return_chart(selected_performance, 430, "%Y.%m"), width="stretch")
        st.markdown(
            '<div class="live-note">주간 체인 지수 · 매년 빈티지 교체를 반영한 시점가용(PIT) 백테스트 · 2026-06-29 종료 · 2026-07-01 공식 지수와 비연결</div>',
            unsafe_allow_html=True,
        )

    section_header("Supporting context", "출범 전후 성과 비교", "트럼프 2기를 핵심 구간으로 보고, 그 이전 관측 구간은 배경 정보로만 제시합니다.")
    comparison = pd.DataFrame(
        [
            {"구간": "트럼프 2기", "시리즈": "T30", "누적수익률": trump_h30_stats["total_return"]},
            {"구간": "트럼프 2기", "시리즈": "SPY", "누적수익률": trump_spy_stats["total_return"]},
            {"구간": "출범 이전", "시리즈": "T30", "누적수익률": pre_trump_h30_stats["total_return"]},
            {"구간": "출범 이전", "시리즈": "SPY", "누적수익률": pre_trump_spy_stats["total_return"]},
        ]
    )
    compare_chart, compare_copy = st.columns([1.15, 0.85])
    with compare_chart:
        st.altair_chart(regime_comparison_chart(comparison), width="stretch")
    with compare_copy:
        st.markdown(
            f"""
            <div class="data-note">
            <b>트럼프 2기</b> · 2025-01-21 — 2026-06-29<br>
            T30 {trump_h30_stats['total_return']:+.1f}% · SPY {trump_spy_stats['total_return']:+.1f}%<br>
            최대낙폭 T30 {trump_h30_stats['mdd']:.1f}% · SPY {trump_spy_stats['mdd']:.1f}%<br><br>
            <b>출범 이전</b> · 2023-07-03 — 2025-01-13<br>
            T30 {pre_trump_h30_stats['total_return']:+.1f}% · SPY {pre_trump_spy_stats['total_return']:+.1f}%<br>
            최대낙폭 T30 {pre_trump_h30_stats['mdd']:.1f}% · SPY {pre_trump_spy_stats['mdd']:.1f}%
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("7년 장기 맥락 보기 · 근사 요약"):
        st.caption("2019.07 — 2026.06 · 확정 7개 빈티지 · 일별 에쿼티커브 미확정")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("누적수익", "+123.6%", "SPY +144.4%", delta_color="off")
        c2.metric("CAGR", "12.0%", "SPY 13.4%", delta_color="off")
        c3.metric("최대낙폭", "−32%", "SPY −32%", delta_color="off")
        c4.metric("샤프", "0.43", "SPY 0.51", delta_color="off")
        st.markdown(
            '<div class="data-note">7년 성과는 누적수익 역산·반올림 근사치입니다. 정확한 시계열이 확정되기 전까지 장기 방향을 보는 참고 수치로만 사용합니다.</div>',
            unsafe_allow_html=True,
        )
        st.subheader("연도별 정책축 구성 변화")
        sector_history = pd.read_csv(DATA / "sector_history.csv").set_index("연도")
        st.bar_chart(sector_history, stack=True, height=410)
        st.caption("매년 30종목 · 정책축당 최대 6종목 · 2019~2025 빈티지")

with live:
    section_header("Current · Official", f"{today_label} 공식 지수", "누적 방향과 일간 진폭을 분리해 표시합니다.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("최신 종가", f"{latest['지수']:,.2f}", latest["일자"].strftime("%Y-%m-%d"))
    c2.metric("출시 후 수익률", f"{current_return:+.2f}%")
    c3.metric("SPY 대비", f"{current_return - spy_return:+.2f}%p")
    c4.metric("최대낙폭", f"{max_drawdown(current['지수']):.2f}%")

    section_header("Cumulative", "기준일 대비 누적수익률", "Y축을 실제 관측 범위로 확대해 T30과 SPY의 상대 흐름을 비교합니다.")
    st.altair_chart(cumulative_return_chart(performance, 430), width="stretch")

    section_header("Index points", "공식 지수 점수(포인트)", "기준값 1,000에서 출발한 T30과 SPY의 원지수 흐름을 표시합니다.")
    st.altair_chart(index_point_chart(current, 430), width="stretch")

    section_header("Daily range", "T30 일간 등락률", "상승일과 하락일의 진폭을 별도 막대로 확인합니다.")
    st.altair_chart(daily_return_chart(performance), width="stretch")

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("기간 고점", f"{current['지수'].max():,.2f}")
    p2.metric("기간 저점", f"{current['지수'].min():,.2f}")
    p3.metric("최대 일간 등락", f"{best_day:+.2f}%", f"최저 {worst_day:+.2f}%")
    p4.metric("상승일 비중", f"{positive_ratio:.1f}%", f"{int((daily_moves > 0).sum())}/{len(daily_moves)}일")

    st.markdown('<div class="live-note">누적수익률 차트는 0% 기준선을 중심으로 관측 구간을 확대합니다. 원지수는 아래 표에서 소수점 네 자리까지 확인할 수 있습니다.</div>', unsafe_allow_html=True)
    st.dataframe(
        performance[["일자", "지수", "SPY지수", "T30 누적수익률", "T30 일간등락"]].sort_values("일자", ascending=False),
        hide_index=True,
        width="stretch",
        column_config={
            "일자": st.column_config.DateColumn("일자", format="YYYY-MM-DD"),
            "지수": st.column_config.NumberColumn("T30", format="%.4f"),
            "SPY지수": st.column_config.NumberColumn("SPY", format="%.4f"),
            "T30 누적수익률": st.column_config.NumberColumn("누적수익률", format="%+.2f%%"),
            "T30 일간등락": st.column_config.NumberColumn("일간등락", format="%+.2f%%"),
        },
    )

with holdings:
    section_header(
        "Constituents",
        "최종 30종목과 정책 수혜",
        "카드로 빠르게 훑어보고, 필요할 때 간단한 표로 전환할 수 있습니다.",
    )
    search_col, axis_col, view_col = st.columns([1.55, 1.05, 0.8])
    query = search_col.text_input("종목 검색", placeholder="티커·기업명·수혜 내용")
    axes = axis_col.multiselect("정책축", constituents["정책축"].drop_duplicates().tolist())
    view_mode = view_col.segmented_control(
        "보기 방식", ["카드", "간단 표"], default="카드"
    )

    filtered = constituents.copy()
    if query:
        searchable = filtered[["티커", "기업명", "정책축", "수혜1", "수혜2"]]
        mask = searchable.astype(str).apply(
            lambda row: row.str.contains(query, case=False, na=False).any(), axis=1
        )
        filtered = filtered[mask]
    if axes:
        filtered = filtered[filtered["정책축"].isin(axes)]

    shown = filtered.copy()
    shown["주요 정책 수혜"] = "• " + shown["수혜1"] + "\n• " + shown["수혜2"]
    st.markdown(
        f'<div class="holdings-summary"><b>{len(shown)}개 기업</b><span class="summary-dot"></span><span>{shown["정책축"].nunique()}개 정책축</span><span class="summary-dot"></span><span>종목당 3.33% 동일가중</span></div>',
        unsafe_allow_html=True,
    )

    if shown.empty:
        st.info("조건에 맞는 종목이 없습니다. 검색어나 정책축 필터를 조정해 주세요.")
    elif view_mode == "간단 표":
        st.dataframe(
            shown[["순위", "티커", "기업명", "정책축", "총점", "주요 정책 수혜"]],
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
            },
        )
    else:
        records = [row for _, row in shown.sort_values("순위").iterrows()]
        for offset in range(0, len(records), 2):
            card_columns = st.columns(2)
            for column, row in zip(card_columns, records[offset : offset + 2]):
                with column:
                    st.markdown(holding_card(row), unsafe_allow_html=True)

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
        file_name="T30_방법론_요약.txt",
        mime="text/plain",
    )

st.markdown(
    '<div class="footer">INDEX TEAM 1 · AMERICAN GLOBAL HEGEMONY TOP30 · Research prototype · Not investment advice</div>',
    unsafe_allow_html=True,
)
