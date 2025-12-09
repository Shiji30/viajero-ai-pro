# viajero-ai-pro
# ✈️ ViajeroAI Pro: Planificador de Viajes con Cotizaciones en Tiempo Real

## 🌍 Descripción General del Proyecto

**ViajeroAI Pro** es una solución avanzada de planificación de viajes que genera itinerarios personalizados y cotizaciones estimadas de vuelos y alojamiento. Aprovecha el poder de los Grandes Modelos de Lenguaje (LLMs) y técnicas de Generación Aumentada por Recuperación (RAG) para ofrecer planes de viaje realistas y actualizados.

Este proyecto fue desarrollado como parte de un desafío de implementación de LLMs, centrado en la personalización, el uso de contexto y la integración de herramientas web sin depender de APIs de pago externas (más allá de OpenAI).

### 🔗 Enlace a la Aplicación Desplegada

Puedes probar la aplicación en vivo aquí:
➡️ **[https://streamlit.io/cloud](https://viajero-ai-pro-ppg9h8tdfqcbnhm7pappbdl.streamlit.app)**

---

## 🛠️ Características Clave

* **Personalización Profunda:** Genera itinerarios basados en Ciudad de Origen, Destino, Fechas exactas, Presupuesto e Intereses específicos (Gastronomía, Historia, Naturaleza, etc.).
* **Cotización Estimada:** Utiliza la búsqueda web en tiempo real (DuckDuckGo) para encontrar rangos de precios actuales de vuelos y hoteles, proporcionando un presupuesto estimado total.
* **RAG Dinámico (Uso de Herramientas):** Busca información fresca (clima, eventos, precios) en la web antes de generar la respuesta, lo que previene la alucinación de datos obsoletos.
* **Cálculo Logístico:** Calcula automáticamente la duración del viaje a partir de las fechas de inicio y fin.

---

## 💻 Arquitectura y Tecnología

El proyecto sigue un enfoque de Ingeniería Avanzada (E1) utilizando el stack de Python y LangChain:

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Frontend/UI** | `Streamlit` | Interfaz de usuario simple para ingresar las preferencias del viaje. |
| **Orquestación/Backend** | `LangChain` | Gestión de la cadena de lógica (prompt, herramientas, modelo). |
| **Cerebro (LLM)** | `OpenAI (gpt-4o-mini)` | Generación del itinerario y análisis de datos de precios. |
| **Tool Use / RAG** | `DuckDuckGoSearchRun` | Acceso a información en tiempo real (precios, clima, eventos). |

### Diagrama Conceptual

[Puedes incluir aquí un enlace a una imagen del diagrama de arquitectura si lo tienes.]

---

## 🚀 Cómo Usar la Aplicación Desplegada

1.  **Obtener tu API Key:** Consigue una clave de API válida de [OpenAI Platform].
2.  **Configuración:** Abre la barra lateral (Panel de Configuración) e introduce tu **OpenAI API Key**.
3.  **Datos del Viaje:** Introduce tu ciudad de origen y destino, selecciona las fechas de ida y vuelta.
4.  **Preferencias:** Ajusta el presupuesto, intereses y el número de pasajeros.
5.  **Generar Plan:** Haz clic en **"Generar Plan de Viaje"**.

El modelo te devolverá dos secciones: una **Cotización Estimada** y un **Itinerario** detallado día por día.

---

## ⚙️ Configuración y Ejecución Local

Si deseas ejecutar este proyecto en tu propia máquina (entorno local):

### Prerrequisitos

* Python 3.8+
* Una cuenta de OpenAI con una API Key activa.

### Pasos

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/TuUsuario/viajero-ai-pro.git](https://github.com/TuUsuario/viajero-ai-pro.git)
    cd viajero-ai-pro
    ```

2.  **Crear y Activar Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # .\venv\Scripts\activate  # Windows
    ```

3.  **Instalar Dependencias:**
    Instala las librerías listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la Aplicación:**
    ```bash
    streamlit run app.py
    ```
    Esto abrirá la aplicación en tu navegador (normalmente en `http://localhost:8501`).

---

## 📝 Archivos del Proyecto

* **`app.py`**: El código principal de la aplicación Streamlit y la lógica de LangChain.
* **`requirements.txt`**: Listado de dependencias Python necesarias para el despliegue.
* **`README.md`**: Este archivo.
