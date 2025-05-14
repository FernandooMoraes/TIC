import os
from pathlib import Path
from typing import Optional
from datetime import datetime
import cv2 as cv
import mss
import numpy as np
from ultralytics import YOLO
from time import time, sleep
from typing import Optional, Dict
import random
import math
from collections import defaultdict
import json

def save_results_to_json(results, date, camera_name, file_path: str) -> None:
    """
    Salva os resultados do YOLO em um arquivo JSON, adicionando um novo registro com timestamp.

    Args:
        results: Os resultados da inferência do YOLO.
        file_path (str): O caminho do arquivo JSON para salvar os resultados.
    """
    # Inicializa a lista de detecções
    detections = []
    
    for result in results:
        for box in result.boxes:
            detections.append({
                "class": int(box.cls),  # Classe detectada
                "confidence": float(box.conf),  # Confiança da detecção
                "bbox": box.xywh.tolist()  # Coordenadas da caixa delimitadora (x, y, w, h)
            })

    # Adiciona timestamp
    data = {
        "timestamp": date,
        "detections": detections,
        "camera": camera_name, 
    }

    # Lê o conteúdo existente no arquivo JSON ou inicializa uma nova lista
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                file_data = json.load(f)
                # Verifica se o conteúdo é um dicionário vazio e converte para uma lista
                if isinstance(file_data, dict):
                    file_data = [file_data]
            except json.JSONDecodeError:
                # Se o arquivo estiver vazio ou corrompido, inicializa como uma lista
                file_data = []
    else:
        file_data = []

    # Adiciona os novos resultados à lista
    file_data.append(data)

    # Salva o conteúdo atualizado no arquivo JSON
    with open(file_path, 'w') as f:
        json.dump(file_data, f, indent=4)

def save_annotated_image(image: np.ndarray, date: str, camera_name: str, folder_path: str) -> None: 
    """
    Salva a imagem anotada com as detecções, nomeando com o timestamp atual.

    Args:
        image (np.ndarray): A imagem anotada para salvar.
        folder_path (str): O caminho da pasta onde a imagem será salva.
    """
    # Cria a pasta se não existir
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Define o nome do arquivo com o timestamp
    file_name = f"{camera_name}_detection_{date}.png"
    file_path = os.path.join(folder_path, file_name)
    print(file_path)
    # Salva a imagem anotada
    cv.imwrite(file_path, image)

def main(directory: str, model_path: Optional[str] = None, model_path2: Optional[str] = None,model_path3: Optional[str] = None,model_path4: Optional[str] = None
         , output_json: str = "output.json", output_json2: str = "output2.json", output_json3: str = "output3.json", output_json4: str = "output4.json", image_folder: str = "detections") -> None:
    if not os.path.exists(directory):
            print(f"O diretório '{directory}' não existe.")
            return
    model = YOLO(model_path)
    model2 = YOLO(model_path2)
    model3 = YOLO(model_path3)
    model4 = YOLO(model_path4)
    #model5 = YOLO(model_path5)
    
    
    i = 1
    for filename in os.listdir(directory):
        t = i+1
        camera_name = filename.split('f')[0]
        file_path = os.path.join(directory, filename)
        screenshot = cv.imread(file_path)
        # Run YOLOv8 inference on the frame
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results = model(screenshot)
        results2 = model2(screenshot)
        if len(results[0].boxes) > 0:
            annotated_framemod1 = results[0].plot()
            save_annotated_image(annotated_framemod1, date, camera_name, folder_path="C:/Users/ferna/OneDrive/Área de Trabalho/Arma")
            save_results_to_json(results, date, camera_name, 'Arma/' + output_json)
        
        if len(results2[0].boxes) > 0:
            annotated_framemod2 = results2[0].plot()
            save_annotated_image(annotated_framemod2, date, camera_name, folder_path="C:/Users/ferna/OneDrive/Área de Trabalho/Fogo")
            save_results_to_json(results2, date, camera_name, 'Fogo/' + output_json2)
        
        if t / 600 == 1:
            results3 = model3(screenshot)
            results4 = model4(screenshot)
            if len(results3[0].boxes) > 0:
                    annotated_framemod3 = results3[0].plot()
                    save_annotated_image(annotated_framemod3, date, camera_name, folder_path="C:/Users/ferna/OneDrive/Área de Trabalho/Alagamento")
                    save_results_to_json(results3, date, camera_name,'Alagamento/' + output_json3)

            if len(results4[0].boxes) > 0:
                annotated_framemod4 = results4[0].plot()
                save_annotated_image(annotated_framemod4, date, camera_name, folder_path="C:/Users/ferna/OneDrive/Área de Trabalho/Pichação")
                save_results_to_json(results4, date, camera_name,'Pichação/' + output_json4)
    
            t = 1  
        
       #results5 = model5(screenshot)

        # Se houver detecções, salva a imagem anotada

      
        #if len(results5[0].boxes) > 0:
        #    annotated_framemod5 = results5[0].plot()
        #    save_annotated_image(annotated_framemod5, date, folder_path= "Suspeito")
        #    save_results_to_json(results5, date,'Suspeito/' + output_json5)
        print(file_path)
        os.remove(file_path)

if __name__ == "__main__":
    main(directory="C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\detections\\", 
         model_path="C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\TIC\\test-window-capture\\test-window-capture\\public-safety.pt",
          model_path2="C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\TIC\\test-window-capture\\test-window-capture\\public-safety.pt",
           model_path3="C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\TIC\\test-window-capture\\test-window-capture\\public-safety.pt",
            model_path4="C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\TIC\\test-window-capture\\test-window-capture\\public-safety.pt",
             #model_path5="C:\\Users\\ferna\\OneDrive\\Área de Trabalho\\TIC\\test-window-capture\\test-window-capture\\public-safety.pt",
         output_json="output.json",output_json2="output2.json",output_json3="output3.json",output_json4="output4.json")#,output_json5="output5.json")