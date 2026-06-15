# Dashboard de Exoplanetas con Streamlit - Moira
# Tiene tres vistas segun a quien se le muestre: Ejecutiva, Tecnica y Operativa.
# Lee los datos desde mi API (FastAPI).

import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")

COLORES = {"Rocoso": "#8d6e63", "Neptuniano": "#42a5f5", "Gigante Gaseoso": "#ef6c00", "Desconocido": "#9e9e9e"}

st.set_page_config(page_title="Exoplanetas", page_icon="planet", layout="wide")


@st.cache_data(ttl=300)
def traer_estadisticas():
    r = requests.get(f"{API}/estadisticas", timeout=10)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def traer_planetas(tipo=None, pagina=1, tam=500):
    params = {"pagina": pagina, "tam_pagina": tam}
    if tipo:
        params["tipo"] = tipo
    r = requests.get(f"{API}/planetas", params=params, timeout=15)
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=300)
def traer_todos():
    # Trae todos los planetas recorriendo las paginas, para los graficos.
    filas, pagina = [], 1
    while True:
        datos = traer_planetas(pagina=pagina)
        filas += datos["planetas"]
        if pagina * datos["tam_pagina"] >= datos["total"]:
            break
        pagina += 1
    return pd.DataFrame(filas)


def hay_api():
    try:
        requests.get(f"{API}/salud", timeout=5).raise_for_status()
        return True
    except Exception:
        st.error(f"No me puedo conectar con la API en {API}. Revisa que este levantada.")
        return False


def vista_ejecutiva():
    st.header("Vista Ejecutiva")
    st.caption("Resumen general del catalogo de exoplanetas.")
    e = traer_estadisticas()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Planetas", f"{e['total_planetas']:,}")
    c2.metric("Masa media (M Jupiter)", e["masa_promedio"])
    c3.metric("Radio medio (R Jupiter)", e["radio_promedio"])
    c4.metric("Periodo medio (dias)", e["periodo_promedio"])

    tipos = pd.DataFrame(e["por_tipo"])
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(tipos, names="planet_type", values="cantidad", hole=0.45,
                     color="planet_type", color_discrete_map=COLORES,
                     title="Planetas por tipo")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(tipos, x="planet_type", y="cantidad", color="planet_type",
                     color_discrete_map=COLORES, title="Cantidad por clasificacion")
        st.plotly_chart(fig, use_container_width=True)

    top = tipos.sort_values("cantidad", ascending=False).iloc[0]
    st.success(f"El tipo mas comun es **{top['planet_type']}** con {top['cantidad']:,} planetas.")


def vista_tecnica():
    st.header("Vista Tecnica")
    st.caption("Graficos de masa, radio y resultados de los modelos de la Evaluacion 2.")
    df = traer_todos()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(df, x="masa_jup", y="radio_jup", color="planet_type",
                         color_discrete_map=COLORES, opacity=0.6,
                         title="Masa vs radio por tipo")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="radio_jup", color="planet_type", nbins=40,
                           color_discrete_map=COLORES, title="Distribucion del radio")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Modelos de la Evaluacion 2")
    modelos = pd.DataFrame({
        "Modelo": ["Arbol de Decision", "Regresion Logistica", "Random Forest"],
        "Accuracy": [0.941, 0.931, 0.951],
        "ROC-AUC": [0.80, 0.96, 0.994],
    })
    st.dataframe(modelos, use_container_width=True, hide_index=True)


def vista_operativa():
    st.header("Vista Operativa")
    st.caption("Para buscar y revisar planetas uno por uno.")
    e = traer_estadisticas()
    tipos = [t["planet_type"] for t in e["por_tipo"]]

    col1, col2 = st.columns([1, 2])
    with col1:
        tipo_sel = st.selectbox("Tipo de planeta", ["(Todos)"] + tipos)
    with col2:
        buscar = st.text_input("Buscar por nombre", "")

    tipo = None if tipo_sel == "(Todos)" else tipo_sel
    df = traer_todos() if tipo is None else pd.DataFrame(traer_planetas(tipo=tipo)["planetas"])
    if buscar:
        df = df[df["nombre"].str.contains(buscar, case=False, na=False)]

    st.write(f"{len(df):,} planetas encontrados.")
    st.dataframe(
        df[["nombre", "planet_type", "estrella", "masa_jup", "radio_jup",
            "periodo_orbital_dias", "metodo_descubrimiento", "distancia_pc"]],
        use_container_width=True, hide_index=True,
    )

    if not df.empty:
        sel = st.selectbox("Ver detalle de un planeta", df["nombre"].tolist())
        if sel:
            r = requests.get(f"{API}/planetas/{sel}", timeout=10)
            if r.ok:
                st.json(r.json())


st.title("Catalogo de Exoplanetas")
if hay_api():
    vista = st.sidebar.radio("Vista", ["Ejecutiva", "Tecnica", "Operativa"])
    st.sidebar.caption(f"API: {API}")
    {"Ejecutiva": vista_ejecutiva, "Tecnica": vista_tecnica, "Operativa": vista_operativa}[vista]()
