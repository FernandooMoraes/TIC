import cv2
import os

def extract_frames(video_path, output_folder, interval=1):
    # Cria a pasta de saída se não existir
    # Extrai o nome do arquivo
    file_name_video = os.path.basename(video_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Abre o vídeo
    cap = cv2.VideoCapture(video_path)

    # Verifica se o vídeo foi aberto com sucesso
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        return

    # Obtém a taxa de frames por segundo (fps)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        print("Não foi possível obter a taxa de FPS do vídeo.")
        cap.release()
        return

    frame_interval = int(fps * interval)

    # Inicializa o contador de frames
    frame_count = 0

    while True:
        # Lê um frame do vídeo
        ret, frame = cap.read()

        # Verifica se o frame foi lido com sucesso
        if not ret:
            break

        # Se o frame atual deve ser salvo
        if frame_count % frame_interval == 0:
            #cv2.imshow("Janela", frame) #caso queira visualizar a janela com o frame
            # # Define o nome do arquivo para o frame
            frame_filename = os.path.join(output_folder, f"{file_name_video}_frame_{frame_count}.jpg")
            result = cv2.imwrite(frame_filename, frame)
            if result:
                print(f"Salvando: {frame_filename}")
            else:
                print(f"Erro ao salvar: {frame_filename}")

        # Incrementa o contador de frames
        frame_count += 1

    # Libera o vídeo
    cap.release()
    print(f"Frames extraídos e salvos na pasta: {output_folder}")

# Caminho para o vídeo e pasta de saída
output_folder = 'output_folder'
video_path = 'video\\path'
# Intervalo em segundos entre frames extraídos
interval = 1/2  
extract_frames(video_path, output_folder, interval)

#Você pode tentar utilizar o codigo abaixo para fazer isso de forma automática para varios videos na pasta
#all_files = os.listdir("video\\path")
#print(all_files)
#for video_file in all_files:
#    video_path = 'video\\path' + video_file
# Extrai os frames
#    extract_frames(video_path, output_folder, interval)