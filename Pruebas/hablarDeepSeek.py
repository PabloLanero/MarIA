import ollama
#Es lo mas simple posible este arrchivo
#Recuerda que para poder usarlo tienes que descargar antes el modelo deepseek-r1:8b desde ollama
#IMPORTANTE: No recuerda lo que dice entre mensaje y mensaje, puede ser un problema que habra que mirar como lidiar
while True:
    print("--------------------")
    mensaje = input()
    respuesta = ollama.chat(model="prueba", messages=[{"role":"user","content":f"{mensaje}"}])
    print(respuesta["message"]["content"])