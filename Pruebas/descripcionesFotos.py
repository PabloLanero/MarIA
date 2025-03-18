from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import ollama

# Cargar el modelo BLIP para procesar imágenes
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Función para describir una imagen usando BLIP
def describir_imagen(ruta_imagen):
    # Cargar la imagen
    imagen = Image.open(ruta_imagen).convert('RGB')
    
    # Preprocesar la imagen y prepararla para el modelo
    inputs = processor(imagen, return_tensors="pt")
    
    # Generar la descripción
    out = model.generate(**inputs)
    
    # Decodificar la descripción
    descripcion = processor.decode(out[0], skip_special_tokens=True)
    
    return descripcion

# Función para interactuar con Ollama
def generar_respuesta_con_ollama(prompt):
    # Usar Ollama para generar una respuesta basada en el prompt
    response = ollama.generate(model="deepseek-r1:8B", prompt=prompt)
    return response["response"]

# Ruta de la imagen que quieres describir
ruta_imagen = "C:/Users/Suriv/OneDrive/Imágenes/Wallpapers/Ornstein y smoug.jpg"

# Obtener la descripción de la imagen usando BLIP
descripcion_imagen = describir_imagen(ruta_imagen)
print("Descripción de la imagen (BLIP):", descripcion_imagen)

# Usar Ollama para generar una respuesta basada en la descripción de la imagen
prompt = f"Basado en la siguiente descripción de una imagen, genera una respuesta creativa: {descripcion_imagen}"
respuesta_ollama = generar_respuesta_con_ollama(prompt)
print("Respuesta de Ollama:", respuesta_ollama)