import numpy as np

import torch

from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement
from byte_tracker.tracker import BYTETracker as ByteTracker


class TrackingNode:
    def __init__(self, config):

        first_track_thresh = config["first_track_thresh"]
        second_track_thresh = config["second_track_thresh"]
        match_thresh = config["match_thresh"]
        track_buffer = config["track_buffer"]
        fps = 30

        self.tracker = ByteTracker(
            fps=fps,
            first_track_thresh=first_track_thresh,
            second_track_thresh=second_track_thresh,
            match_thresh=match_thresh,
            track_buffer=track_buffer,
            resize_width_height=1
        )

    def process(self, frame_element: FrameElement) -> FrameElement:
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element

        assert isinstance(
            frame_element, FrameElement
        ), f"TrackingNode | Неправильный формат входного элемента {type(frame_element)}"

        detections_list = self._convert_detections(frame_element)

        if len(detections_list) == 0:
            detections_list = np.empty((0, 6))

        track_list = self.tracker.update(torch.tensor(detections_list), xyxy=True)

        # Add tracking information to frame element
        frame_element.id_list = [int(t.track_id) for t in track_list]
        frame_element.tracked_xyxy = [list(t.tlbr.astype(int)) for t in track_list]
        frame_element.tracked_cls = [t.class_name for t in track_list]
        frame_element.tracked_conf = [t.score for t in track_list]

        return frame_element

    def _convert_detections(self, frame_element: FrameElement) -> np.ndarray:
        """
        Create a list for each frame in (x1, y1, x2, y2, conf, cls) item format.

        :param frame_element: Contains information about a frame from a video stream.
        :return:
        """
        detections_list = []

        # Iterate over each detection from a frame.
        for xyxy, conf, cls in zip(frame_element.xyxy, frame_element.conf, frame_element.cls):
            merged_detection = [
                xyxy[0],
                xyxy[1],
                xyxy[2],
                xyxy[3],
                conf,
                2  # TODO: Если отправлять cls, то будет ошибка из-за того, что он str
            ]

            detections_list.append(merged_detection)

        return np.array(detections_list)
