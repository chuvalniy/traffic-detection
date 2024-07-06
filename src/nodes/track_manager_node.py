from elements.frame_element import FrameElement
from elements.video_end_break_element import VideoEndBreakElement
from elements.track_element import TrackElement


def has_road_intersection(bbox: tuple, road_poly: list) -> bool:
    """
    Check number of objects that are inside road polygon using Ray Casting.
    :param bbox: Bounding box of car object (x1, y1, x2, y2).
    :param road_poly: Road polygon coordinates [[x1, y1], [x2, y2], ...]
    :return: int
    """

    x1_box, y1_box, x2_box, y2_box = bbox
    # Iterate over all detection for specific frame
    cx, cy = x1_box + (x2_box - x1_box) // 2, y1_box + (y2_box - y1_box) // 2
    # Ray casting to check if point is inside a polygon.

    n_edges_crossed = 0
    for (x1, y1), (x2, y2) in zip(road_poly, road_poly[1:]):
        if (cy < y1) != (cy < y2) and cx < x1 + ((cy - y1) / (y2 - y1)) * (x2 - x1):
            n_edges_crossed += 1

    # If we cross odd number of edges it means that we're inside that polygon
    has_intersection = n_edges_crossed % 2 == 1

    return has_intersection


class TrackManagerNode:
    """
    Модуль для обработки треков.
    """

    def __init__(self, config):
        self.size_buffer_analytics = config['buffer_analytics'] * 60  # Переводим в секунду из минут
        self.size_buffer_analytics += config['min_lifetime_track']

        self.roads = [config[f'road_{i}'] for i in range(1, 100) if f'road_{i}' in config]

        self.buffer_tracks = {}

    def process(self, frame_element: FrameElement):
        if isinstance(frame_element, VideoEndBreakElement):
            return frame_element
        assert isinstance(
            frame_element, FrameElement
        ), f"{self.__name__} | Неправильный формат входного элемента {type(frame_element)}"
        id_list = frame_element.id_list

        frame_element.roads_info = self.roads.copy()
        for i, idx in enumerate(id_list):
            if idx not in self.buffer_tracks:
                self.buffer_tracks[idx] = TrackElement(
                    track_id=idx,
                    timestamp_first=frame_element.timestamp
                )
            else:
                self.buffer_tracks[idx].update(frame_element.timestamp)

            if self.buffer_tracks[idx].start_road is None:
                for road_id, road in enumerate(self.roads):
                    if has_road_intersection(bbox=frame_element.tracked_xyxy[i], road_poly=road):
                        self.buffer_tracks[idx].start_road = road_id

                if self.buffer_tracks[idx].start_road is not None:
                    self.buffer_tracks[idx].timestamp_init_road = frame_element.timestamp

        keys_to_remove = []
        for key, track_element in sorted(self.buffer_tracks.items()):
            if frame_element.timestamp - track_element.timestamp_first < self.size_buffer_analytics:
                break
            else:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            self.buffer_tracks.pop(key)

        frame_element.buffer_tracks = self.buffer_tracks

        return frame_element
