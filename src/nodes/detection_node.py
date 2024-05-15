from ultralytics import YOLO

import torch

from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement


class DetectionNode:
    def __init__(self, config):
        device = torch.device(config['device'])
        print("Current device : {}".format(device))

        self.model = YOLO(config['model_path'])
        self.model.fuse()

        self.classes = self.model.names

    def process(self, frame_element: FrameElement) -> FrameElement:
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element

        frame = frame_element.frame.copy()

        results = self.model.predict(frame, verbose=False)

        frame_element.conf = results[0].boxes.conf.cpu().int().tolist()
        frame_element.xyxy = results[0].boxes.xyxy.cpu().int().tolist()

        num_classes = results[0].boxes.cls.cpu().int().tolist()
        frame_element.cls = [self.classes[i] for i in num_classes]

        return frame_element
