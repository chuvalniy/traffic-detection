import os
from typing import Generator
import logging
import cv2

from elements.video_end_break_element import VideoEndBreakElement
from elements.frame_element import FrameElement

logger = logging.getLogger(__name__)


class VideoReader:
    def __init__(self, config: dict):
        self.video_pth = config['src']
        self.video_src = f"Processing of {self.video_pth}"

        assert os.path.isfile(self.video_pth)

        self.stream = cv2.VideoCapture(self.video_pth)

        self.skip_secs = config['skip_secs']
        self.last_frame_timestamp = -1
        self.first_timestamp = 0

        self.break_element_sent = False

    def process(self) -> Generator[FrameElement, None, None]:
        frame_number = 0

        while True:
            success, frame = self.stream.read()
            if not success:
                logger.warning("Can't receive frame. Exiting ...")

                if not self.break_element_sent:
                    self.break_element_sent = True
                    yield VideoEndBreakElement(self.video_pth, self.last_frame_timestamp)
                break

            timestamp = self.stream.get(cv2.CAP_PROP_POS_MSEC) / 1000

            timestamp = (
                timestamp
                if timestamp > self.last_frame_timestamp
                else self.last_frame_timestamp + 0.1
            )

            if abs(self.last_frame_timestamp - timestamp) < self.skip_secs:
                continue

            self.last_frame_timestamp = timestamp

            frame_number += 1

            yield FrameElement(self.video_src, frame, timestamp, frame_number)
