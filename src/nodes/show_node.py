import cv2

from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement


class ShowNode:
    def __init__(self, config):
        self.imshow = config['imshow']

    def process(self, frame_element: FrameElement):
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element

        frame_result = frame_element.frame.copy()

        if self.imshow:
            cv2.imshow(frame_element.source, frame_result)
            cv2.waitKey(1)

        return frame_element
