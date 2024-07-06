class TrackElement:
    def __init__(
            self,
            track_id: int,
            timestamp_first: float,
            start_road: int = None,
    ):
        self.track_id = track_id
        self.timestamp_first = timestamp_first
        self.timestamp_last = timestamp_first

        # Road information
        self.start_road = start_road
        self.timestamp_init_road = timestamp_first

    def update(self, timestamp: float):
        """
        Update timestamp last with current timestamp of this track element.
        :param timestamp:
        :return:
        """
        self.timestamp_last = timestamp
