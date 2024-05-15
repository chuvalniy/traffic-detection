from elements.frame_element import FrameElement


class VideoEndBreakElement(FrameElement):
    def __init__(self, video_source, timestamp):
        self.image_source = video_source
        self.timestamp = timestamp
