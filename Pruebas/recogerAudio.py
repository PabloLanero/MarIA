import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
from transformers import pipeline

# Inicialización del motor de síntesis de voz
engine = pyttsx3.init()

# Cargar un modelo de procesamiento del lenguaje natural
nlp_model = pipeline("text-classification")

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language='es-ES')
            print(f"Usuario dijo: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None
        except sr.RequestError:
            print("Error en la solicitud al servicio de reconocimiento de voz")
            return None

def get_info(query):
    if "hora" in query:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"La hora actual es {now}")
    elif "buscar" in query:
        search_query = query.split("buscar")[-1].strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Buscando {search_query} en Google")
    elif "abrir youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("Abriendo YouTube")
    elif "abrir navegador" in query:
        webbrowser.open("https://www.google.com")
        speak("Abriendo el navegador")
    else:
        speak("No se pudo entender la consulta")

def main():
    while True:
        query = listen()
        if query:
            get_info(query)

if __name__ == "__main__":
    main()