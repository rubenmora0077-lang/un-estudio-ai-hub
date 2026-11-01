import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# Configuración inicial de la página
st.set_page_config(page_title="UN ESTUDIO - Panel Multi-Agente", layout="wide", page_icon="🎬")

st.title("🎬 UN ESTUDIO - Panel Multi-Agente AI")

# --- BARRA LATERAL: API KEYS ---
st.sidebar.header("⚙️ Configuración de API Keys")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password", help="Obtenla en Google AI Studio")
serper_key = st.sidebar.text_input("Serper API Key", type="password", help="Obtenla en serper.dev (opcional para el Agente 2)")

# Asignar llaves al entorno de sistema de forma inmediata si fueron ingresadas
if gemini_key:
    os.environ["GEMINI_API_KEY"] = gemini_key
if serper_key:
    os.environ["SERPER_API_KEY"] = serper_key

# --- SELECCIÓN DE HERRAMIENTA ---
opcion = st.sidebar.radio(
    "Selecciona la Herramienta de IA:",
    [
        "🚀 Agente 1: Prospección B2B",
        "✍️ Agente 2: Guiones y Pitches",
        "💰 Agente 3: Cotizador Inteligente",
        "📊 Pilar 8: Dashboard & Métricas ROI"
    ]
)

# Inicializar modelo de LLM para CrewAI (si hay Gemini Key)
llm = None
if gemini_key:
    llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=gemini_key
    )

# --- VISTA 1: PROSPECCIÓN B2B ---
if opcion == "🚀 Agente 1: Prospección B2B":
    st.header("🚀 Agente de Prospección Comercial")
    tipo_prospecto = st.text_input("Tipo de Prospecto:", "Salones de Eventos")
    
    if st.button("Iniciar Prospección"):
        if not gemini_key or not serper_key:
            st.error("Por favor ingresa tanto la Gemini API Key como la Serper API Key en la barra lateral.")
        else:
            with st.spinner(f"Ejecutando agente para buscar {tipo_prospecto}..."):
                try:
                    search_tool = SerperDevTool()
                    
                    prospector = Agent(
                        role="Investigador de Mercado B2B",
                        goal=f"Encontrar los mejores prospectos para {tipo_prospecto} en el mercado actual.",
                        backstory="Eres un especialista en prospección comercial para agencias audiovisuales y creativas.",
                        tools=[search_tool],
                        llm=llm,
                        verbose=True
                    )
                    
                    task1 = Task(
                        description=f"Investiga 3 prospectos clave para {tipo_prospecto}. Entrega nombre, sitio web/redes y por qué necesitan servicios visuales.",
                        expected_output="Lista estructurada de 3 prospectos con detalles de contacto y recomendación visual.",
                        agent=prospector
                    )
                    
                    crew = Crew(agents=[prospector], tasks=[task1], process=Process.sequential)
                    resultado = crew.kickoff()
                    st.success("Prospección completada:")
                    st.markdown(resultado.raw)
                except Exception as e:
                    st.error(f"Error al ejecutar la prospección: {str(e)}")

# --- VISTA 2: GUIONES Y PITCHES ---
elif opcion == "✍️ Agente 2: Guiones y Pitches":
    st.header("✍️ Agente Redactor de Guiones & Pitches")
    servicio = st.selectbox("Servicio a promocionar:", ["Video Institucional", "Fotografía Comercial", "Podcast / Entrevistas", "Cobertura de Eventos"])
    tono = st.select_slider("Tono del contenido:", options=["Corporativo", "Creativo", "Directo a Ventas"])
    
    if st.button("Generar Guion con IA"):
        if not gemini_key:
            st.error("Por favor ingresa tu Gemini API Key en la barra lateral.")
        else:
            with st.spinner("Generando guion comercial..."):
                try:
                    writer = Agent(
                        role="Copywriter Audiovisual Senior",
                        goal=f"Crear guiones persuasivos para vender servicios de {servicio}.",
                        backstory="Experto en redacción creativa y propuestas comerciales para UN ESTUDIO.",
                        llm=llm,
                        verbose=True
                    )
                    
                    task2 = Task(
                        description=f"Escribe una propuesta corta y un guion de video de 30 segundos promocionando el servicio de {servicio} con un tono {tono}.",
                        expected_output="Guion estructurado con propuesta visual y locución.",
                        agent=writer
                    )
                    
                    crew = Crew(agents=[writer], tasks=[task2], process=Process.sequential)
                    resultado = crew.kickoff()
                    st.success("Guion generado:")
                    st.markdown(resultado.raw)
                except Exception as e:
                    st.error(f"Error al generar el guion: {str(e)}")

# --- VISTA 3: COTIZADOR ---
elif opcion == "💰 Agente 3: Cotizador Inteligente":
    st.header("💰 Cotizador Inteligente")
    st.info("Módulo en desarrollo para estimación automática de paquetes audiovisuales.")

# --- VISTA 4: DASHBOARD ---
elif opcion == "📊 Pilar 8: Dashboard & Métricas ROI":
    st.header("📊 Dashboard & Métricas ROI")
    st.info("Panel métrico para seguimiento de campañas y conversión de clientes.")
