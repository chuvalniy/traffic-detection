import numpy as np


class FrameElement:
    def __init__(
            self,
            source: str,
            frame: np.ndarray,
            timestamp: float,
            frame_num: float
    ):
        self.source = source
        self.frame = frame
        self.timestamp = timestamp
        self.frame_num = frame_num
