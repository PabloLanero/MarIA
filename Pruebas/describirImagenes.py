from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Cargar el procesador y el modelo
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Función para describir una imagen
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

# Ruta de la imagen que quieres describir
ruta_imagen = "C:/Users/Suriv/OneDrive/Imágenes/Wallpapers/20230210223548_1.jpg"

# Obtener la descripción de la imagen
descripcion = describir_imagen(ruta_imagen)
print("Descripción de la imagen:", descripcion)