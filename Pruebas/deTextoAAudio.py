from gtts import gTTS
import os

def texto_a_audio(texto, archivo_salida="output.mp3", idioma="es"):
    """
    Convierte un texto a audio y lo guarda como un archivo de audio.

    :param texto: El texto que deseas convertir a audio.
    :param archivo_salida: El nombre del archivo de salida (por defecto es "output.mp3").
    :param idioma: El idioma en el que se generará el audio (por defecto es "es" para español).
    """
    try:
        # Crear el objeto gTTS
        tts = gTTS(text=texto, lang=idioma, slow=False)
        
        # Guardar el archivo de audio
        tts.save(archivo_salida)
        
        print(f"El archivo de audio '{archivo_salida}' ha sido creado exitosamente.")
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    texto = input("Introduce el texto que deseas convertir a audio: ")
    archivo_salida = input("Introduce el nombre del archivo de salida (con extensión .mp3): ")
    
    texto_a_audio(texto, archivo_salida)