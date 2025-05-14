import cv2
import os


video_path = 'video_path'

file_name_video = os.path.basename(video_path)
# Abre o vídeo
cap = cv2.VideoCapture(video_path)

# Obtém a taxa de frames por segundo (fps)
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(fps)   

all_files = os.listdir("video\\path")
print(all_files)