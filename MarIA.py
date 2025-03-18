from pydantic import BaseModel
from typing import List, Optional
from ollama import chat
from metodosMarIA import metodos
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
from transformers import pipeline


# Define el esquema para la respuesta de la IA
class MetodoSeleccionado(BaseModel):
    metodo: str  # Nombre del método a ejecutar
    argumentos: Optional[List[str]] = None  # Argumentos para el método




# Variable global para almacenar el historial
historial = []

"""


1. **saludar**:  
   - Argumentos: Ninguno.  
   - Descripción: Muestra un mensaje de bienvenida amigable.  
   - Cuándo usarlo: Al iniciar la interacción o cuando el usuario solicite un saludo.

2. **despedirse**:  
   - Argumentos: Ninguno.  
   - Descripción: Muestra un mensaje de despedida cordial.  
   - Cuándo usarlo: Cuando el usuario quiera finalizar la conversación.

    3. **sumar**:  
   - Argumentos: Dos números (ej: "5", "3").  
   - Descripción: Realiza la suma de dos valores numéricos.  
   - Cuándo usarlo: Cuando el usuario solicite sumar dos cantidades.

7. **cambiar_pestana**:  
   - Argumentos: Índice numérico (ej: "2").  
   - Descripción: Cambia a una pestaña específica según su posición.  
   - Cuándo usarlo: Para navegar entre pestañas abiertas usando números.
   
12. **mostrar_historial**:  
    - Argumentos: Ninguno.  
    - Descripción: Muestra el registro de acciones realizadas.  
    - Cuándo usarlo: Para consultar el historial de operaciones.
    
    ---

### 7. **abrir_enlace_en_nueva_pestaña**:  
   - **Argumentos**: URL completa (ej: "https://google.com").  
   - **Descripción**: Abre un enlace específico en una nueva pestaña sin abandonar la pestaña actual.  
   - **Cuándo usarlo**:  
     - Para navegar a URLs específicas sin cerrar la pestaña actual.  
     - Cuando el usuario quiera mantener la página actual abierta.  
   - **Ejemplos**:  
     - "Abre https://google.com en una nueva pestaña".  
     - "Navega a https://wikipedia.org en otra pestaña".  
"""

# Función para que la IA decida qué método ejecutar
def decidir_metodo(texto):
    global historial  # Accedemos a la variable global

    # Descripción detallada de los métodos (usando el system_message mejorado)
    system_message = '''
Elige el método a ejecutar basado en el texto del usuario. Las opciones son:

---

### 1. **abrir_navegador**:  
   - **Argumentos**: Ninguno.  
   - **Descripción**: Inicia el navegador Microsoft Edge.  
   - **Cuándo usarlo**:  
     - Cuando el usuario solicite abrir el navegador por primera vez.  
     - Cuando no haya ninguna instancia del navegador en ejecución.  
   - **Ejemplos**:  
     - "Abre el navegador Edge".  
     - "Inicia Microsoft Edge".  

---

### 2. **cerrar_navegador**:  
   - **Argumentos**: Ninguno.  
   - **Descripción**: Cierra completamente el navegador Microsoft Edge.  
   - **Cuándo usarlo**:  
     - Cuando el usuario quiera finalizar la sesión de navegación.  
     - Cuando se necesite liberar recursos del sistema.  
   - **Ejemplos**:  
     - "Cierra el navegador".  
     - "Finaliza Microsoft Edge".  

---

### 3. **crear_pestana_nueva**:  
   - **Argumentos**: URL (opcional, ej: "https://google.com").  
   - **Descripción**: Abre una nueva pestaña en el navegador. Si se proporciona una URL, navega automáticamente a esa dirección.  
   - **Cuándo usarlo**:  
     - Para abrir pestañas adicionales sin cerrar las existentes.  
     - Para acceder rápidamente a una URL específica en una nueva pestaña.  
   - **Ejemplos**:  
     - "Abre una nueva pestaña".  
     - "Abre una pestaña y ve a https://google.com".  

---

### 4. **cerrar_pestana_actual**:  
   - **Argumentos**: Ninguno.  
   - **Descripción**: Cierra la pestaña en uso actualmente.  
   - **Cuándo usarlo**:  
     - Para cerrar la pestaña activa sin afectar las demás.  
     - Cuando el usuario ya no necesite la pestaña actual.  
   - **Ejemplos**:  
     - "Cierra esta pestaña".  
     - "Cierra la pestaña actual".  

---

### 5. **buscar_informacion**:  
   - **Argumentos**: Término de búsqueda (ej: "clima en Madrid").  
   - **Descripción**: Realiza una búsqueda web en la página actual utilizando el término proporcionado.  
   - **Cuándo usarlo**:  
     - Cuando el usuario pida buscar contenido en internet.  
     - Cuando se necesite encontrar información específica en la web.  
   - **Ejemplos**:  
     - "Busca el clima en Madrid".  
     - "Encuentra información sobre inteligencia artificial".  

---

### 6. **resumir_pagina**:  
   - **Argumentos**: Ninguno.  
   - **Descripción**: Genera un resumen del contenido principal de la página web actual.  
   - **Cuándo usarlo**:  
     - Cuando el usuario solicite un resumen o síntesis del contenido de la página.  
     - Para obtener una visión rápida del contenido sin leer todo el texto.  
   - **Ejemplos**:  
     - "Resume esta página".  
     - "Haz un resumen del contenido".  



---

### 8. **click_resultado_busqueda**:  
   - **Argumentos**: Número (ej: "2") o texto (ej: "Python.org").  
   - **Descripción**: Hace clic en un resultado específico de una búsqueda en Google u otro motor de búsqueda.  
   - **Cuándo usarlo**:  
     - Cuando el usuario esté en una página de resultados de búsqueda (como Google) y pida seleccionar un resultado por su posición o texto.  
     - Una vez utilizado, no se volverá a usar hasta que se ejecute otro método.  
   - **Ejemplos**:  
     - "Abre el tercer resultado".  
     - "Selecciona el enlace que dice 'Python.org'".  

---

### 9. **interactuar_con_pagina**:  
   - **Argumentos**: Texto que describe la acción (ej: "haz clic en el botón de login").  
   - **Descripción**: Interactúa con elementos específicos de la página actual, como botones, campos de texto, menús desplegables, enlaces, etc.  
   - **Cuándo usarlo**:  
     - Cuando el usuario pida interactuar con elementos dentro de una página web que ya está abierta (no en resultados de búsqueda).  
     - Principalmente después de haber ejecutado el método `click_resultado_busqueda`.  
   - **Ejemplos**:  
     - "Haz clic en el botón de enviar".  
     - "Escribe tu nombre en el campo de texto".  
     - "Selecciona 'España' en el menú desplegable".  

---

### Reglas adicionales:
- Devuelve SOLO el nombre del método y los argumentos como lista de strings.  
- No generes nombres de métodos que no existen.  
- Si el texto del usuario no coincide con ningún método, devuelve `None`.  
'''

    # Añadimos el historial al contexto
    historial_contexto = "\nHistorial de acciones recientes:\n"
    if historial:
        historial_contexto += "\n".join(historial[-5:])  # Mostrar las últimas 5 acciones
    else:
        historial_contexto += "No hay acciones recientes."

    # Pregunta a la IA qué método debe ejecutarse
    response = chat(
        model='deepseek-r1:14b',
        messages=[
            {'role': 'system', 'content': system_message},
            {'role': 'assistant', 'content': historial_contexto},  # Incluimos el historial
            {'role': 'user', 'content': texto}
        ],
        format=MetodoSeleccionado.model_json_schema(),
        options={'temperature': 0},
    )

    # Valida y devuelve la respuesta de la IA
    return MetodoSeleccionado.model_validate_json(response.message.content)

