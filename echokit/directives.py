from enum import Enum
from echokit._utils import enum_contains


class AudioItem:
    def __init__(self, stream):
        self.stream = stream

    def _dict(self):
        return {'stream': self.stream._dict()}


class Stream:
    def __init__(self, url, token, offset_in_milliseconds,
                 expected_previous_token=None):
        self.token = token
        self.url = url
        self.offset_in_milliseconds = offset_in_milliseconds
        self.expected_previous_token = expected_previous_token

    def _dict(self):
        return {k: v for (k, v) in
                self.__dict__.items() if v is not None}


class AudioPlayerDirective:
    @staticmethod
    def play(play_behavior, url, token, offset_in_milliseconds,
             expected_previous_token=None):
        stream = Stream(url, token, offset_in_milliseconds,
                        expected_previous_token)
        return PlayDirective(play_behavior, AudioItem(stream))

    @staticmethod
    def stop():
        return StopDirective()

    @staticmethod
    def clear_queue(clear_behavior):
        return ClearQueueDirective(clear_behavior)


class PlayBehavior(Enum):
    ENQUEUE = 'ENQUEUE'
    REPLACE_ALL = 'REPLACE_ALL'
    REPLACE_ENQUEUED = 'REPLACE_ENQUEUED'


class PlayDirective:
    def __init__(self, play_behavior, audio_item):
        self.type = 'AudioPlayer.Play'
        self._play_behavior = None
        self.play_behavior = play_behavior
        self.audio_item = audio_item

    @property
    def play_behavior(self):
        return self._play_behavior

    @play_behavior.setter
    def play_behavior(self, play_behavior):
        if play_behavior in PlayBehavior:
            self._play_behavior = play_behavior
        elif enum_contains(play_behavior, PlayBehavior):
            self._play_behavior = PlayBehavior(play_behavior)
        else:
            raise ValueError()

    def _dict(self):
        return {
            'type': self.type,
            'play_behavior': self.play_behavior.value,
            'audio_item': self.audio_item._dict()
        }


class ClearBehavior(Enum):
    CLEAR_ALL = 'CLEAR_ALL'
    CLEAR_ENQUEUED = 'CLEAR_ENQUEUED'


class ClearQueueDirective:
    def __init__(self, clear_behavior):
        self.type = 'AudioPlayer.ClearQueue'
        self._clear_behavior = None
        self.clear_behavior = clear_behavior

    @property
    def clear_behavior(self):
        return self._clear_behavior

    @clear_behavior.setter
    def clear_behavior(self, clear_behavior):
        if clear_behavior in ClearBehavior:
            self._clear_behavior = clear_behavior
        elif enum_contains(clear_behavior, ClearBehavior):
            self._clear_behavior = ClearBehavior(clear_behavior)
        else:
            raise ValueError()

    def to_json(self):
        return {
            'type': self.type,
            'clear_behavior': self.clear_behavior.value
        }


class StopDirective:
    def __init__(self):
        self.type = 'AudioPlayer.Stop'

    def _dict(self):
        return self.__dict__
