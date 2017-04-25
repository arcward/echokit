NEXT_COMMAND_ISSUED = 'PlaybackController.NextCommandIssued'
PAUSE_COMMAND_ISSUED = 'PlaybackController.PauseCommandIssued'
PLAY_COMMAND_ISSUED = 'PlaybackController.PlayCommandIssued'
PREVIOUS_COMMAND_ISSUED = 'PlaybackController.PreviousCommandIssued'


class PlaybackController:
    def __init__(self, type, request_id, timestamp, locale):
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale

    def _dict(self):
        return self.__dict__


class NextCommandIssued(PlaybackController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PauseCommandIssued(PlaybackController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PlayCommandIssued(PlaybackController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PreviousCommandIssued(PlaybackController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