# Función para ejecutar el método seleccionado
def ejecutar_metodo_seleccionado(texto, metodos_instancia):
    global historial  # Accedemos a la variable global

    # Pide a la IA que decida el método y los argumentos
    decision_ia = decidir_metodo(texto)
    print(decision_ia)
    metodo_seleccionado = decision_ia.metodo
    argumentos = decision_ia.argumentos or []

    # Registra la acción en el historial
    accion = f"Acción: {metodo_seleccionado}"
    if argumentos:
        accion += f", Argumentos: {', '.join(argumentos)}"
    historial.append(accion)

    # Usa getattr para obtener el método de la instancia
    if hasattr(metodos_instancia, metodo_seleccionado):
        metodo = getattr(metodos_instancia, metodo_seleccionado)
        try:
            # Intenta ejecutar el método con los argumentos proporcionados
            if argumentos:
                metodo(*argumentos)
            else:
                metodo()
        except TypeError as e:
            print(f"Error al ejecutar el método '{metodo_seleccionado}': {e}")
    else:
        print(f"Error: El método '{metodo_seleccionado}' no existe.")

# Ejemplo de uso
metodos_instancia = metodos()
def mostrar_historial():
    global historial
    if historial:
        print("\nHistorial de acciones:")
        for i, accion in enumerate(historial, 1):
            print(f"{i}. {accion}")
    else:
        print("No hay acciones registradas en el historial.")

# Inicialización del motor de síntesis de voz
engine = pyttsx3.init()

# Cargar un modelo de procesamiento del lenguaje natural
nlp_model = pipeline("text-classification")

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()
#Funcion para escuchar lo que dice el usuario
def listen():
    with sr.Microphone() as source:
        # Ajustar el umbral de ruido
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Escuchando...")
        
        # Escuchar el audio con un tiempo de espera más largo
        audio = recognizer.listen(source, phrase_time_limit=50)  # Aumenta el tiempo de escucha si es necesario
        
        try:
            # Reconocer el audio usando Google Web Speech API
            query = recognizer.recognize_google(audio, language='es-ES')
            print(f"Usuario dijo: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None
        except sr.RequestError:
            print("Error en la solicitud al servicio de reconocimiento de voz")
            return None

        
# Ejecuta los métodos basados en los textos
while True:
    texto = listen()
    #texto = input("Escribe tu mensaje: ") 
    if texto:
        if texto.lower() == "historial":
            speak("Enseguida")
            mostrar_historial()
            continue
    
        print(f"\nTexto: {texto}")
        ejecutar_metodo_seleccionado(texto, metodos_instancia)