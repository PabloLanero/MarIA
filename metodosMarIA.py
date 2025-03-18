# metodosMarIA.py (Versión Final)
# Importaciones necesarias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # Importación para WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Importación para EC
from bs4 import BeautifulSoup
from ollama import chat
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict
import time
import pyttsx3

    # Inicialización del motor de síntesis de voz
    
engine = pyttsx3.init()
def speak(text):        
    engine.say(text)
    engine.runAndWait()

class AccionPagina(BaseModel):
    accion: str
    elemento: Optional[Dict[str, str]] = None
    texto: Optional[str] = None
    selector: Optional[str] = None

class metodos:
    def __init__(self):
        self.driver = None
        self.historial = []
        self.ultima_pagina = None
        
        # Configuración de Edge
        self.options = Options()
        self._configurar_navegador()

    def _configurar_navegador(self):
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-infobars")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # ----------------------------
    # Métodos Básicos Originales
    # ----------------------------
    
    def saludar(self):
        """Saluda al usuario"""
        print("¡Hola! Soy tu asistente de Edge. ¿En qué puedo ayudarte hoy?")
    
    def despedirse(self):
        """Se despide del usuario"""
        print("¡Hasta luego! No dudes en llamarme si necesitas más ayuda.")
    
    def sumar(self, a: str, b: str):
        """Suma dos números"""
        try:
            resultado = float(a) + float(b)
            print(f"Resultado: {resultado}")
        except ValueError:
            print("Error: Ingresa números válidos")

    # ----------------------------
    # Gestión de Navegador
    # ----------------------------
    
    def abrir_navegador(self):
        """Abre Microsoft Edge"""
        if not self.driver:
            service = Service(executable_path="./Drivers/Edge/msedgedriver.exe")
            self.driver = webdriver.Edge(service=service, options=self.options)
            self.driver.get("https://www.google.com")
            self._registrar_accion("Navegador abierto")
            speak("Navegador abierto")
    
    def cerrar_navegador(self):
        """Cierra completamente el navegador"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self._registrar_accion("Navegador cerrado")
    

    
    # ----------------------------
    # Gestión de Pestañas
    # ----------------------------
    
    def crear_pestana_nueva(self, url: str = "https://www.google.com"):
        """Abre nueva pestaña"""
        if self.driver:
            self.driver.switch_to.new_window('tab')
            self.driver.get(url)
            self._registrar_accion(f"Nueva pestaña: {url}")
    
    def cerrar_pestana(self):
        """Cierra la pestaña actual"""
        if self.driver and len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            self._registrar_accion("Pestaña cerrada")
    
    def cerrar_pestana_especifica(self, indice: str):
        """Cierra pestaña por índice"""
        if self.driver:
            try:
                indice = int(indice)
                handles = self.driver.window_handles
                if 0 <= indice < len(handles):
                    self.driver.switch_to.window(handles[indice])
                    self.driver.close()
                    if handles:
                        self.driver.switch_to.window(handles[0])
                    self._registrar_accion(f"Cerrada pestaña {indice}")
            except ValueError:
                print("Índice inválido")
    
    def cambiar_pestana_siguiente(self):
        """Cambia a la siguiente pestaña"""
        if self.driver:
            handles = self.driver.window_handles
            current = self.driver.current_window_handle
            new_index = (handles.index(current) + 1) % len(handles)
            self.driver.switch_to.window(handles[new_index])
            self._registrar_accion("Cambio a siguiente pestaña")
    
    # ----------------------------
    # Búsqueda e Interacción
    # ----------------------------
    
    def buscar_informacion(self, query: str, resultado: Optional[str] = None):
        """Realiza una búsqueda y selecciona un resultado si se especifica"""
        if self.driver:
            try:
                speak(f"Buscando {query}")
                
                # Realizar búsqueda
                search_box = self.driver.find_element(By.NAME, 'q')
                search_box.clear()
                search_box.send_keys(query + Keys.RETURN)
                self._registrar_accion(f"Búsqueda: {query}")
                
                # Seleccionar resultado si se especifica
                if resultado:
                    self.click_resultado_busqueda(resultado)
            except Exception as e:
                print(f"Error en búsqueda: {e}")
    
    def abrir_enlace_en_nueva_pestaña(self, url: str):
        """Abre un enlace específico en nueva pestaña"""
        if self.driver:
            try:
                # Validar y completar URL si es necesario
                if not url.startswith(('http://', 'https://')):
                    url = f'https://{url}'
                speak("Abriendo una pestaña nueva")
               
                
                # Abrir nueva pestaña
                self.driver.switch_to.new_window('tab')
                self.driver.get(url)
                self._registrar_accion(f"Nueva pestaña con enlace: {url}")
                
                
                
            except Exception as e:
                print(f"Error abriendo enlace: {e}")
        else:
            print("Error: Navegador no abierto")
    
    def interactuar_con_pagina(self, instruccion: str):
        """
        Ejecuta una acción en la página basada en la instrucción del usuario.
        Incluye análisis de la página, interpretación de la acción y ejecución.
        
        Args:
            instruccion (str): La instrucción del usuario (ej: "haz clic en el botón de login").
        """
        if not self.driver:
            print("Error: El navegador no está abierto")
            return

        try:
            # Paso 1: Obtener el contenido completo de la página
            html = self.driver.page_source

            # Guardar el contenido en un archivo temporal (opcional, para depuración)
            with open("pagina_actual.html", "w", encoding="utf-8") as f:
                f.write(html)

            # Paso 2: Analizar la página con BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Extraer elementos interactivos (botones, enlaces, campos de texto, etc.)
            elementos = []
            for tag in ['a', 'button', 'input', 'select', 'textarea', 'div', 'span']:
                for elem in soup.find_all(tag):
                    info = {
                        'tag': tag,
                        'texto': elem.get_text(strip=True),
                        'id': elem.get('id'),
                        'clases': elem.get('class', []),
                        'name': elem.get('name'),
                        'href': elem.get('href'),
                        'type': elem.get('type'),
                        'placeholder': elem.get('placeholder')
                    }
                    elementos.append(info)

            # Paso 3: Consultar a la IA para determinar la acción
            system_msg = '''
            Analiza la página y la instrucción del usuario para determinar:
            1. Qué acción realizar (click, escribir, seleccionar, resumir).
            2. Qué elemento interactuar.
            3. Qué texto introducir (si es necesario).

            Elementos disponibles (primeros 15):
            {elementos}

            Instrucción del usuario:
            {instruccion}

            Devuelve la acción en formato JSON con:
            - accion (str): click, escribir, seleccionar
            - elemento (dict): atributos del elemento (texto, id, clases, etc.).
            - texto (str, opcional): texto a escribir (si la acción es "escribir").
            '''.format(elementos=str(elementos), instruccion=instruccion)

            response = chat(
                model='deepseek-r1:14b',
                messages=[
                    {'role': 'system', 'content': system_msg},
                    {'role': 'user', 'content': "Realiza la acción solicitada"}
                ],
                format=AccionPagina.model_json_schema(),
                options={'temperature': 0.2}  # Más determinístico
            )

            # Paso 4: Validar y ejecutar la acción
            accion = AccionPagina.model_validate_json(response.message['content'])
            if accion.accion == 'click':
                # Buscar el elemento para hacer clic
                elemento = None
                if accion.elemento.get('id'):
                    elemento = self.driver.find_element(By.ID, accion.elemento['id'])
                elif accion.elemento.get('texto'):
                    elemento = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{accion.elemento['texto']}')]")
                elif accion.elemento.get('name'):
                    elemento = self.driver.find_element(By.NAME, accion.elemento['name'])
                
                if elemento:
                    elemento.click()
                    print(f"Click en elemento: {accion.elemento.get('texto')}")
                else:
                    print("Elemento no encontrado para hacer clic")

            elif accion.accion == 'escribir':
                # Buscar el campo para escribir
                elemento = None
                if accion.elemento.get('id'):
                    elemento = self.driver.find_element(By.ID, accion.elemento['id'])
                elif accion.elemento.get('name'):
                    elemento = self.driver.find_element(By.NAME, accion.elemento['name'])
                elif accion.elemento.get('placeholder'):
                    elemento = self.driver.find_element(By.XPATH, f"//*[@placeholder='{accion.elemento['placeholder']}']")
                
                if elemento:
                    elemento.send_keys(accion.texto)
                    print(f"Texto escrito: {accion.texto}")
                else:
                    print("Campo no encontrado para escribir")

            elif accion.accion == 'resumir':
                # Generar resumen de la página
                texto_pagina = soup.get_text(separator=' ', strip=True)
                palabras = texto_pagina.split()[:5000]  # Limitar a 5000 palabras
                texto_limpiado = ' '.join(palabras)

                if len(texto_limpiado) < 50:
                    print("Error: No hay suficiente contenido para resumir")
                    return

                response = chat(
                    model='deepseek-r1:14b',
                    messages=[
                        {'role': 'system', 'content': 'Genera un resumen conciso del siguiente contenido:'},
                        {'role': 'user', 'content': texto_limpiado}
                    ],
                    options={'temperature': 0.2}
                )
                print("📄 Resumen de la página:")
                print(response.message['content'])

            else:
                print(f"Acción no soportada: {accion.accion}")

            # Registrar la acción en el historial
            self._registrar_accion(f"Interacción: {instruccion}")

        except Exception as e:
            print(f"Error en interacción con la página: {str(e)}")
            
    def click_resultado_busqueda(self, criterio: str):
        """
        Haz clic en un resultado de búsqueda específico.
        
        Args:
            criterio (str): Puede ser un número (ej: "2") o texto (ej: "Python.org").
        """
        if self.driver and "google.com" in self.driver.current_url:
            try:
                # Esperar a que carguen los resultados
                self._esperar_elemento(By.XPATH, "//h3[contains(@class, 'LC20lb')]", timeout=5)
                
                # Obtener todos los resultados
                resultados = self.driver.find_elements(By.XPATH, "//h3[contains(@class, 'LC20lb')]")
                
                if not resultados:
                    print("No se encontraron resultados de búsqueda")
                    return
                
                # Si el criterio es un número (ej: "2" para el segundo resultado)
                if criterio.isdigit():
                    indice = int(criterio) - 1  # Convertir a índice base 0
                    if 0 <= indice < len(resultados):
                        resultados[indice].click()
                        self._registrar_accion(f"Clic en resultado {criterio}")
                    else:
                        print(f"No existe el resultado número {criterio}")
                
                # Si el criterio es texto (ej: "Python.org")
                else:
                    texto_buscado = criterio.lower()
                    for resultado in resultados:
                        if texto_buscado in resultado.text.lower():
                            resultado.click()
                            self._registrar_accion(f"Clic en resultado con texto: {criterio}")
                            return
                    print(f"No se encontró un resultado con el texto: {criterio}")
                    
            except Exception as e:
                print(f"Error seleccionando resultado: {e}")
    
    # ----------------------------
    # Métodos Nuevos
    # ----------------------------
    
    def resumir_pagina(self):
        """Genera un resumen del contenido principal de la página actual."""
        if not self.driver:
            print("Error: El navegador no está abierto")
            return

        try:
            # Obtener el HTML de la página actual
            html = self.driver.page_source
            speak("Ok, pero me llevara un rato largo")
            # Usar BeautifulSoup para extraer el contenido principal
            soup = BeautifulSoup(html, 'html.parser')

            # Eliminar scripts, estilos y otros elementos no relevantes
            for script in soup(["script", "style", "noscript", "meta", "link"]):
                script.decompose()

            # Extraer el texto de la página
            texto_pagina = soup.get_text(separator=' ', strip=True)

            # Limitar el texto a las primeras 10000 palabras para evitar sobrecarga
            palabras = texto_pagina.split()[:10000]
            texto_limpiado = ' '.join(palabras)
            print(texto_limpiado)

            # Verificar si hay suficiente contenido para resumir
            if len(texto_limpiado) < 50:
                print("Error: No hay suficiente contenido para resumir")
                return

            # Generar el resumen usando IA
            response = chat(
                model='llama3.1:8b',
                messages=[
                    {
                        'role': 'system',
                        'content': 'Genera un resumen conciso del siguiente contenido, asegurate que sean menos de 500 palabras y en español:'
                    },
                    {
                        'role': 'user',
                        'content': texto_limpiado
                    }
                ],
                options={'temperature': 0.2}  # Más determinístico
            )

            # Mostrar el resumen
            print("📄 Resumen de la página:")
            print(response.message['content'])
            speak(response.message['content'])
            self._registrar_accion("Resumen generado")

        except Exception as e:
            print(f"Error generando resumen: {e}")
    
    def mostrar_historial(self):
        """Muestra el historial de acciones"""
        print("\n🕒 Historial:")
        for i, accion in enumerate(self.historial, 1):
            print(f"{i}. {accion}")
    
    # ----------------------------
    # Métodos Auxiliares
    # ----------------------------
    
    
    
    def _registrar_accion(self, accion: str):
        """Guarda acción en historial"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.historial.append(f"[{timestamp}] {accion}")
        
    def listar_resultados(self):
        """Muestra todos los resultados de búsqueda disponibles"""
        if self.driver and "google.com" in self.driver.current_url:
            try:
                resultados = self.driver.find_elements(By.XPATH, "//h3[contains(@class, 'LC20lb')]")
                if resultados:
                    print("\n🔍 Resultados de búsqueda:")
                    for i, resultado in enumerate(resultados, 1):
                        print(f"{i}. {resultado.text}")
                else:
                    print("No se encontraron resultados")
            except Exception as e:
                print(f"Error listando resultados: {e}")
                
    def _esperar_elemento(self, by: str, value: str, timeout: int = 10):
        """Espera a que un elemento esté disponible."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value)))
            return True
        except:
            return False
        

