import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="ViajeroAI Pro", page_icon="✈️", layout="wide")

st.title("🌍 ViajeroAI Pro: Itinerarios y Cotizaciones")
st.markdown("""
Planea tu viaje con fechas exactas. La IA buscará referencias de precios de vuelos y hoteles 
en la web para darte un estimado realista sin necesidad de agencias.
""")

# --- BARRA LATERAL: CONFIGURACIÓN ---
with st.sidebar:
    st.header("⚙️ Motor de IA")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    
    st.header("📅 Datos del Viaje")
    origen = st.text_input("Ciudad de Origen", "Ciudad de México")
    destino = st.text_input("Ciudad de Destino", "Madrid, España")
    
    # Selector de Fechas (Rango)
    hoy = datetime.date.today()
    fechas = st.date_input(
        "Selecciona fecha de ida y vuelta",
        (hoy + datetime.timedelta(days=30), hoy + datetime.timedelta(days=37)),
        format="DD/MM/YYYY"
    )
    
    st.divider()
    
    st.header("🎨 Preferencias")
    presupuesto = st.selectbox("Presupuesto", ["Económico (Mochilero)", "Moderado (Estándar)", "Alto (Lujo)"])
    intereses = st.multiselect("Intereses", ["Gastronomía", "Historia", "Naturaleza", "Compras", "Arte"], ["Gastronomía", "Historia"])
    pasajeros = st.number_input("Número de Pasajeros", 1, 10, 2)

# --- LÓGICA DEL AGENTE ---

def generar_plan_completo():
    if not openai_api_key:
        st.warning("⚠️ Necesitas colocar tu API Key de OpenAI en la barra lateral.")
        return

    # Validación de fechas
    if len(fechas) != 2:
        st.error("Por favor selecciona una fecha de inicio Y una de fin en el calendario.")
        return
    
    fecha_inicio, fecha_fin = fechas
    delta = fecha_fin - fecha_inicio
    dias_duracion = delta.days
    
    if dias_duracion < 1:
        st.error("La fecha de fin debe ser posterior a la de inicio.")
        return

    # 1. Búsqueda Web Inteligente (Sin API Keys extra, usa DuckDuckGo anónimo)
    search = DuckDuckGoSearchRun()
    
    def buscar_datos_reales():
        # Consultas específicas para "engañar" al buscador y sacar precios
        q_vuelos = f"precio vuelos baratos {origen} a {destino} fechas {fecha_inicio} a {fecha_fin}"
        q_hoteles = f"mejores hoteles {presupuesto} en {destino} precios {fecha_inicio} a {fecha_fin}"
        q_clima = f"clima en {destino} en {fecha_inicio.strftime('%B')}"
        
        try:
            raw_vuelos = search.run(q_vuelos)
            raw_hoteles = search.run(q_hoteles)
            raw_clima = search.run(q_clima)
            
            return f"""
            - INFO VUELOS ENCONTRADA: {raw_vuelos}
            - INFO HOTELES ENCONTRADA: {raw_hoteles}
            - CLIMA PRONOSTICADO: {raw_clima}
            """
        except Exception as e:
            return f"Error buscando datos en vivo: {e}"

    # 2. Prompt Engineering (Enfocado en Cotización y Logística)
    template = """
    Eres un experto planificador de viajes y agente de presupuestos.
    
    SOLICITUD DEL USUARIO:
    - Origen: {origen} -> Destino: {destino}
    - Fechas: {f_inicio} al {f_fin} ({dias} días)
    - Pasajeros: {pasajeros}
    - Presupuesto: {presupuesto}
    - Intereses: {intereses}
    
    INFORMACIÓN RECUPERADA DE LA WEB (Úsala para estimar precios reales):
    {contexto_web}
    
    TAREA:
    Genera un informe de viaje completo en formato Markdown.
    
    SECCIÓN 1: COTIZACIÓN ESTIMADA (Para {pasajeros} personas)
    - Analiza la "INFO VUELOS" y da un rango de precio estimado por persona y total. Menciona aerolíneas si aparecen.
    - Analiza la "INFO HOTELES" y sugiere 2 opciones de alojamiento concretas con precio aproximado por noche.
    - Calcula un estimado de comida y actividades según el nivel de presupuesto.
    - **Total Estimado del Viaje:** (Suma todo).
    
    SECCIÓN 2: ITINERARIO ({dias} días)
    - Crea un plan día a día optimizado lógicamente por ubicación.
    - Incluye actividades basadas en intereses: {intereses}.
    - Considera el clima: {contexto_web}
    
    IMPORTANTE: Si no encuentras precios exactos en la búsqueda, haz una estimación educada basada en tu conocimiento del mercado para esas fechas y aclara que es "estimado".
    """
    
    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, openai_api_key=openai_api_key)
    
    # 3. Ejecución
    with st.spinner(f"🔎 Buscando vuelos desde {origen} y hoteles en {destino}..."):
        contexto = buscar_datos_reales()
    
    with st.spinner("💡 Armando cotización e itinerario..."):
        chain = prompt | llm | StrOutputParser()
        respuesta = chain.invoke({
            "origen": origen,
            "destino": destino,
            "f_inicio": fecha_inicio,
            "f_fin": fecha_fin,
            "dias": dias_duracion,
            "pasajeros": pasajeros,
            "presupuesto": presupuesto,
            "intereses": ", ".join(intereses),
            "contexto_web": contexto
        })
        
        return respuesta, contexto

# --- UI PRINCIPAL ---

if st.button("Generar Plan de Viaje"):
    plan, datos_usados = generar_plan_completo()
    
    if plan:
        tab1, tab2 = st.tabs(["✈️ Tu Plan de Viaje", "🔍 Datos Encontrados"])
        
        with tab1:
            st.markdown(plan)
            st.warning("Nota: Los precios son estimaciones basadas en búsquedas web recientes. Verifica en las aerolíneas/hoteles directamente.")
            
        with tab2:
            st.text("Esta es la información cruda que la IA encontró en internet para armar tu plan:")
            st.code(datos_usados)