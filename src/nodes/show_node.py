import cv2

from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement


class ShowNode:
    def __init__(self, config):
        self.imshow = config['imshow']
        self.show_detections = config['show_detections']

        # Параметры для шрифтов:
        self.fontFace = 1
        self.fontScale = 2.0
        self.thickness = 2

    def process(self, frame_element: FrameElement):
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element

        frame_result = frame_element.frame.copy()

        if self.show_detections:
            for bbox, class_name in zip(frame_element.xyxy, frame_element.cls):
                x1, y1, x2, y2 = bbox

                cv2.rectangle(frame_result, (x1, y1), (x2, y2), (0, 0, 0), 2)
                cv2.putText(
                    frame_result,
                    class_name,
                    (x1, y1 - 10),
                    color=(0, 0, 255),
                    fontFace=self.fontFace,
                    fontScale=self.fontScale,
                    thickness=self.thickness
                )

        if self.imshow:
            cv2.imshow(frame_element.source, frame_result)
            cv2.waitKey(1)

        return frame_element
