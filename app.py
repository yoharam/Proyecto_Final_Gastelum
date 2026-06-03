import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Panel de Seguridad | HR/HAE Tlajomulco",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── LIGHT MODE (default) ── */
:root,
[data-theme="light"] {
    --guinda:   #6B1A2B;
    --guinda2:  #8B2236;
    --gold:     #B8860B;
    --gold2:    #D4A017;
    --cream:    #F5F0E8;
    --warm:     #EDE8DF;
    --text:     #1A1410;
    --muted:    #6B6460;
    --success:  #2D7A4F;
    --warning:  #C47F00;
    --danger:   #8B0000;
    --info:     #1A4A6B;

    --bg-page:      #F5F0E8;
    --bg-card:      #FFFFFF;
    --bg-card-hover: #FAF8F4;
    --border:       rgba(107,26,43,0.12);
    --shadow:       rgba(0,0,0,0.07);
    --shadow-hover:  rgba(0,0,0,0.13);
    --sidebar-bg1:  #1A0810;
    --sidebar-bg2:  #2D1020;
    --sidebar-text: #EDE8DF;
    --sidebar-label: #D4A017;
    --toggle-bg:    rgba(107,26,43,0.08);
    --toggle-border: rgba(107,26,43,0.2);
    --input-bg:     #FFFFFF;
}

/* ── DARK MODE ── */
[data-theme="dark"],
@media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
        --guinda:   #C4536A;
        --guinda2:  #D96B80;
        --gold:     #D4A017;
        --gold2:    #E8B82A;
        --cream:    #1A1210;
        --warm:     #221815;
        --text:     #F0EBE3;
        --muted:    #9B918A;
        --success:  #4CAF7D;
        --warning:  #E09820;
        --danger:   #E05060;
        --info:     #5B9BD5;

        --bg-page:      #130F0D;
        --bg-card:      #1E1714;
        --bg-card-hover: #251C18;
        --border:       rgba(196,83,106,0.15);
        --shadow:       rgba(0,0,0,0.35);
        --shadow-hover:  rgba(0,0,0,0.5);
        --sidebar-bg1:  #0D0A09;
        --sidebar-bg2:  #1A1210;
        --sidebar-text: #EDE8DF;
        --sidebar-label: #E8B82A;
        --toggle-bg:    rgba(196,83,106,0.1);
        --toggle-border: rgba(196,83,106,0.25);
        --input-bg:     #251C18;
    }
}

