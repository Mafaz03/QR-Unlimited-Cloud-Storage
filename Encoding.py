import cv2
import numpy as np
from tqdm import tqdm
import base64
from scripts import split_to_equal_lenght
from scripts import generateQR


### Encoding
file_to_encode = input("Enter File path to encode: ")
with open(file_to_encode, 'rb') as f:
    b=f.read()
b64 = base64.standard_b64encode(b).decode()
print("Lenght of b64 : ",len(b64))
information = int(input("Amount of inofrmation (10 - 1500): "))
list_of_equal_b64 = split_to_equal_lenght(b64 = b64 , length = information)
print("Lenght of b64 list : ",len(list_of_equal_b64))


filename = input("Enter output filename: ")
# Set up video writer
video_path = f'runs/{filename}.mp4'
frame_size = (1920, 1080)  # Adjust the size based on your requirements
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 24.0  # Set the desired frame rate to 24 fpscat
video_writer = cv2.VideoWriter(video_path, fourcc, fps, frame_size)


count = 0

for i in tqdm(range(len(list_of_equal_b64))):
    qrimg = generateQR(b64=list_of_equal_b64[i],resize=(540, 540))

    qr_array = np.array(qrimg)
    qr_array = np.where(qr_array == 1, 255, qr_array)

    if count == 0:
        blank = np.zeros((1080, 1920))
        blank[270:810, 75:615] = qr_array
        count += 1

    elif count == 1:
        blank[270:810, 690:1230] = qr_array
        count += 1

    elif count == 2:
        blank[270:810, 1305:1845] = qr_array
        video_writer.write(cv2.cvtColor(blank.astype(np.uint8), cv2.COLOR_GRAY2BGR))  # Convert to BGR for writing
        count = 0

# Release the video writer
video_writer.release()
print(f"Video saved successfully at {video_path}")
