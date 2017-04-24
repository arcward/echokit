from collections import namedtuple
from enum import Enum
import echokit

AudioItem = namedtuple('AudioItem', 'stream')


class Stream:
    def __init__(self, url, token, offset_in_milliseconds,
                 expected_previous_token=None):
        self.token = token
        self.url = url
        self.offset_in_milliseconds = offset_in_milliseconds
        self.expected_previous_token = expected_previous_token

    def to_json(self):
        stream_dict = {
            'token': self.token,
            'url': self.url,
            'offsetInMilliseconds': self.offset_in_milliseconds
        }
        if self.expected_previous_token:
            stream_dict['expectedPreviousToken'] = self.expected_previous_token

        return stream_dict


class PlayBehavior(Enum):
    ENQUEUE = 'ENQUEUE'
    REPLACE_ALL = 'REPLACE_ALL'
    REPLACE_ENQUEUED = 'REPLACE_ENQUEUED'


class ClearBehavior(Enum):
    CLEAR_ALL = 'CLEAR_ALL'
    CLEAR_ENQUEUED = 'CLEAR_ENQUEUED'


class AudioPlayerDirective:
    @staticmethod
    def play(play_behavior, url, token, offset_in_milliseconds,
             expected_previous_token=None):
        stream = Stream(url, token, offset_in_milliseconds,
                        expected_previous_token)
        return _Play(play_behavior, AudioItem(stream))

    @staticmethod
    def stop():
        return _Stop()

    @staticmethod
    def clear_queue(clear_behavior):
        return _ClearQueue(clear_behavior)


class _Play:
    Behavior = Enum('PlayBehavior', [
        (a, a) for a in ('ENQUEUE', 'REPLACE_ALL', 'REPLACE_ENQUEUED')
    ])

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
        elif echokit._in_enum(play_behavior, PlayBehavior):
            self._play_behavior = PlayBehavior(play_behavior)
        else:
            raise ValueError()

    def to_json(self):
        return {
            'type': self.type,
            'playBehavior': self.play_behavior.value,
            'audioItem': self.audio_item.stream.to_json()
        }


class _Stop:
    def __init__(self):
        self.type = 'AudioPlayer.Stop'

    def to_json(self):
        return {'type': self.type}


class _ClearQueue:
    Behavior = Enum('ClearBehavior', [(a, a) for a in
                                      ('CLEAR_ALL', 'CLEAR_ENQUEUED')])

    def __init__(self, clear_behavior):
        self.type = 'AudioPlayer.ClearQueue'
        self._clear_behavior = None
        self.clear_behavior = clear_behavior

    @property
    def clear_behavior(self):
        return self._clear_behavior

    @clear_behavior.setter
    def clear_behavior(self, clear_behavior):
        if clear_behavior in ClearQueue.Behavior:
            self._clear_behavior = clear_behavior
        elif echokit._in_enum(clear_behavior, ClearQueue.Behavior):
            self._clear_behavior = ClearQueue.Behavior(clear_behavior)
        else:
            raise ValueError()

    def to_json(self):
        return {
            'type': self.type,
            'clearBehavior': self.clear_behavior.value
        }

