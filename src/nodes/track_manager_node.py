from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement
from elements.track_element import TrackElement


class TrackManagerNode:
    """
    Модуль для обработки треков.
    """

    def __init__(self, config):
        self.size_buffer_analytics = config['buffer_analytics'] * 60  # Переводим в секунду из минут
        self.size_buffer_analytics += config['min_lifetime_track']

        self.buffer = {}

    def process(self, frame_element: FrameElement):
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element
        assert isinstance(
            frame_element, FrameElement
        ), f"{self.__name__} | Неправильный формат входного элемента {type(frame_element)}"

        id_list = frame_element.id_list

        for i, idx in enumerate(id_list):
            if idx not in self.buffer:
                self.buffer[idx] = TrackElement(
                    track_id=idx,
                    timestamp_first=frame_element.timestamp
                )
            else:
                self.buffer[idx].update(frame_element.timestamp)

        keys_to_remove = []
        for key, track_element in sorted(self.buffer.items()):
            if frame_element.timestamp - track_element.timestamp_first < self.size_buffer_analytics:
                break
            else:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            self.buffer.pop(key)

        frame_element.buffer_track = self.buffer

        return frame_element
