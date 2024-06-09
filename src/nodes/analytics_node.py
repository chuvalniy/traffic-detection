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

        # TODO: Исправить на вариант с подсчетом количества треков вместо детекций
        n_objects = len(frame_element.xyxy)

        info = {'n_objects': n_objects}
        frame_element.info = info

        return frame_element
