from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement


class AnalyticsNode:
    """
    Модуль аналитики для подсчета статистики по объектам.
    """

    def __init__(self):
        pass

    def process(self, frame_element: FrameElement):
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element
        assert isinstance(
            frame_element, FrameElement
        ), f"{self.__name__} | Неправильный формат входного элемента {type(frame_element)}"

        # todo: add gathering road info
        info = {
            0: 0,
            1: 0,
            2: 0,
        }
        for track in frame_element.buffer_tracks.values():
            if track.start_road is not None:
                road_id = track.start_road
                info[road_id] += 1

        # TODO: Исправить на вариант с подсчетом количества треков вместо детекций
        frame_element.info = info

        return frame_element
