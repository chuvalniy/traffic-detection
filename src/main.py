import hydra
from nodes import (
    VideoReader,
    ShowNode,
    DetectionNode
)
import cv2


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(config) -> None:
    video_reader = VideoReader(config['video_reader'])
    show_node = ShowNode(config['show_node'])
    detection_node = DetectionNode(config['detection_node'])

    for frame_element in video_reader.process():
        frame_element = detection_node.process(frame_element)
        frame_element = show_node.process(frame_element)


if __name__ == '__main__':
    main()
