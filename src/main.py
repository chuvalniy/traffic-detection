import hydra
from nodes import (
    VideoReader,
    ShowNode,
    DetectionNode,
    TrackingNode,
    TrackManagerNode,
    AnalyticsNode
)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config) -> None:
    video_reader = VideoReader(config['video_reader'])
    show_node = ShowNode(config['show_node'])
    detection_node = DetectionNode(config['detection_node'])
    tracking_node = TrackingNode(config['tracking_node'])
    track_manager_node = TrackManagerNode(config['track_manager_node'])
    analytics_node = AnalyticsNode(config['analytics_node'])

    for frame_element in video_reader.process():
        frame_element = detection_node.process(frame_element)
        frame_element = tracking_node.process(frame_element)
        frame_element = track_manager_node.process(frame_element)
        frame_element = analytics_node.process(frame_element)
        frame_element = show_node.process(frame_element)


if __name__ == '__main__':
    main()
