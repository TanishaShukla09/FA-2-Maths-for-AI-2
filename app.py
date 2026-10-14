from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="LogiSight Delivery Dashboard", page_icon="🛵", layout="wide")
TRAFFIC = ["Low", "Medium", "High", "Jam"]
FILTERS = ["Weather", "Traffic", "Vehicle", "Area", "Category"]

# ---------- Colour themes (close screen values of Pantone colours) ----------
THEMES = {
    "Fondant, Apricot, Blues": dict(  # Chocolate Fondant, Apricot Illusion, Dress Blues
        bg="#FBF2E9", card="#FFFFFF", side="#3B2A24", side2="#4F3A32", stext="#F7E6D8", text="#2B2420",
        muted="#7B6A5F", grid="#EFE3D8", main="#2A3244", accent="#D9825B", low="#FBEBDD", btn="#D9825B", btnt="#FFFFFF",
        cats=["#2A3244", "#D9825B", "#6F7F99", "#F0BC9B", "#8C6B5A", "#B9C2D3"]),
    "Plum Wine, Olive": dict(  # Alabaster, Plum Wine, Olive Drab
        bg="#F2EFE7", card="#FFFFFF", side="#5C2A45", side2="#723A58", stext="#F4EAF0", text="#2A2327",
        muted="#716870", grid="#E7E2D8", main="#6B6A45", accent="#8A2F5E", low="#EEEBDD", btn="#A43F73", btnt="#FFFFFF",
        cats=["#6B6A45", "#8A2F5E", "#A8A77B", "#C792AE", "#4D4C31", "#D8D6C0"]),
    "Plum, Popcorn, Cerulean": dict(  # Chocolate Plum, Popcorn, Cerulean
        bg="#FCF6E2", card="#FFFFFF", side="#4A2630", side2="#613642", stext="#FBEFD0", text="#2C1D21",
        muted="#7A6A62", grid="#EFE6C9", main="#5E86AE", accent="#4A2630", low="#E9F0F7", btn="#F0D27A", btnt="#4A2630",
        cats=["#5E86AE", "#4A2630", "#98B4D4", "#F0D27A", "#8D5A67", "#C9D8E8"]),
    "Marine, Red, Lemon": dict(  # Marine Blue, Red, Lemon
        bg="#F6F4EE", card="#FFFFFF", side="#12355B", side2="#1D4A7A", stext="#EEF3F9", text="#14233A",
        muted="#667589", grid="#E4E8EE", main="#2F5D8C", accent="#B8232F", low="#E8EEF5", btn="#B8232F", btnt="#FFFFFF",
        cats=["#2F5D8C", "#B8232F", "#F3D34A", "#8FA9C7", "#12355B", "#E7A8AD"]),
}
st.session_state.setdefault("theme", list(THEMES)[0])
P = THEMES[st.session_state["theme"]]
FONT = "Inter, sans-serif"

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap');
.stApp {{background:{P['bg']}; color:{P['text']}; font-family:'Inter',sans-serif;}}
.block-container {{max-width:1400px; padding-top:2.5rem;}}
h1, h2, h3 {{font-family:'Playfair Display',serif !important; color:{P['text']} !important;}}
[data-testid="stHeader"] {{background:transparent;}}
[data-testid="stSidebar"] {{background:{P['side']}; min-width:300px;}}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] summary, [data-testid="stSidebar"] span {{color:{P['stext']} !important;}}
[data-testid="stSidebar"] [data-testid="stExpander"] {{border:1px solid rgba(255,255,255,.2); border-radius:10px;}}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {{background:transparent !important;}}
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{background:rgba(255,255,255,.10) !important;}}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-rac][role="group"],
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-rac] {{background:{P['side2']} !important; border:1px solid rgba(255,255,255,.18) !important;}}
[data-testid="stSidebar"] [data-tag] {{background:rgba(255,255,255,.16) !important; color:{P['stext']} !important; border-radius:6px;}}
[data-testid="stSidebar"] [data-testid="stSelectbox"] * {{color:{P['stext']} !important;}}
[data-testid="stSidebar"] .stButton button {{background:{P['btn']}; border:none; border-radius:8px; width:100%;}}
[data-testid="stSidebar"] .stButton button p {{color:{P['btnt']} !important;}}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{border:none; padding:0;}}
[data-testid="stMetric"] {{background:{P['card']}; border-left:5px solid {P['accent']}; border-radius:12px;
  padding:14px 18px; box-shadow:0 1px 6px rgba(0,0,0,.07);}}
