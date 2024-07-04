import cv2
import numpy as np

from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement


class ShowNode:
    def __init__(self, config):
        self.imshow = config['imshow']
        self.show_detection = config['show_detection']
        self.show_tracking = config['show_tracking']
        self.show_analytics = config['snow_analytics']
        self.show_roi = config['show_roi']

        # Параметры для шрифтов:
        self.fontFace = 1
        self.fontScale = 2.0
        self.thickness = 2

    def process(self, frame_element: FrameElement):
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element

        frame_result = frame_element.frame.copy()

        # TODO: Addd asserts if frame_element.xyxy is None
        if self.show_detection:
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

        if self.show_tracking:
            for bbox in frame_element.tracked_xyxy:
                x1, y1, x2, y2 = bbox

                cv2.rectangle(frame_result, (x1, y1), (x2, y2), (127, 127, 127), 3)

        if self.show_analytics:
            info = frame_element.info

            n_objects_text = f"Objects inside road: {info['n_objects_crossed_road']}"

            y = 55
            # Выводим текст для количества машин
            cv2.putText(
                frame_result,
                text=n_objects_text,
                org=(20, y),
                fontFace=self.fontFace,
                fontScale=self.fontScale * 1.5,
                thickness=self.thickness,
                color=(255, 255, 255),
            )

        if self.show_roi:
            # TODO: Add multiple roads support
            road_1 = np.array(frame_element.roads_info, np.int32).reshape((-1, 1, 2))
            cv2.polylines(
                frame_result,
                [road_1],
                isClosed=True,
                color=(0, 0, 255),
                thickness=2
            )

        if self.imshow:
            cv2.imshow(frame_element.source, frame_result)
            cv2.waitKey(1)

        return frame_element
