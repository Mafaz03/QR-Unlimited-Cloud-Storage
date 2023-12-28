from PIL import Image
import base64
import qrcode
import cv2
import pyboof as pb
import numpy as np
import os
from pytube import YouTube
import ssl

def split_to_equal_lenght(b64 : str , length : int) -> list[str]:
    slices = 40
    list_of_slices = []
    # Calculate the number of full length
    full_slices = len(b64) // length

    # Iterate over the length
    for i in range(0, full_slices * length, length):
        slice_part = b64[i:i + length]
        list_of_slices.append(slice_part)

    # Handle the remaining part if the length is not an exact multiple
    if len(b64) % length != 0:
        remaining_part = b64[full_slices * length:]
        list_of_slices.append(remaining_part)
    return list_of_slices


def generateQR(b64: str, resize: tuple):

    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )

    qr.add_data(b64)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Resize the QR code image
    resized_qr_img = qr_img.resize(resize)

    return resized_qr_img



def getframenumber(video_path : str):

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        exit()

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return total_frames



class QR_Extractor:
    # Src: github.com/lessthanoptimal/PyBoof/blob/master/examples/qrcode_detect.py
    def __init__(self):
        self.detector = pb.FactoryFiducial(np.uint8).qrcode()
    
    def extract(self, img_path):
        if not os.path.isfile(img_path):
            print('File not found:', img_path)
            return None
        image = pb.load_single_band(img_path, np.uint8)
        self.detector.detect(image)
        qr_codes = []
        for qr in self.detector.detections:
            qr_codes.append({
                'text': qr.message,
                'points': qr.bounds.convert_tuple()
            })
        return qr_codes
    

def base64_to_zip(base64_string : str, output_file : str):
    try:
        # Decode base64 string
        decoded_data = base64.b64decode(base64_string)

        # Write the decoded data to a zip file
        with open(output_file, 'wb') as file:
            file.write(decoded_data)

        print(f"Zip file successfully restored as {output_file}")

    except Exception as e:
        print(f"Error: {e}")


def download_youtube(video_url: str, download_path: str):
    
    # Create SSL 
    ssl._create_default_https_context = ssl._create_unverified_context

    # Create a YouTube object
    yt = YouTube(video_url)

    # Get the stream with the highest resolution (1080p)
    video_stream = yt.streams.filter(res='1080p').first()

    # Check if the stream is available
    if video_stream:
        # Download the video
        video_stream.download(download_path)
        print(f"Video downloaded to {download_path}")
    else:
        print("1080p stream not available for the video.")