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
        self.fontScale = 1.0
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

            # TODO: Fix using .tracked_xyxy instead of buffer_tracks
        if self.show_tracking:
            for bbox, track_id in zip(frame_element.tracked_xyxy, frame_element.id_list):
                x1, y1, x2, y2 = bbox

                # Bounding box
                cv2.rectangle(frame_result, (x1, y1), (x2, y2), (127, 127, 127), 3)

                # Track id
                cv2.putText(
                    frame_result,
                    text=f"id: {track_id}",
                    org=(x1, y1 + 5),
                    fontFace=self.fontFace,
                    fontScale=self.fontScale,
                    thickness=self.thickness,
                    color=(0, 0, 255)
                )

        if self.show_analytics:
            info = frame_element.info
            for i, (k, v) in enumerate(info.items()):
                y = 35 + (i * 20)

                # Выводим текст для количества машин
                n_objects_text = f"Objects inside {k}: {v}"
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
            for road in frame_element.roads_info:
                road = np.array(road, np.int32).reshape((-1, 1, 2))
                cv2.polylines(
                    frame_result,
                    [road],
                    isClosed=True,
                    color=(0, 0, 255),
                    thickness=2
                )

        if self.imshow:
            cv2.imshow(frame_element.source, frame_result)
            cv2.waitKey(1)

        return frame_element