[data-theme="dark"] {
    --guinda:   #C4536A;
    --guinda2:  #D96B80;
    --gold:     #D4A017;
    --gold2:    #E8B82A;
    --cream:    #1A1210;
    --warm:     #221815;
    --text:     #F0EBE3;
    --muted:    #9B918A;
    --success:  #4CAF7D;
    --warning:  #E09820;
    --danger:   #E05060;
    --info:     #5B9BD5;

    --bg-page:      #130F0D;
    --bg-card:      #1E1714;
    --bg-card-hover: #251C18;
    --border:       rgba(196,83,106,0.15);
    --shadow:       rgba(0,0,0,0.35);
    --shadow-hover:  rgba(0,0,0,0.5);
    --sidebar-bg1:  #0D0A09;
    --sidebar-bg2:  #1A1210;
    --sidebar-text: #EDE8DF;
    --sidebar-label: #E8B82A;
    --toggle-bg:    rgba(196,83,106,0.1);
    --toggle-border: rgba(196,83,106,0.25);
    --input-bg:     #251C18;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-page) !important;
    color: var(--text) !important;
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* Stapp main background */
.stApp {
    background-color: var(--bg-page) !important;
}
.main .block-container {
    background-color: var(--bg-page) !important;
}



/* ── Header ── */
.main-header {
    background: linear-gradient(135deg, var(--guinda) 0%, var(--guinda2) 60%, #3D0A15 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(107,26,43,0.35);
}
[data-theme="dark"] .main-header {
    box-shadow: 0 8px 40px rgba(0,0,0,0.6);
}
.main-header::after {
    content: '';
    position: absolute;
    right: -40px; top: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(212,160,23,0.12);
}
.main-header h1 {
    font-family: 'Playfair Display', serif;
    color: white;
    font-size: 1.9rem;
    margin: 0;
    line-height: 1.2;
}
.main-header p { color: rgba(255,255,255,0.7); margin: 0.25rem 0 0; font-size: 0.85rem; }
.header-icon { font-size: 3rem; }

/* ── KPI Cards ── */
.kpi-card {
    background: var(--bg-card);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px var(--shadow);
    border-left: 5px solid var(--guinda);
    transition: box-shadow 0.2s, background 0.3s;
    height: 100%;
}
.kpi-card:hover { box-shadow: 0 6px 24px var(--shadow-hover); background: var(--bg-card-hover); }
.kpi-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 0.4rem; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 900; color: var(--guinda); line-height: 1; }
.kpi-sub { font-size: 0.78rem; color: var(--muted); margin-top: 0.35rem; }
.kpi-delta-up   { color: var(--danger); font-size: 0.78rem; }
.kpi-delta-down { color: var(--success); font-size: 0.78rem; }

.kpi-gold   { border-left-color: var(--gold); }
.kpi-gold .kpi-value { color: var(--gold); }
.kpi-green  { border-left-color: var(--success); }
.kpi-green .kpi-value { color: var(--success); }
.kpi-warn   { border-left-color: var(--warning); }
.kpi-warn .kpi-value { color: var(--warning); }

/* ── Section title ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    color: var(--guinda);
    font-weight: 700;
    border-bottom: 2px solid var(--gold2);
    padding-bottom: 0.4rem;
    margin: 1.5rem 0 1rem;
    display: inline-block;
}

/* ── Table ── */
.dataframe { font-size: 0.82rem !important; }

/* ── Streamlit native elements in dark mode ── */
[data-theme="dark"] .stDataFrame,
[data-theme="dark"] [data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
}
[data-theme="dark"] .stTextInput input,
[data-theme="dark"] .stSelectbox select,
[data-theme="dark"] [data-testid="stTextInput"] input {
    background: var(--input-bg) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}
[data-theme="dark"] [data-testid="metric-container"] {
    background: var(--bg-card) !important;
    color: var(--text) !important;
}
[data-theme="dark"] .stTabs [data-baseweb="tab"] {
    background: var(--bg-card) !important;
    color: var(--text) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--sidebar-bg1) 0%, var(--sidebar-bg2) 100%) !important;
    transition: background 0.3s;
}
[data-testid="stSidebar"] * { color: var(--sidebar-text) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiselect label,
[data-testid="stSidebar"] .stDateInput label {
    color: var(--sidebar-label) !important;
    font-size: 0.8rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em;
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-centinela { background: #FFF3CD; color: #856404; }
.badge-adverso   { background: #F8D7DA; color: #842029; }
.badge-cuasifalla{ background: #D1ECF1; color: #0C5460; }
.badge-enviado   { background: #D4EDDA; color: #155724; }
.badge-revision  { background: #FFF3CD; color: #856404; }
.badge-cerrado   { background: #E2E3E5; color: #383D41; }

[data-theme="dark"] .badge-centinela { background: #3D2E00; color: #F0C060; }
[data-theme="dark"] .badge-adverso   { background: #3D0F14; color: #F08090; }
[data-theme="dark"] .badge-cuasifalla{ background: #0A2030; color: #70C0D8; }
[data-theme="dark"] .badge-enviado   { background: #0D2A1A; color: #60C890; }
[data-theme="dark"] .badge-revision  { background: #3D2E00; color: #F0C060; }
[data-theme="dark"] .badge-cerrado   { background: #252525; color: #C0C0C0; }

/* ── Metric containers ── */
div[data-testid="metric-container"] {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 2px 8px var(--shadow);
    transition: background 0.3s;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: var(--bg-card);
    border-radius: 8px 8px 0 0;
    padding: 0.5rem 1.2rem;
    font-size: 0.83rem;
    font-weight: 600;
    color: var(--text);
    transition: background 0.2s, color 0.2s;
}
.stTabs [aria-selected="true"] {
    background: var(--guinda) !important;
    color: white !important;
}
</style>



<script>
(function() {
    // Force dark mode
    applyTheme('dark');
})();

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
}
</script>
""", unsafe_allow_html=True)

# ── Paletas Plotly ──────────────────────────────────────────────────────────────
GUINDA = "#6B1A2B"
GOLD   = "#B8860B"
GOLD2  = "#D4A017"
COLORS_TIPO  = {"Adverso": "#8B2236", "Centinela": "#B8860B", "Cuasifalla": "#1A4A6B"}
COLORS_ESTADO = {"Enviado": "#2D7A4F", "En Revisión": "#C47F00", "Cerrado": "#6B6460", "Centinela": "#6B1A2B"}

# ── Datos de ejemplo ─────────────────────────────────────────────────────────────
@st.cache_data
def generar_datos():
    random.seed(42)
    np.random.seed(42)

    areas = ["Urgencias", "UCI / Areas Criticas", "Hospitalización", "Quirófano",
             "Imagenología", "Medicina Interna", "Cocina", "Área Quirúrgica",
             "Auxiliares de Diagnóstico y Tratamiento"]
    subareas = {
        "Urgencias":        ["Triage", "Observación Adultos", "Observación Pediátrica", "Reanimación / Choque"],
        "UCI / Areas Criticas": ["UCIA", "UCIP"],
        "Hospitalización":  ["Medicina Interna", "Cirugía", "Aislados / Infecciosos"],
        "Quirófano":        ["Quirófano 1", "Quirófano 2", "CEYE"],
        "Imagenología":     ["Medicina Nuclear", "Radiología", "Ultrasonido"],
        "Medicina Interna": ["Cardiología", "Neumología"],
        "Cocina":           ["Cocina General"],
        "Área Quirúrgica":  ["Endoscopia Gastrointestinal", "Cirugía Ambulatoria"],
        "Auxiliares de Diagnóstico y Tratamiento": ["Laboratorio", "Banco de Sangre"],
    }
    incidentes = ["Caídas", "Medicación", "Tecnovigilancia", "Procedimientos Quirúrgicos o Médicos",
                  "Infección Nosocomial", "Identificación del Paciente", "Comunicación", "Otros"]
    tipos      = ["Adverso", "Centinela", "Cuasifalla"]
    estados    = ["Enviado", "En Revisión", "Cerrado", "Centinela"]
    nombres    = ["Zaid Gonzalez", "Martha Gonzalez", "Diego Noel Galarza Meza", "Alberto Rodriguez",
                  "Diego Gonzalez", "Ana Pérez López", "Carlos Reyes", "Maria Hernandez",
                  "Juan Torres", "Lucía Martínez", "Roberto García", "Patricia Sánchez"]
    reportadores = ["Dr. García", "Enf. López", "Dr. Martínez", "Enf. Reyes", "Dr. Sánchez",
                    "Enf. Torres", "Dr. Hernández", "Enf. Rodríguez"]

    rows = []
    start = datetime(2026, 1, 1)
    for i in range(1, 98):
        fecha = start + timedelta(days=random.randint(0, 88), hours=random.randint(0,23), minutes=random.randint(0,59))
        area  = random.choice(areas)
        sub   = random.choice(subareas[area])
        tipo  = random.choices(tipos, weights=[40, 35, 25])[0]
        estado= random.choices(estados, weights=[49, 12, 4, 35])[0] if tipo != "Centinela" else random.choices(["Centinela", "Cerrado"], weights=[70, 30])[0]
        gravedad = random.choices(["Leve", "Moderado", "Grave", "Catastrófico"], weights=[40, 35, 18, 7])[0]
        rows.append({
            "Código":       f"EVT-{fecha.strftime('%y%m')}-{i:04d}",
            "Paciente":     random.choice(nombres),
            "Fecha":        fecha,
            "Mes":          fecha.strftime("%B %Y"),
            "Tipo":         tipo,
            "Incidente":    random.choice(incidentes),
            "Área":         area,
            "Subárea":      sub,
            "Estado":       estado,
            "Gravedad":     gravedad,
            "Prevenible":   random.choice(["Sí", "No"]),
            "Reportador":   random.choice(reportadores),
            "Días_resol":   random.randint(0, 45) if estado == "Cerrado" else None,
        })

    df = pd.DataFrame(rows)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df

df_full = generar_datos()

# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 Filtros")
    st.markdown("---")

    fecha_min = df_full["Fecha"].min().date()
    fecha_max = df_full["Fecha"].max().date()
    rango = st.date_input("Rango de fechas", value=(fecha_min, fecha_max), min_value=fecha_min, max_value=fecha_max)

    areas_disp = ["Todas"] + sorted(df_full["Área"].unique().tolist())
    area_sel   = st.selectbox("Área", areas_disp)

    tipos_disp = st.multiselect("Tipo de evento", ["Adverso", "Centinela", "Cuasifalla"], default=["Adverso", "Centinela", "Cuasifalla"])
    estados_disp = st.multiselect("Estado", ["Enviado", "En Revisión", "Cerrado", "Centinela"], default=["Enviado", "En Revisión", "Cerrado", "Centinela"])

    st.markdown("---")
    st.markdown("<small style='color:#9B8B80'>ISSSTE — HR/HAE Tlajomulco<br>Panel de Seguridad del Paciente<br>v1.0 · 2026</small>", unsafe_allow_html=True)

# ── Filtrado ──────────────────────────────────────────────────────────────────────
if isinstance(rango, (list, tuple)) and len(rango) == 2:
    df = df_full[(df_full["Fecha"].dt.date >= rango[0]) & (df_full["Fecha"].dt.date <= rango[1])]
else:
    df = df_full.copy()

if area_sel != "Todas":
    df = df[df["Área"] == area_sel]
if tipos_disp:
    df = df[df["Tipo"].isin(tipos_disp)]
if estados_disp:
    df = df[df["Estado"].isin(estados_disp)]

# ── Header ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <div class="header-icon">🏥</div>
  <div>
    <h1>Panel de Seguridad del Paciente</h1>
    <p>ISSSTE — Hospital Regional de Alta Especialidad Tlajomulco de Zúñiga &nbsp;|&nbsp; {datetime.now().strftime('%d de %B de %Y')}</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────────
total      = len(df)
adversos   = len(df[df["Tipo"] == "Adverso"])
centinelas = len(df[df["Tipo"] == "Centinela"])
cuasifallas= len(df[df["Tipo"] == "Cuasifalla"])
enviados   = len(df[df["Estado"] == "Enviado"])
en_rev     = len(df[df["Estado"] == "En Revisión"])
cerrados   = len(df[df["Estado"] == "Cerrado"])
prevenibles= len(df[df["Prevenible"] == "Sí"])
tasa_cent  = round((centinelas / total * 100), 1) if total > 0 else 0
tasa_prev  = round((prevenibles / total * 100), 1) if total > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total Eventos</div>
        <div class="kpi-value">{total}</div>
        <div class="kpi-sub">en el período seleccionado</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card kpi-gold">
        <div class="kpi-label">Adversos</div>
        <div class="kpi-value">{adversos}</div>
        <div class="kpi-sub">{round(adversos/total*100,1) if total else 0}% del total</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-card" style="border-left-color:#1A4A6B">
        <div class="kpi-label">Cuasifallas</div>
        <div class="kpi-value" style="color:#1A4A6B">{cuasifallas}</div>
        <div class="kpi-sub">{round(cuasifallas/total*100,1) if total else 0}% del total</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Centinela</div>
        <div class="kpi-value">{centinelas}</div>
        <div class="kpi-sub">Tasa: {tasa_cent} / 100 eventos</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class="kpi-card kpi-warn">
        <div class="kpi-label">Prevenibles</div>
        <div class="kpi-value">{prevenibles}</div>
        <div class="kpi-sub">{tasa_prev}% del total</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resumen", "📈 Tendencias", "🗺️ Por Área", "📋 Registros", "⚙️ Calidad"])

# ═══════════════════════════════════════════════════
# TAB 1: RESUMEN
# ═══════════════════════════════════════════════════
with tab1:
    col_a, col_b, col_c = st.columns([1.1, 1, 1])

    # Donut tipo
    with col_a:
        st.markdown('<p class="section-title">Por Tipo de Evento</p>', unsafe_allow_html=True)
        tipo_counts = df["Tipo"].value_counts().reset_index()
        tipo_counts.columns = ["Tipo", "count"]
        fig_tipo = px.pie(tipo_counts, names="Tipo", values="count", hole=0.6,
                          color="Tipo", color_discrete_map=COLORS_TIPO)
        fig_tipo.update_traces(textposition="outside", textinfo="label+percent")
        fig_tipo.update_layout(
            showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=280,
            annotations=[dict(text=f"<b>{total}</b><br>eventos", x=0.5, y=0.5,
                              font_size=16, showarrow=False, font_color=GUINDA)],
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_tipo, use_container_width=True, config={"displayModeBar": False})

    # Donut estado
    with col_b:
        st.markdown('<p class="section-title">Estado de Eventos</p>', unsafe_allow_html=True)
        est_counts = df["Estado"].value_counts().reset_index()
        est_counts.columns = ["Estado", "count"]
        fig_est = px.pie(est_counts, names="Estado", values="count", hole=0.6,
                         color="Estado", color_discrete_map=COLORS_ESTADO)
        fig_est.update_traces(textposition="outside", textinfo="label+percent")
        fig_est.update_layout(
            showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=280,
            annotations=[dict(text=f"<b>{enviados}</b><br>enviados", x=0.5, y=0.5,
                               font_size=16, showarrow=False, font_color="#2D7A4F")],
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_est, use_container_width=True, config={"displayModeBar": False})

    # Top incidentes
    with col_c:
        st.markdown('<p class="section-title">Top Incidentes</p>', unsafe_allow_html=True)
        inc_counts = df["Incidente"].value_counts().head(6).reset_index()
        inc_counts.columns = ["Incidente", "count"]
        fig_inc = px.bar(inc_counts.sort_values("count"), x="count", y="Incidente",
                          orientation="h", color_discrete_sequence=[GUINDA])
        fig_inc.update_layout(
            xaxis_title="", yaxis_title="", height=280,
            margin=dict(t=5, b=5, l=5, r=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(tickfont=dict(size=11))
        )
        fig_inc.update_traces(marker_color=GUINDA, marker_line_width=0)
        st.plotly_chart(fig_inc, use_container_width=True, config={"displayModeBar": False})

    # Gravedad
    st.markdown('<p class="section-title">Distribución por Gravedad y Tipo</p>', unsafe_allow_html=True)
    grav_tipo = df.groupby(["Gravedad", "Tipo"]).size().reset_index(name="count")
    orden_grav = ["Leve", "Moderado", "Grave", "Catastrófico"]
    grav_tipo["Gravedad"] = pd.Categorical(grav_tipo["Gravedad"], categories=orden_grav, ordered=True)
    grav_tipo = grav_tipo.sort_values("Gravedad")
    fig_grav = px.bar(grav_tipo, x="Gravedad", y="count", color="Tipo",
                       color_discrete_map=COLORS_TIPO, barmode="group")
    fig_grav.update_layout(
        height=300, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="", yaxis_title="N° Eventos", legend_title="Tipo"
    )
    st.plotly_chart(fig_grav, use_container_width=True, config={"displayModeBar": False})

# ═══════════════════════════════════════════════════
# TAB 2: TENDENCIAS
# ═══════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">Eventos por Semana</p>', unsafe_allow_html=True)
    df_trend = df.copy()
    df_trend["Semana"] = df_trend["Fecha"].dt.to_period("W").apply(lambda r: r.start_time)
    weekly = df_trend.groupby(["Semana", "Tipo"]).size().reset_index(name="count")

    fig_line = px.line(weekly, x="Semana", y="count", color="Tipo",
                        color_discrete_map=COLORS_TIPO, markers=True, line_shape="spline")
    fig_line.update_traces(line_width=2.5, marker_size=7)
    fig_line.update_layout(
        height=340, margin=dict(t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="", yaxis_title="N° Eventos", legend_title="Tipo",
        hovermode="x unified"
    )
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<p class="section-title">Hora del Día (Distribución)</p>', unsafe_allow_html=True)
        df["Hora"] = df["Fecha"].dt.hour
        hora_counts = df.groupby(["Hora", "Tipo"]).size().reset_index(name="count")
        fig_hora = px.area(hora_counts, x="Hora", y="count", color="Tipo",
                            color_discrete_map=COLORS_TIPO)
        fig_hora.update_layout(
            height=280, margin=dict(t=5,b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickmode="linear", dtick=4, title="Hora"),
            yaxis_title="Eventos", legend_title="Tipo"
        )
        st.plotly_chart(fig_hora, use_container_width=True, config={"displayModeBar": False})

    with col_r:
        st.markdown('<p class="section-title">Día de la Semana</p>', unsafe_allow_html=True)
        dias_es = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}
        df["DiaSemana"] = df["Fecha"].dt.dayofweek.map(dias_es)
        orden_dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
        dia_counts = df.groupby("DiaSemana").size().reset_index(name="count")
        dia_counts["DiaSemana"] = pd.Categorical(dia_counts["DiaSemana"], categories=orden_dias, ordered=True)
        dia_counts = dia_counts.sort_values("DiaSemana")
        fig_dia = px.bar(dia_counts, x="DiaSemana", y="count", color_discrete_sequence=[GOLD])
        fig_dia.update_layout(
            height=280, margin=dict(t=5,b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="", yaxis_title="Eventos"
        )
        st.plotly_chart(fig_dia, use_container_width=True, config={"displayModeBar": False})

    # Heatmap
    st.markdown('<p class="section-title">Mapa de Calor — Día × Hora</p>', unsafe_allow_html=True)
    df["DiaSemana_n"] = df["Fecha"].dt.dayofweek
    heat = df.groupby(["DiaSemana_n", "Hora"]).size().reset_index(name="count")
    heat_pivot = heat.pivot(index="DiaSemana_n", columns="Hora", values="count").fillna(0)
    heat_pivot.index = [orden_dias[i] for i in heat_pivot.index]
    fig_heat = px.imshow(heat_pivot, color_continuous_scale=["#FFF5F5","#8B2236"],
                          labels=dict(x="Hora", y="Día", color="Eventos"),
                          aspect="auto")
    fig_heat.update_layout(
        height=280, margin=dict(t=5,b=5),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

# ═══════════════════════════════════════════════════
# TAB 3: POR ÁREA
# ═══════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">Eventos por Área Hospitalaria</p>', unsafe_allow_html=True)

    col_m, col_n = st.columns([1.4, 1])
    with col_m:
        area_tipo = df.groupby(["Área", "Tipo"]).size().reset_index(name="count")
        area_total = area_tipo.groupby("Área")["count"].sum().sort_values(ascending=True)
        area_tipo["Área"] = pd.Categorical(area_tipo["Área"], categories=area_total.index, ordered=True)
        fig_area = px.bar(area_tipo.sort_values("Área"), x="count", y="Área", color="Tipo",
                           orientation="h", color_discrete_map=COLORS_TIPO, barmode="stack")
        fig_area.update_layout(
            height=380, margin=dict(t=5,b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="N° Eventos", yaxis_title="", legend_title="Tipo"
        )
        st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False})

    with col_n:
        st.markdown("**Riesgo por Área**")
        area_stats = df.groupby("Área").agg(
            total=("Tipo","count"),
            centinelas=("Tipo", lambda x: (x=="Centinela").sum()),
            graves=("Gravedad", lambda x: x.isin(["Grave","Catastrófico"]).sum())
        ).reset_index()
        area_stats["score"] = (area_stats["centinelas"]*3 + area_stats["graves"]*2 + area_stats["total"]).round(1)
        area_stats = area_stats.sort_values("score", ascending=False).head(8)

        fig_risk = px.scatter(area_stats, x="total", y="centinelas", size="graves",
                               color="score", text="Área",
                               color_continuous_scale=["#FFF5EE","#8B2236"],
                               size_max=35)
        fig_risk.update_traces(textposition="top center", textfont_size=9)
        fig_risk.update_layout(
            height=380, margin=dict(t=5,b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Total eventos", yaxis_title="Eventos centinela",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_risk, use_container_width=True, config={"displayModeBar": False})

    # Subáreas
    st.markdown('<p class="section-title">Top Subáreas con Mayor Incidencia</p>', unsafe_allow_html=True)
    sub_counts = df.groupby(["Área","Subárea"]).size().reset_index(name="count").sort_values("count", ascending=False).head(15)
    fig_sub = px.treemap(sub_counts, path=["Área","Subárea"], values="count",
                          color="count", color_continuous_scale=["#FFF5EE","#6B1A2B"])
    fig_sub.update_layout(height=360, margin=dict(t=5,b=5), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_sub, use_container_width=True, config={"displayModeBar": False})

# ═══════════════════════════════════════════════════
# TAB 4: REGISTROS
# ═══════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">Listado de Eventos</p>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        buscar = st.text_input("🔍 Buscar por código, paciente...", "")
    with col_f2:
        inc_filtro = st.selectbox("Incidente", ["Todos"] + sorted(df["Incidente"].unique().tolist()))
    with col_f3:
        grav_filtro = st.selectbox("Gravedad", ["Todas","Leve","Moderado","Grave","Catastrófico"])

    df_tabla = df.copy()
    if buscar:
        df_tabla = df_tabla[df_tabla.apply(lambda r: buscar.lower() in str(r).lower(), axis=1)]
    if inc_filtro != "Todos":
        df_tabla = df_tabla[df_tabla["Incidente"] == inc_filtro]
    if grav_filtro != "Todas":
        df_tabla = df_tabla[df_tabla["Gravedad"] == grav_filtro]

    df_show = df_tabla[["Código","Paciente","Fecha","Tipo","Incidente","Área","Subárea","Estado","Gravedad","Prevenible"]].copy()
    df_show["Fecha"] = df_show["Fecha"].dt.strftime("%d/%m/%Y %H:%M")
    df_show = df_show.sort_values("Código", ascending=False).reset_index(drop=True)

    st.dataframe(
        df_show,
        use_container_width=True,
        height=420,
        column_config={
            "Código":    st.column_config.TextColumn("Código", width=140),
            "Tipo":      st.column_config.TextColumn("Tipo", width=100),
            "Estado":    st.column_config.TextColumn("Estado", width=100),
            "Gravedad":  st.column_config.TextColumn("Gravedad", width=100),
            "Prevenible":st.column_config.TextColumn("¿Prevenible?", width=90),
        }
    )

    st.caption(f"Mostrando {len(df_show)} de {total} registros")

    # Descarga
    csv = df_show.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar CSV", data=csv, file_name="eventos_seguridad.csv", mime="text/csv")

# ═══════════════════════════════════════════════════
# TAB 5: CALIDAD
# ═══════════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-title">Indicadores de Calidad y Gestión</p>', unsafe_allow_html=True)

    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    cerrados_df = df[df["Estado"] == "Cerrado"]
    tiempo_prom = cerrados_df["Días_resol"].mean() if len(cerrados_df) > 0 else 0
    tasa_cierre = round(len(cerrados_df)/total*100, 1) if total > 0 else 0
    col_q1.metric("⏱ Tiempo prom. resolución", f"{tiempo_prom:.1f} días")
    col_q2.metric("✅ Tasa de cierre", f"{tasa_cierre}%")
    col_q3.metric("🔴 Graves + Catastróficos", len(df[df["Gravedad"].isin(["Grave","Catastrófico"])]))
    col_q4.metric("⚠️ En revisión pendientes", en_rev)

    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown("**Prevenibilidad por Tipo**")
        prev_tipo = df.groupby(["Tipo","Prevenible"]).size().reset_index(name="count")
        fig_prev = px.bar(prev_tipo, x="Tipo", y="count", color="Prevenible",
                           barmode="group",
                           color_discrete_map={"Sí":"#C47F00","No":"#D4D4D4"})
        fig_prev.update_layout(
            height=280, margin=dict(t=5,b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="", yaxis_title="Eventos", legend_title="Prevenible"
        )
        st.plotly_chart(fig_prev, use_container_width=True, config={"displayModeBar": False})

    with col_r2:
        st.markdown("**Eventos por Reportador**")
        rep_counts = df["Reportador"].value_counts().reset_index()
        rep_counts.columns = ["Reportador","count"]
        fig_rep = px.bar(rep_counts, x="count", y="Reportador", orientation="h",
                          color_discrete_sequence=[GUINDA])
        fig_rep.update_layout(
            height=280, margin=dict(t=5,b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Eventos", yaxis_title=""
        )
        st.plotly_chart(fig_rep, use_container_width=True, config={"displayModeBar": False})

    # Semáforo de riesgo
    st.markdown('<p class="section-title">Semáforo de Riesgo por Área</p>', unsafe_allow_html=True)
    risk_df = df.groupby("Área").agg(
        total=("Tipo","count"),
        centinelas=("Tipo", lambda x: (x=="Centinela").sum()),
        graves=("Gravedad", lambda x: x.isin(["Grave","Catastrófico"]).sum()),
        prevenibles=("Prevenible", lambda x: (x=="Sí").sum()),
    ).reset_index()
    risk_df["score"] = risk_df["centinelas"]*3 + risk_df["graves"]*2 + risk_df["prevenibles"]
    maxs = risk_df["score"].max()
    def semaforo(s, mx):
        if mx == 0: return "🟢 Bajo"
        p = s / mx
        if p >= 0.66: return "🔴 Alto"
        if p >= 0.33: return "🟡 Medio"
        return "🟢 Bajo"
    risk_df["Riesgo"] = risk_df["score"].apply(lambda s: semaforo(s, maxs))
    risk_df = risk_df.rename(columns={"total":"Eventos","centinelas":"Centinelas","graves":"Graves","prevenibles":"Prevenibles"})
    st.dataframe(risk_df[["Área","Eventos","Centinelas","Graves","Prevenibles","Riesgo"]].sort_values("Riesgo", ascending=False).reset_index(drop=True),
                  use_container_width=True, hide_index=True)