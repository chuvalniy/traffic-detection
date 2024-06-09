class TrackElement:
    def __init__(self, track_id: int, timestamp_first: float):
        self.track_id = track_id
        self.timestamp_first = timestamp_first
        self.timestamp_last = timestamp_first

    def update(self, timestamp: float):
        """
        Update timestamp last with current timestamp of this track element.
        :param timestamp:
        :return:
        """
        self.timestamp_last = timestamp