[data-testid="stMetricLabel"] p {{color:{P['muted']}; font-weight:500;}}
[data-testid="stMetricValue"] {{font-family:'Playfair Display',serif; color:{P['text']};}}
.stTabs [data-baseweb="tab"] {{font-weight:600; color:{P['muted']};}}
.stTabs [aria-selected="true"] {{color:{P['accent']};}}
.stTabs [data-baseweb="tab-highlight"] {{background:{P['accent']};}}
[data-testid="stPlotlyChart"] {{background:{P['card']}; border-radius:14px; padding:8px; box-shadow:0 1px 6px rgba(0,0,0,.07);}}
[data-testid="stCaptionContainer"] {{border-left:3px solid {P['accent']}; padding-left:10px; opacity:1;}}
[data-testid="stMain"] [data-testid="stCaptionContainer"] p {{color:{P['text']} !important; opacity:.85; font-size:.92rem;}}
</style>""", unsafe_allow_html=True)


# ---------- Stage 4: load, clean and prepare ----------
@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "Last_mile_Delivery_Data.csv")
    for c in FILTERS:  # strip spaces; the text "NaN" becomes a real missing value
        df[c] = df[c].astype(str).str.strip().replace({"NaN": np.nan, "nan": np.nan})
    df["Area"] = df["Area"].replace({"Metropolitian": "Metropolitan"})  # typo in the data
    df["Vehicle"] = df["Vehicle"].str.title()
    df = df.dropna(subset=FILTERS + ["Agent_Rating"])  # drop rows with missing values
    df = df[df["Agent_Rating"] <= 5].copy()  # ratings above 5 are invalid
    df["Order_Hour"] = pd.to_datetime(df["Order_Time"], format="%H:%M:%S", errors="coerce").dt.hour
    df["Age_Group"] = pd.cut(df["Agent_Age"], [0, 24, 30, 39], labels=["Under 25", "25-30", "31-39"])
    return df


df = load_data()
LATE = df["Delivery_Time"].mean() + df["Delivery_Time"].std()  # late = mean + 1 standard deviation
df["Late"] = df["Delivery_Time"] > LATE

# ---------- Stage 6: compact sidebar filters ----------
OPTIONS = {c: sorted(df[c].unique()) for c in FILTERS}
RATING_RANGE = (float(df["Agent_Rating"].min()), 5.0)
for c in FILTERS:
    st.session_state.setdefault(c, OPTIONS[c])
st.session_state.setdefault("rating", RATING_RANGE)


def reset_filters():
    for c in FILTERS:
        st.session_state[c] = OPTIONS[c]
    st.session_state["rating"] = RATING_RANGE


st.sidebar.title("Filters")
st.sidebar.button("Reset all filters", on_click=reset_filters)
summary = st.sidebar.empty()
for c in FILTERS:
    with st.sidebar.expander(c):
        st.multiselect(c, OPTIONS[c], key=c, label_visibility="collapsed")
st.sidebar.slider("Agent rating", RATING_RANGE[0], 5.0, step=0.1, key="rating")
with st.sidebar.expander("Theme"):
    st.selectbox("Colour palette", list(THEMES), key="theme", label_visibility="collapsed")
st.sidebar.caption(f"Late delivery = longer than mean + 1 SD ({LATE:.0f} min).")

mask = df["Agent_Rating"].between(*st.session_state["rating"])
for c in FILTERS:
    mask &= df[c].isin(st.session_state[c])
f = df[mask]
summary.caption(f"Showing {len(f):,} of {len(df):,} deliveries")
if f.empty:
    st.warning("No deliveries match these filters. Widen your selection in the sidebar.")
    st.stop()

# ---------- Header and key metrics ----------
st.title("LogiSight Delivery Performance Dashboard")
st.write("Find what slows last-mile deliveries down. Use the sidebar to drill into any situation.")
k = st.columns(4)
k[0].metric("Orders", f"{len(f):,}")
k[1].metric("Avg delivery time", f"{f['Delivery_Time'].mean():.0f} min")
k[2].metric("Late deliveries", f"{f['Late'].mean():.1%}")
k[3].metric("Avg agent rating", f"{f['Agent_Rating'].mean():.2f}")


def show(fig, caption):
    fig.update_layout(margin=dict(t=50, b=10, l=10, r=10), plot_bgcolor=P["card"], paper_bgcolor=P["card"],
                      font=dict(family=FONT, color=P["text"]),
                      title_font=dict(family="Playfair Display, serif", size=18))
    fig.update_yaxes(gridcolor=P["grid"], zerolinecolor=P["grid"])
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig)
    st.caption(caption)


def bar(g, x, y, title, unit):  # bar chart with the highest bar in the accent colour
    g = g.assign(Key=np.where(g[y] == g[y].max(), "Highest", "Other"))
    fig = px.bar(g, x=x, y=y, color="Key", title=title, text_auto=".0f" if unit == "min" else ".1%",
                 color_discrete_map={"Highest": P["accent"], "Other": P["main"]}, labels={y: unit})
    if unit == "%":
        fig.update_yaxes(tickformat=".0%")
    return fig.update_layout(showlegend=False)


# ---------- Stage 5: visualisations ----------
tab1, tab2, tab3 = st.tabs(["Delays", "Vehicles and agents", "Areas and categories"])

with tab1:
    g = f.groupby(["Traffic", "Weather"], as_index=False)["Delivery_Time"].mean()
    fig = px.bar(g, x="Traffic", y="Delivery_Time", color="Weather", barmode="group",
                 title="Delay Analyzer: average delivery time by traffic and weather",
                 category_orders={"Traffic": TRAFFIC}, labels={"Delivery_Time": "Avg minutes"},
                 color_discrete_sequence=P["cats"])
    r = g.loc[g["Delivery_Time"].idxmax()]
    show(fig, f"Slowest combination: {r['Traffic']} traffic with {r['Weather']} weather ({r['Delivery_Time']:.0f} min).")
    c1, c2 = st.columns(2)
    with c1:  # optional chart 1
        h = f.groupby("Order_Hour")["Delivery_Time"].mean().reindex(range(24)).rename_axis("Order_Hour").reset_index()
        fig = px.line(h, x="Order_Hour", y="Delivery_Time", markers=True, title="Average delivery time by order hour",
                      labels={"Order_Hour": "Hour of day", "Delivery_Time": "Avg minutes"})
        fig.update_traces(line_color=P["main"], marker_color=P["accent"])
        show(fig, f"Slowest hour: {int(h.loc[h['Delivery_Time'].idxmax(), 'Order_Hour'])}:00 ({h['Delivery_Time'].max():.0f} min).")
    with c2:  # optional chart 2
        t = f.groupby("Traffic", as_index=False)["Late"].mean()
        t["Traffic"] = pd.Categorical(t["Traffic"], TRAFFIC, ordered=True)
        t = t.sort_values("Traffic")
        show(bar(t, "Traffic", "Late", "Late deliveries by traffic", "%"),
             f"{t.loc[t['Late'].idxmax(), 'Traffic']} traffic has the highest share of late deliveries.")

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        v = f.groupby("Vehicle", as_index=False)["Delivery_Time"].mean()
        show(bar(v, "Vehicle", "Delivery_Time", "Vehicle Comparison: average delivery time", "min"),
             f"Fastest: {v.loc[v['Delivery_Time'].idxmin(), 'Vehicle']} ({v['Delivery_Time'].min():.0f} min).")
    with c2:
        s = f.sample(min(len(f), 3000), random_state=1).copy()
        s["Agent rating"] = s["Agent_Rating"] + np.random.default_rng(1).uniform(-0.04, 0.04, len(s))  # jitter
        fig = px.scatter(s, x="Agent rating", y="Delivery_Time", color="Age_Group", opacity=0.5,
                         title="Agent Performance: rating vs delivery time",
                         labels={"Delivery_Time": "Delivery time (min)"},
                         category_orders={"Age_Group": ["Under 25", "25-30", "31-39"]},
                         color_discrete_sequence=[P["cats"][2], P["main"], P["accent"]])
        fig.update_traces(marker_size=5)
        show(fig, f"Sample of up to 3,000 deliveries (small jitter so dots do not overlap). Correlation between rating and time: "
                  f"{f['Agent_Rating'].corr(f['Delivery_Time']):.2f}.")

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        p = f.pivot_table(index="Area", columns="Traffic", values="Delivery_Time", aggfunc="mean")
        p = p[[c for c in TRAFFIC if c in p.columns]]
        fig = px.imshow(p, text_auto=".0f", aspect="auto", title="Area Heatmap: average delivery time (min)",
                        color_continuous_scale=[P["low"], P["accent"]], labels={"color": "Avg min"})
        area, traffic = p.stack().idxmax()
        show(fig, f"Slowest cell: {area} area in {traffic} traffic. Blank cells have no deliveries.")
    with c2:
        order = list(f.groupby("Category")["Delivery_Time"].median().sort_values().index)
        fig = px.box(f, x="Category", y="Delivery_Time", category_orders={"Category": order},
                     title="Category Visualizer: delivery time distribution",
                     labels={"Delivery_Time": "Delivery time (min)"}, color_discrete_sequence=[P["main"]])
        show(fig, f"Lowest median: {order[0]}. Highest median: {order[-1]}.")
