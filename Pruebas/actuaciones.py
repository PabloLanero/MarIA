import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import re
from transformers import pipeline

# 1. Cargar el dataset (asegúrate de tener un archivo dataset.csv)
# El archivo CSV debe tener dos columnas: "texto" y "categoria"
dataset = pd.read_csv("datos.csv")

# 2. Crear un pipeline con TF-IDF y Naive Bayes
modelo = make_pipeline(TfidfVectorizer(), MultinomialNB())

# 3. Entrenar el modelo
modelo.fit(dataset["texto"], dataset["categoria"])

# 4. Definir las funciones que ejecutarán las acciones
def informacion():
    pass

def ajustar_brillo(porcentaje):
    return f"Brillo ajustado al {porcentaje}%"

def ajustar_volumen(porcentaje=None):
    if porcentaje:
        return f"Volumen ajustado al {porcentaje}%"
    else:
        return "Volumen bajado"

# 5. Mapeo de categorías a funciones
funciones = {
    "informacion": informacion,
    "ajustar_brillo": ajustar_brillo,
    "ajustar_volumen": ajustar_volumen,
}

# 6. Función para procesar el texto del usuario
def procesar_texto(texto):
    # Clasificar la intención del texto usando el modelo entrenado
    categoria = modelo.predict([texto])[0]

    # Extraer valores numéricos o porcentajes (si existen)
    valores = re.findall(r"\d+%?", texto)  # Encuentra números seguidos o no de "%"
    porcentaje = int(valores[0].replace("%", "")) if valores else None

    # Llamar a la función correspondiente
    if categoria in funciones:
        if categoria in ["ajustar_brillo", "ajustar_volumen"]:
            # Si la categoría requiere un valor, lo pasamos como argumento
            return funciones[categoria](porcentaje)
        else:
            # Si no requiere un valor, llamamos a la función sin argumentos
            return funciones[categoria]()
    else:
        return None  # Si no hay una categoría válida, devolvemos None

# 7. Cargar un modelo de Hugging Face para clasificación zero-shot
try:
    modelo_hf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")  # Puedes usar otro modelo si prefieres
except Exception as e:
    print(f"Error al cargar el modelo de Hugging Face para clasificación zero-shot: {e}")
    modelo_hf = None

# 8. Método para interactuar con la IA
def interactuar_con_ia():
    print("¡Hola! Soy tu asistente virtual. Puedes hablar conmigo. Escribe 'salir' para terminar.")
    while True:
        # Solicitar entrada al usuario
        texto_usuario = input("Tú: ")
        
        # Salir si el usuario escribe "salir"
        if texto_usuario.lower() == "salir":
            print("Asistente: ¡Hasta luego!")
            break
        
        # Procesar el texto con el modelo personalizado
        respuesta = procesar_texto(texto_usuario)
        
        # Si el modelo personalizado no tiene una respuesta, usar el modelo de Hugging Face para clasificación zero-shot
        if respuesta is None and modelo_hf is not None:
            try:
                resultado = modelo_hf(texto_usuario, candidate_labels=["informacion", "ajustar_brillo", "ajustar_volumen"])
                categoria = resultado['labels'][0]  # Tomamos la primera etiqueta como categoría más probable
                respuesta = funciones[categoria]() if categoria in funciones else None
            except Exception as e:
                print(f"Error en el modelo de clasificación zero-shot: {e}")
                respuesta = "Hubo un error al procesar tu solicitud."
        
        # Mostrar la respuesta
        print(f"Asistente: {respuesta}")


# 9. Ejecutar la interacción
if __name__ == "__main__":
    interactuar_con_ia()