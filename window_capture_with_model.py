import os
from pathlib import Path
from time import time
from typing import Optional

import cv2 as cv
import mss
import numpy as np
import win32api
import win32con
import win32gui
from ultralytics import YOLO


def list_window_names() -> None:
    """
    Lista os nomes de todas as janelas visíveis no sistema.

    Esta função utiliza a API do Windows para enumerar todas as janelas
    visíveis e imprime seus identificadores e títulos.
    """

    def winEnumHandler(hwnd: int, ctx: Optional[None]) -> None:
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(winEnumHandler, None)

def capture_window(window_title: str) -> np.ndarray:
    """
    Captura a tela de uma janela específica e retorna a imagem como um array numpy.

    Args:
        window_title (str): O título da janela a ser capturada.

    Returns:
        np.ndarray: Uma imagem da janela capturada como um array numpy.

    Raises:
        Exception: Se a janela com o título especificado não for encontrada.
    """
    # Encontra a janela pelo título
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        raise Exception(f"Janela com o título '{window_title}' não encontrada.")

    # Obtém as dimensões da janela
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    with mss.mss() as sct:
        # Define a área a ser capturada
        monitor = {"top": top, "left": left, "width": width, "height": height}
        screenshot = sct.grab(monitor)

        # Converte a captura para um array numpy
        img = np.array(screenshot)

        # Remove o canal alfa para converter a imagem para 3 canais (RGB) compatível como YOLO
        img = img[:, :, :3]

    return img


def main(window_title: Optional[str] = None, model_name: Optional[str] = None) -> None:
    """
    Captura continuamente a tela de uma janela específica ou da área de trabalho e exibe em uma janela do OpenCV.

    Args:
        window_title (Optional[str]): O título da janela a ser capturada. Se não for especificado, captura a área de trabalho.
        model_name (Optional[str]): Caminho para o modelo que deseja rodar.

    Raises:
        Exception: Se a janela com o título especificado não for encontrada.
    """
    # Change the working directory to the folder this script is in.
    # Doing this because I'll be putting the files from each video in their own folder on GitHub
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if window_title is None:
        hwnd = win32gui.GetDesktopWindow()
    else:
        hwnd = win32gui.FindWindow(None, window_title)
        if not hwnd:
            raise Exception(f'Window not found: {window_title}')

    # Restaura a janela se estiver minimizada, mas sem redimensioná-la
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)

    # Coloca a janela no topo da pilha de janelas sem dar foco e sem redimensionar
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    # Aguarda um momento para garantir que a janela esteja visível
    win32api.Sleep(500)

    # Carrega o modelo
    model_path = Path(__file__).parent / model_name
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"O arquivo do modelo não foi encontrado: {model_path}")
    model = YOLO(model_path)

    loop_time = time()
    while True:
        # Obtém uma imagem atualizada da janela
        screenshot = capture_window(window_title=window_title)

        # Run YOLOv8 inference on the frame
        results = model(screenshot)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv.imshow("YOLOv8 Inference", annotated_frame)

        # Debug da taxa de atualização
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        # Pressione 'q' com a janela de saída focada para sair.
        # Espera 1 ms a cada loop para processar pressionamentos de tecla
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    print('Done.')


if __name__ == "__main__":
    # Para conferir o nome da janela, basta rodar o list_windows_names e pegar o nome da janela depois do código dela
    #list_window_names()

    # Para rodar o modelo na janela, basta substituir o nome da janela exatamente como foi encontrado na lista (menos o código da janela)
    # Lembre-se de mudar o path do modelo desejado
    # Para finalizar o programa, apertar Q depois de clicar na visualização do plot ou fechar a janela que está sendo detectada
    main(window_title="WHARF TALK - YouTube - Google Chrome", model_name="yolov8s.pt")
