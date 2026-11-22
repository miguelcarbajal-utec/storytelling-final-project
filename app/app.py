import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc
import streamlit as st


st.set_page_config(
    page_title="Observatorio SIDPOL",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def load_data():
    base = "dataset"
    fact = pd.read_csv(
        f"{base}/Fact_Denuncias.csv",
        encoding="utf-8-sig",
        dtype={"UBIGEO_HECHO": "string"},
    )
    calendar = pd.read_csv(f"{base}/Dim_Calendario.csv", encoding="utf-8-sig")
    location = pd.read_csv(
        f"{base}/Dim_Ubicacion.csv",
        encoding="utf-8-sig",
        dtype={"UBIGEO_HECHO": "string"},
    )
    modality = pd.read_csv(f"{base}/Dim_Modalidad.csv", encoding="utf-8-sig")
    channel = pd.read_csv(f"{base}/Dim_Canal.csv", encoding="utf-8-sig")
    time = pd.read_csv(f"{base}/Dim_Franja_Horaria.csv", encoding="utf-8-sig")

    for frame in (fact, calendar, location, modality, channel, time):
        frame.columns = frame.columns.str.strip().str.replace("\ufeff", "", regex=False)

    location["UBIGEO_HECHO"] = location["UBIGEO_HECHO"].str.zfill(6)
    fact["UBIGEO_HECHO"] = fact["UBIGEO_HECHO"].str.zfill(6)

    df = fact.merge(calendar, left_on="Fecha_Key", right_on="Fecha_Key", how="left")
    df = df.merge(location, left_on="UBIGEO_HECHO", right_on="UBIGEO_HECHO", how="left")
    df = df.merge(modality, left_on="ID_Modalidad", right_on="ID_Modalidad", how="left")
    df = df.merge(channel, left_on="ID_Canal", right_on="ID_Canal", how="left")
    df = df.merge(time, left_on="ID_Franja", right_on="ID_Franja", how="left")
    df["Fecha_Key"] = pd.to_datetime(df["Fecha_Key"])
    return df


def format_compact(value, suffix=""):
    if abs(value) >= 1_000_000:
        text = f"{value / 1_000_000:.2f}".rstrip("0").rstrip(".") + " M"
    elif abs(value) >= 1_000:
        text = f"{value / 1_000:.0f} mil"
    else:
        text = f"{value:.0f}"
    return text + suffix


def blank_axis(fig, showgrid=False):
    fig.update_xaxes(showgrid=showgrid, zeroline=False, tickfont=dict(size=9, color="#6f7f96"))
    fig.update_yaxes(showgrid=showgrid, zeroline=False, tickfont=dict(size=9, color="#6f7f96"))
    fig.update_layout(
        margin=dict(l=8, r=8, t=5, b=4),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", color="#2d3e53"),
    )
    return fig


st.markdown(
    """
    <style>
    :root {
      --navy: #10286a;
      --blue: #0877d1;
      --border: #dde5ef;
    }
    html, body, [class*="css"] {
      font-family: Arial, Helvetica, sans-serif;
    }
    .stApp {
      background: #eef3f9;
    }
    header[data-testid="stHeader"] {
      height: 0;
      background: transparent;
    }
    [data-testid="stToolbar"], [data-testid="stDecoration"] {
      display: none;
    }
    .block-container {
      max-width: none;
      padding: 0 30px 8px 30px;
    }
    .topbar {
      height: 76px;
      margin: 0 -30px;
      background: linear-gradient(90deg, #08174f 0%, #102568 50%, #182f78 100%);
      border-bottom: 1px solid #1d3a76;
      display: grid;
      grid-template-columns: 58% 10.5% 10.5% 10.5% 10.5%;
      align-items: center;
      padding: 0 31px;
    }
    .brand-kicker {
      color: #6f94dc;
      font-size: 10px;
      letter-spacing: 1.1px;
      margin-bottom: 9px;
    }
    .brand-title {
      color: #dce8ff;
      font-size: 17px;
      font-weight: 600;
    }
    [data-testid="stSelectbox"] label {
      color: #aab8d4 !important;
      font-size: 9px !important;
      margin-bottom: -5px;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
      background: #102864;
      border: 1px solid #2c4177;
      min-height: 40px;
      color: #dce6fb;
      font-size: 11px;
    }
    [data-testid="stSelectbox"] svg {
      fill: #91a8d1;
    }
    .kpi-row {
      margin: 14px 0 12px 0;
    }
    .kpi {
      height: 96px;
      background: #fff;
      border: 1px solid #dfe7f0;
      border-radius: 7px;
      box-shadow: 0 1px 3px rgba(31,54,82,.10);
      position: relative;
      padding: 16px 18px 10px 22px;
      overflow: hidden;
    }
    .kpi:before {
      content: "";
      width: 6px;
      height: 67px;
      position: absolute;
      left: 9px;
      top: 14px;
      border-radius: 3px;
      background: #163a78;
    }
    .kpi.red:before { background: #ef1111; }
    .kpi.cyan:before { background: #1267a8; }
    .kpi.blue:before { background: #087eda; }
    .kpi-label {
      color: #718097;
      font-size: 9.5px;
      margin-bottom: 12px;
    }
    .kpi-value {
      color: #18375d;
      font-size: 23px;
      font-weight: 500;
      line-height: 1;
    }
    .kpi-value.red { color: #df0606; }
    .kpi-value.blue { color: #0876dc; }
    .kpi-sub {
      color: #738198;
      font-size: 9.5px;
      margin-top: 12px;
    }
    .chart-card {
      height: 246px;
      background: #fff;
      border: 1px solid #dfe7f0;
      border-radius: 7px;
      box-shadow: 0 1px 3px rgba(31,54,82,.09);
      padding: 11px 16px 5px 16px;
      overflow: hidden;
    }
    .chart-card.tight {
      height: 228px;
    }
    .chart-title {
      color: #263a54;
      font-size: 12.5px;
      font-weight: 600;
      margin: 2px 0 4px 0;
    }
    .chart-subtitle {
      color: #7c8ba0;
      font-size: 9.5px;
      margin-bottom: 2px;
    }
    .footer {
      height: 23px;
      display: flex;
      justify-content: space-between;
      align-items: end;
      color: #718198;
      font-size: 8.5px;
      padding: 0 2px;
    }
    [data-testid="stVerticalBlock"] { gap: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)


df = load_data()

# Header
st.markdown(
    """
    <div class="topbar">
      <div>
        <div class="brand-kicker">OBSERVATORIO SIDPOL</div>
        <div class="brand-title">Dashboard Exploratorio de Denuncias Policiales (2018–2026)</div>
      </div>
      <div></div><div></div><div></div>
      <div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns([58, 10.5, 10.5, 10.5, 10.5])
with filter_col1:
    st.markdown("<div style='height:1px'></div>", unsafe_allow_html=True)
with filter_col2:
    year_options = ["2018–2026"] + [str(y) for y in sorted(df["Anio"].unique(), reverse=True)]
    year_choice = st.selectbox("Año", year_options)
with filter_col3:
    region_choice = st.selectbox("Región", ["Todas"] + sorted(df["Departamento"].dropna().unique()))
with filter_col4:
    modality_choice = st.selectbox("Modalidad", ["Todas"] + sorted(df["Modalidad"].dropna().unique()))
with filter_col5:
    channel_choice = st.selectbox("Canal", ["Todos"] + sorted(df["Canal_Denuncia"].dropna().unique()))

# Keep the filter controls aligned with the dark header.
st.markdown(
    "<style>div[data-testid='stHorizontalBlock']:nth-of-type(2){margin-top:-61px;height:61px;align-items:end}</style>",
    unsafe_allow_html=True,
)

filtered = df.copy()
if year_choice != "2018–2026":
    filtered = filtered[filtered["Anio"] == int(year_choice)]
else:
    filtered = filtered
if region_choice != "Todas":
    filtered = filtered[filtered["Departamento"] == region_choice]
if modality_choice != "Todas":
    filtered = filtered[filtered["Modalidad"] == modality_choice]
if channel_choice != "Todos":
    filtered = filtered[filtered["Canal_Denuncia"] == channel_choice]

total = filtered["Cantidad_Denuncias"].sum()
resolved = filtered["Casos_Resueltos"].sum()
resolution_rate = resolved / total if total else 0
loss = filtered["Perdida_Economica_PEN"].sum()
weighted_time = (
    (filtered["Tiempo_Respuesta_Min"] * filtered["Cantidad_Denuncias"]).sum() / total
    if total else 0
)
emergency = filtered[filtered["Estado_Emergencia"] == 1]
emergency_time = (
    (emergency["Tiempo_Respuesta_Min"] * emergency["Cantidad_Denuncias"]).sum()
    / emergency["Cantidad_Denuncias"].sum()
    if emergency["Cantidad_Denuncias"].sum() else 0
)

# KPI cards
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">DENUNCIAS TOTALES</div>'
        f'<div class="kpi-value">{total / 1_000_000:.2f} M</div>'
        '<div class="kpi-sub">9 años (2026*: Ene–Oct)</div></div>',
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f'<div class="kpi red"><div class="kpi-label">TASA DE RESOLUCIÓN</div>'
        f'<div class="kpi-value red">{resolution_rate * 100:.1f}%</div>'
        '<div class="kpi-sub">Extensión: 9.4% (mín.)</div></div>',
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f'<div class="kpi cyan"><div class="kpi-label">PÉRDIDA ECONÓMICA EST.</div>'
        f'<div class="kpi-value">S/ {loss / 1_000_000:.3f} M</div>'
        '<div class="kpi-sub">Pico en 2023: S/ 691 M</div></div>',
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        f'<div class="kpi blue"><div class="kpi-label">TIEMPO PROM. RESPUESTA</div>'
        f'<div class="kpi-value blue">{weighted_time:.1f} min</div>'
        f'<div class="kpi-sub">±0.0 min en Emergencia</div></div>',
        unsafe_allow_html=True,
    )

# Annual evolution
annual = filtered.groupby("Anio", as_index=False)["Cantidad_Denuncias"].sum()
annual["rate"] = (
    filtered.assign(_digital=filtered["ID_Canal"].eq(1).astype(int) * filtered["Cantidad_Denuncias"])
    .groupby("Anio")["_digital"].sum()
    / filtered.groupby("Anio")["Cantidad_Denuncias"].sum()
).values * 100
annual["color"] = annual["Anio"].apply(lambda y: "#173b7a" if y == 2023 else "#ccd0e9")
annual["color"] = annual["Anio"].apply(
    lambda y: "#5e78a5" if y == 2024 else ("#173b7a" if y == 2023 else "#cfd5ee")
)
annual["color"] = annual["Anio"].apply(
    lambda y: "#173b7a" if y == 2023 else ("#677fa8" if y == 2024 else "#ccd3ee")
)

annual_fig = go.Figure()
annual_fig.add_trace(
    go.Bar(
        x=annual["Anio"].astype(str),
        y=annual["Cantidad_Denuncias"] / 1000,
        marker=dict(color=annual["color"]),
        text=[f"{v/1000:.0f}k" for v in annual["Cantidad_Denuncias"]],
        textposition="outside",
        textfont=dict(size=8, color="#52647a"),
        hovertemplate="%{x}: %{y:.0f} mil denuncias<extra></extra>",
        width=0.58,
    )
)
annual_fig.add_trace(
    go.Scatter(
        x=annual["Anio"].astype(str),
        y=annual["rate"],
        mode="lines+markers",
        line=dict(color="#087ed1", width=2),
        marker=dict(size=6, color="#087ed1"),
        text=[f"{v:.1f}% " for v in annual["rate"]],
        textposition="top center",
        textfont=dict(size=8, color="#087ed1"),
        yaxis="y2",
        hovertemplate="%{x}: %{y:.1f}% resuelto<extra></extra>",
    )
)
annual_fig.update_layout(
    height=205,
    margin=dict(l=25, r=22, t=16, b=24),
    barmode="group",
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(range=[0, max(annual["Cantidad_Denuncias"] / 1000) * 1.22], showticklabels=False, showgrid=False),
    yaxis2=dict(range=[0, max(30, annual["rate"].max() * 1.25)], overlaying="y", side="right", showticklabels=False, showgrid=False),
)
annual_fig.update_xaxes(tickfont=dict(size=9, color="#657790"), showgrid=False, zeroline=False)

# Modality bars
mod = (
    filtered.groupby("Modalidad", as_index=False)["Cantidad_Denuncias"].sum()
    .sort_values("Cantidad_Denuncias")
)
mod_total = mod["Cantidad_Denuncias"].sum()
mod["share"] = mod["Cantidad_Denuncias"] / mod_total * 100

modal_fig = go.Figure()
for i, row in mod.iterrows():
    modal_fig.add_trace(
        go.Bar(
            x=[row["Cantidad_Denuncias"] / 1_000_000],
            y=[row["Modalidad"]],
            orientation="h",
            marker=dict(color=("#ef3b43" if "Extorsión" in row["Modalidad"] else ("#d9e1f4" if row["Modalidad"] in ["Estafa", "Secuestro"] else "#4c75ad"))),
            text=f"{row['Cantidad_Denuncias']/1_000_000:.1f}M ({row['share']:.1f}%)",
            textposition="outside",
            textfont=dict(size=8, color="#52647a"),
            showlegend=False,
            width=0.42,
        )
    )
modal_fig.update_layout(
    height=205,
    margin=dict(l=92, r=36, t=8, b=18),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    bargap=0.12,
)
modal_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
modal_fig.update_yaxes(tickfont=dict(size=9, color="#52647a"), showgrid=False, zeroline=False)

# Top regions
regions = (
    filtered.groupby("Departamento", as_index=False)["Cantidad_Denuncias"].sum()
    .sort_values("Cantidad_Denuncias")
    .tail(6)
)
region_names = regions["Departamento"].replace(
    {
        "LIMA METROPOLITANA": "Lima Met.",
        "PROV. CONST. DEL CALLAO": "Callao",
    }
)

region_fig = go.Figure()
region_fig.add_trace(
    go.Bar(
        y=region_names,
        x=regions["Cantidad_Denuncias"] / 1_000_000,
        orientation="h",
        marker=dict(color=["#173b7a" if i == regions["Cantidad_Denuncias"].idxmax() else "#607ba3" for i in regions.index]),
        text=[f"{v/1_000_000:.1f} M" for v in regions["Cantidad_Denuncias"]],
        textposition="outside",
        textfont=dict(size=8, color="#52647a"),
        width=0.42,
    )
)
region_fig.update_layout(
    height=190,
    margin=dict(l=108, r=42, t=5, b=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
region_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
region_fig.update_yaxes(tickfont=dict(size=9, color="#52647a"), showgrid=False, zeroline=False)

# Hourly heatmap
heat = (
    filtered.groupby(["Modalidad", "Turno_Corto"], as_index=False)["Cantidad_Denuncias"].sum()
)
turn_order = ["Madrugada", "Mañana", "Tarde", "Noche"]
heat_modalities = ["Robo", "Violencia contra la mujer e integrantes", "Hurto", "Estafa", "Extorsión"]
heat_modalities = [m for m in heat_modalities if m in filtered["Modalidad"].unique()]
heat_pivot = heat.pivot(index="Modalidad", columns="Turno_Corto", values="Cantidad_Denuncias").fillna(0)
heat_pivot = heat_pivot.reindex(index=heat_modalities, columns=turn_order, fill_value=0)
row_share = heat_pivot.div(heat_pivot.sum(axis=1).replace(0, 1), axis=0) * 100

short_names = {
    "Violencia contra la mujer e integrantes": "Violencia F.",
    "Madrugada": "Madrugada",
}
heat_labels = [short_names.get(m, m) for m in heat_pivot.index]
heat_fig = go.Figure()
heat_fig.add_trace(go.Heatmap(
    z=row_share.values,
    x=["Madrugada\n(00–06h)", "Mañana\n(06–12h)", "Tarde\n(12–18h)", "Noche\n(18–24h)"],
    y=heat_labels,
    colorscale=[[0, "#bcd5ed"], [0.25, "#96bee4"], [0.50, "#6ba6d7"], [0.75, "#3f89c7"], [1, "#0c63ad"]],
    zmin=0,
    zmax=50,
    text=[[f"{v:.0f}%" for v in row] for row in row_share.values],
    texttemplate="%{text}",
    textfont=dict(size=9, color="#18375d"),
    hovertemplate="%{y} · %{x}: %{z:.1f}%<extra></extra>",
    showscale=False,
))
heat_fig.update_layout(height=190, margin=dict(l=90, r=10, t=6, b=25), paper_bgcolor="rgba(0,0,0,0)")
heat_fig.update_xaxes(side="bottom", tickfont=dict(size=8, color="#657790"), showgrid=False)
heat_fig.update_yaxes(tickfont=dict(size=8.5, color="#52647a"), showgrid=False, autorange="reversed")

# Layout
st.markdown('<div style="height:1px"></div>', unsafe_allow_html=True)
chart1, chart2 = st.columns([58, 42])
with chart1:
    st.markdown(
        '<div class="chart-card"><div class="chart-title">Evolución Anual de Denuncias y Adopción del Canal Digital (2018–2026*)</div>'
        '<div class="chart-subtitle">Barras: Miles de denuncias | Línea celeste: % Denuncia Digital</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(annual_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
with chart2:
    st.markdown(
        '<div class="chart-card"><div class="chart-title">Volumen y Tasa de Resolución por Modalidad</div>'
        '<div class="chart-subtitle">Acumulado 2018–2026 | Etiqueta derecha: % Casos Resueltos</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(modal_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

chart3, chart4 = st.columns([58, 42])
with chart3:
    st.markdown(
        '<div class="chart-card tight"><div class="chart-title">Top 6 Regiones por Volumen Acumulado (2018–2026)</div>'
        '<div class="chart-subtitle">Clic derecho en región para Drill-through a detalle distrital (1,840 distritos)</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(region_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
with chart4:
    st.markdown(
        '<div class="chart-card tight"><div class="chart-title">Patrón Horario por Modalidad Delictiva (% de denuncias)</div>'
        '<div class="chart-subtitle">Base para asignación de turnos de patrullaje localizado</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(heat_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="footer"><div>Fuente: Sistema de Denuncias Policiales (SIDPOL) 2018–2026 (Dataset Consolidado y Enriquecido: 378,187 registros) | *2026: Enero–Octubre.</div>'
    '<div>PÁGINA 1 · EXPLORATORIO</div></div>',
    unsafe_allow_html=True,
)
