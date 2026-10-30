import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# -------------------------------------------------------------
# CONFIGURACIÓN Y AUTENTICACIÓN
# -------------------------------------------------------------
st.set_page_config(page_title="UN ESTUDIO — AI Multi-Agent Hub", page_icon="🤖", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Acceso al Hub — UN ESTUDIO")
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Ingresar"):
            if username == "admin" and password == "unestudio2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.stop()

# -------------------------------------------------------------
# BARRA LATERAL (SELECTOR DE AGENTES)
# -------------------------------------------------------------
st.sidebar.title("🎛️ Panel Multi-Agente")
modulo = st.sidebar.radio(
    "Selecciona la Herramienta de IA:",
    [
        "🚀 Agente 1: Prospección B2B",
        "✍️ Agente 2: Guiones y Pitches",
        "💰 Agente 3: Cotizador Inteligente",
        "📊 Pilar 8: Dashboard & Métricas ROI"
    ]
)

gemini_key = st.sidebar.text_input("Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
serper_key = st.sidebar.text_input("Serper API Key", value=os.getenv("SERPER_API_KEY", ""), type="password")

# -------------------------------------------------------------
# AGENTE 1: PROSPECCIÓN B2B
# -------------------------------------------------------------
if modulo == "🚀 Agente 1: Prospección B2B":
    st.title("🚀 Agente de Prospección Comercial")
    tipo = st.selectbox("Tipo de Prospecto:", ["Salones de Eventos", "Wedding Planners", "Corporativos"])
    if st.button("Iniciar Prospección"):
        # Lógica del Agente con CrewAI + Serper (Código actual)
        st.info(f"Ejecutando agente para buscar {tipo}...")

# -------------------------------------------------------------
# AGENTE 2: GUIONES & PITCHES
# -------------------------------------------------------------
elif modulo == "✍️ Agente 2: Guiones y Pitches":
    st.title("✍️ Agente Redactor de Guiones & Pitches")
    servicio = st.selectbox("Servicio a promocionar:", ["Video Institucional", "Cobertura de Boda", "Podcast"])
    tono = st.select_slider("Tono del contenido:", options=["Corporativo", "Emotivo", "Viral / Dinámico"])
    
    if st.button("Generar Guion con IA"):
        if not gemini_key:
            st.error("Ingresa tu Gemini API Key")
        else:
            llm = LLM(model="gemini/gemini-1.5-flash", api_key=gemini_key)
            agente_guionista = Agent(
                role="Director Creativo y Guionista B2B",
                goal=f"Escribir un guion de video corto (Reel/TikTok) de 30s enfocando el servicio de {servicio} de UN ESTUDIO en tono {tono}.",
                backstory="Eres un reconocido director creativo de comerciales audiovisuales.",
                llm=llm
            )
            tarea_guion = Task(
                description=f"Redacta una parrilla escena por escena (Video, Audio, Texto en Pantalla) para un video de {servicio}.",
                expected_output="Estructura detallada escena por escena del video.",
                agent=agente_guionista
            )
            crew = Crew(agents=[agente_guionista], tasks=[tarea_guion])
            res = crew.kickoff()
            st.success("¡Guion Generado!")
            st.write(res)

# -------------------------------------------------------------
# AGENTE 3: COTIZADOR INTELIGENTE
# -------------------------------------------------------------
elif modulo == "💰 Agente 3: Cotizador Inteligente":
    st.title("💰 Cotizador Automático de Servicios")
    col1, col2 = st.columns(2)
    with col1:
        horas_cobertura = st.number_input("Horas de Evento / Grabación:", min_value=1, value=4)
        num_camaras = st.slider("Cantidad de Cámaras:", 1, 4, 2)
    with col2:
        incluye_dron = st.checkbox("¿Incluye Tomas Aéreas con Dron?")
        entrega_express = st.checkbox("¿Entrega Express (48 hrs)?")
    
    costo_base = (horas_cobertura * 1500) + (num_camaras * 2000)
    if incluye_dron: costo_base += 3500
    if entrega_express: costo_base *= 1.25
    
    st.markdown(f"### **Total Estimado: ${costo_base:,.2f} MXN**")

# -------------------------------------------------------------
# PILAR 8: DASHBOARD & MÉTRICAS ROI
# -------------------------------------------------------------
elif modulo == "📊 Pilar 8: Dashboard & Métricas ROI":
    st.title("📊 Panel BI — Métricas y Rendimiento Operativo")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Leads Prospectados", "128", "+12% este mes")
    kpi2.metric("Cotizaciones Generadas", "$245,000 MXN", "+8%")
    kpi3.metric("Tiempo Ahorrado con IA", "34 Horas", "Semanales")
    
    # Gráfica de ejemplo de conversión
    data = pd.DataFrame({"Semana": ["Sem 1", "Sem 2", "Sem 3", "Sem 4"], "Leads": [20, 35, 40, 33]})
    st.bar_chart(data.set_index("Semana"))