from transformers import GroundingDinoModel, AutoProcessor
from PIL import ImageGrab
import torch
import pyautogui

"""
    NO SE INTENTA, NO HAY NINGUN MODELO QUE FUNCIONE CON BUENA PRECISION NI MUCHO MENOS 
    RAPIDO, ASI QUE SE QUEDA EN STANDBY
    
    _summary_
    """



def detectar_elemento(descripcion):
    # Cargar modelo y procesador específicos
    model = GroundingDinoModel.from_pretrained("IDEA-Research/grounding-dino-base")
    processor = AutoProcessor.from_pretrained("IDEA-Research/grounding-dino-base")
    
    # Captura de pantalla
    imagen = ImageGrab.grab().convert("RGB")
    
    # Procesar entrada
    inputs = processor(
        text=[descripcion],
        images=imagen,
        return_tensors="pt"
    )
    
    # Inferencia
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Post-procesamiento
    target_sizes = torch.tensor([imagen.size[::-1]])
    resultados = processor.post_process_grounded_object_detection(
        outputs,
        input_ids=inputs.input_ids,
        target_sizes=target_sizes,
        threshold=0.4
    )[0]
    
    if len(resultados["scores"]) == 0:
        print("Elemento no encontrado")
        return False
    
    # Obtener mejor resultado
    mejor_idx = torch.argmax(resultados["scores"])
    box = resultados["boxes"][mejor_idx]
    
    # Mover ratón
    x = (box[0] + box[2]) // 2
    y = (box[1] + box[3]) // 2
    pyautogui.moveTo(x.item(), y.item())
    return True

if __name__ == "__main__":
    detectar_elemento("La lupa")