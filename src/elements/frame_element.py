import numpy as np
from typing import Optional


class FrameElement:
    """
    Contains information about a frame from a video stream.
    """

    def __init__(
            self,
            source: str,
            frame: np.ndarray,
            timestamp: float,
            frame_num: float,
            buffer_tracks: dict = None,
            id_list: Optional[list] = None,
            tracked_conf: Optional[list] = None,
            tracked_cls: Optional[list] = None,
            tracked_xyxy: Optional[list] = None,
    ):
        self.source = source
        self.frame = frame
        self.timestamp = timestamp
        self.frame_num = frame_num

        # Detections
        self.conf = []
        self.xyxy = []
        self.cls = []

        # Tracking
        self.id_list = id_list
        self.tracked_conf = tracked_conf
        self.tracked_cls = tracked_cls
        self.tracked_xyxy = tracked_xyxy

        self.buffer_tracks = buffer_tracks
