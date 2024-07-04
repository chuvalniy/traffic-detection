from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement


class AnalyticsNode:
    """
    Модуль аналитики для подсчета статистики по объектам.
    """

    def __init__(self, config):
        self.roads = [config[f'road_{i}'] for i in range(1, 100) if f'road_{i}' in config]

    def process(self, frame_element: FrameElement):
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element
        assert isinstance(
            frame_element, FrameElement
        ), f"{self.__name__} | Неправильный формат входного элемента {type(frame_element)}"

        # TODO: Надо перенести логику по инициализации дорог в другое место
        frame_element.roads_info = self.roads.copy()

        info = {}
        for i, road in enumerate(frame_element.roads_info):
            n_objects_crossed_road = self._process_road_intersection(frame_element, road)
            info[f'road_{i}'] = n_objects_crossed_road

        # TODO: Исправить на вариант с подсчетом количества треков вместо детекций
        frame_element.info = info

        return frame_element

    def _process_road_intersection(self, frame_element: FrameElement, roads: list) -> int:
        """
        Check number of objects that are inside road polygon using Ray Casting.
        :param frame_element: Frame element with information about detections xyxy.
        :param roads: Roads [[x1, y1], [x2, y2], ...]
        :return: int
        """

        n_inside = 0
        # Iterate over all detection for specific frame
        for xyxy in frame_element.tracked_xyxy:
            x1, y1, x2, y2 = xyxy
            cx, cy = x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2
            # Ray casting to check if point is inside a polygon.
            n_edges_crossed = 0
            for (x1, y1), (x2, y2) in zip(roads, roads[1:]):
                if (cy < y1) != (cy < y2) and cx < x1 + ((cy - y1) / (y2 - y1)) * (x2 - x1):
                    n_edges_crossed += 1

            # If we cross odd number of edges it means that we're inside that polygon
            if n_edges_crossed % 2 == 1:
                n_inside += 1

        return n_inside
