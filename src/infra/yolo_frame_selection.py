import os

import cv2
import gdown
import numpy as np
import torch
from ultralytics import YOLO

MODEL = 'yolov8n.pt'
FRAME_INTERVAL = 5
CONFIDENCE = 0.6


class YoloFrameSelection:
    def __init__(self, video_url: str = None):
        self.__video_url: str = video_url
        self.__model = YOLO(MODEL)

    def __detect_objects(self, frame) -> bool:
        results = self.__model(frame)
        torch.cuda.empty_cache()
        return any(
            any(score >= CONFIDENCE for score in result.boxes.conf.cpu().numpy())
            for result in results
        )

    def extract_better_frames_with_objects(self) -> tuple[int, list]:
        file_name = "video.mp4"
        gdown.download(self.__video_url, file_name, quiet=False)

        cap = cv2.VideoCapture(file_name)
        if not cap.isOpened():
            raise RuntimeError('Error when opening the video!')

        frame_count = 0
        best_frames: list[np.ndarray] = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % FRAME_INTERVAL == 0:
                if self.__detect_objects(frame):
                    best_frames.append(frame)

            frame_count += 1

        print(f'Evaluated Frames: {frame_count}')
        print(f'Selected Frames: {len(best_frames)}')
        cap.release()

        self.__remove_file(file_name)
        self.__remove_file(MODEL)

        return frame_count, best_frames

    def parse_to_byte(self, frame_as_npndarray: np.ndarray) -> bytes:
        _, buffer = cv2.imencode('.jpg', frame_as_npndarray)
        return buffer.tobytes()

    def __remove_file(self, file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File {file_name} deleted successfully.")
        else:
            print(f"File {file_name} not found for deletion.")
