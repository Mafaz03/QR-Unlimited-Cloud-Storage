import numpy as np
import cv2
from scripts import getframenumber
from scripts import base64_to_zip
from scripts import download_youtube
from scripts import QR_Extractor
from tqdm import tqdm
import os
from PIL import Image, ImageFilter

option = int(input(("\nLoad Video from local directory(0) or youtube(1): ")))
if option == 0:
    video_path = input("Video to decode path: ")
    ouput_name = input("Output file name: ")
elif option == 1:
    video_url = input("Youtube URL to decode : ")
    ouput_name = input("Output file name: ")
    yt_video_path = f"runs/{ouput_name}"
    download_youtube(video_url = video_url , download_path = yt_video_path)

    vid_name = os.listdir(f"runs/{ouput_name}")
    video_path = f"runs/{ouput_name}/{vid_name[0]}"

frames = getframenumber(video_path = video_path)
print(f"Total frames in the video: {frames}")

qr_scanner = QR_Extractor()

cap = cv2.VideoCapture(video_path)

complete_b64 = ""
start_frame = 0
end_frame = frames

for frame_number in tqdm(range(start_frame, end_frame)):
    # Set the current frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame from the video
    ret, frame = cap.read()
    # Check if the frame was read successfully
    if not ret:
        print("Error reading frame")
        break
    
    for i in range(3):

        roi = frame[270:810, 75 + (615 * i) : 615 + (615 * i)]
        roi_image = Image.fromarray(roi)
        # Apply the sharpen filter
        sharpened_roi = roi_image.filter(ImageFilter.SHARPEN)
        qr = np.array(sharpened_roi)
        
        cv2.imwrite('temp/temp.png', qr)
        
        output = qr_scanner.extract(f'temp/temp.png')
        part_of_b64 = output[0]["text"]
        complete_b64 += part_of_b64

base64_to_zip(complete_b64 , f"ZipFilesOutput/{ouput_name}.zip")