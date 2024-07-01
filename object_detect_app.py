import cv2
import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
MODEL = "model/MobileNetSSD_deploy.caffemodel"
PROTOTXT = "model/MobileNetSSD_deploy.prototxt.txt"


def process_image(image):
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    net.setInput(blob)
    detections = net.forward()
    return detections


def annotate_image(image, detections, confidence_threshold=0.5):

    (h, w) = image.shape[:2]
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confidence_threshold:
            int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = box.astype("int")
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), 80, 3)
    return image


def annotate_video(video, output_video_path="temp.mp4"):
    video = cv2.VideoCapture(video)
    fps_video = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps_video, size)
    while True:
        ret, frame = video.read()

        if not ret:
            break
        detections = process_image(frame)
        process_frame = annotate_image(frame, detections=detections)

        out.write(process_frame)
    video.release()
    out.release()

    with open('temp.mp4', 'rb') as f:
        video_bytes = BytesIO(f.read())

    return video_bytes

def main():
    st.title('Object Detection for Images')
    file = st.file_uploader("Upload file", type=['png', 'jpeg', 'jpg'])
    if file is not None:
        st.image(file, caption='Uploaded image')

        image = Image.open(file)
        image = np.array(image)
        detections = process_image(image)
        image_processed = annotate_image(image, detections)
        st.image(image_processed, caption="processed image")


if __name__ == "__main__":
    main()
