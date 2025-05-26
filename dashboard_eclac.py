# Dashboard de riesgo comunal ECLAC usando Streamlit (versión profesional)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Configuración de página y estilo general
st.set_page_config(page_title="Dashboard Riesgo Comunal - ECLAC", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .block-container { padding: 2rem 2rem; }
        h1 { color: #003366; }
        .stMetric { font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

# Logo y título
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://www.cepal.org/sites/all/themes/cepal/logo.png", width=100)
with col_title:
    st.title("Dashboard de riesgo comunal del personal ECLAC")
    st.markdown("Visualización de la distribución del personal según el nivel de riesgo delictual en la Región Metropolitana")

# Cargar los datos
resumen = pd.read_excel("ECLAC_Riesgo_Comunal.xlsx")

# Filtros laterales
st.sidebar.header("🔎 Filtrar datos")
comunas_seleccionadas = st.sidebar.multiselect(
    "📍 Comunas:",
    options=resumen["Comuna"].unique(),
    default=resumen["Comuna"].unique()
)
niveles_seleccionados = st.sidebar.multiselect(
    "⚠️ Niveles de riesgo:",
    options=resumen["Nivel_Riesgo"].unique(),
    default=resumen["Nivel_Riesgo"].unique()
)

# Filtrar el dataframe
filtro = resumen[
    (resumen["Comuna"].isin(comunas_seleccionadas)) &
    (resumen["Nivel_Riesgo"].isin(niveles_seleccionados))
]

# Métricas generales
st.markdown("## 📊 Indicadores generales")
col1, col2, col3 = st.columns(3)
col1.metric("🗺️ Total de comunas", len(filtro["Comuna"].unique()))
col2.metric("👥 Total de personas", int(filtro["Cantidad_Personas"].sum()))
col3.metric("🚨 Promedio robos 2025", f"{filtro['Robos_2025'].mean():.1f}")

# Gráfico de barras
st.markdown("## 📈 Personas por nivel de riesgo")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=filtro,
    x="Nivel_Riesgo",
    y="Cantidad_Personas",
    estimator=sum,
    ci=None,
    palette="Set2",
    order=["Alto", "Medio", "Bajo", "Disminución"]
)
plt.title("Cantidad de personas por nivel de riesgo")
plt.ylabel("Cantidad de personas")
plt.xlabel("Nivel de riesgo")
st.pyplot(fig)

# Tabla detallada
st.markdown("## 🧾 Detalle por comuna")
st.dataframe(filtro.sort_values(by="Cantidad_Personas", ascending=False), use_container_width=True)

# Pie de página
st.markdown("""
    <hr style='margin-top:2rem; margin-bottom:1rem;'>
    <center><small>Fuente: ECLAC - Elaboración propia con datos de seguridad comunal 2024–2025</small></center>
""", unsafe_allow_html=True)
