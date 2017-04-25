import echokit
from collections import namedtuple
from enum import Enum
from echokit.request_handler import handler_funcs

PLAYBACK_STARTED = 'AudioPlayer.PlaybackStarted'
PLAYBACK_FINISHED = 'AudioPlayer.PlaybackFinished'
PLAYBACK_STOPPED = 'AudioPlayer.PlaybackStopped'
PLAYBACK_NEARLY_FINISHED = 'AudioPlayer.PlaybackNearlyFinished'
PLAYBACK_FAILED = 'AudioPlayer.PlaybackFailed'
EXCEPTION_ENCOUNTERED = 'System.ExceptionEncountered'


Error = namedtuple('Error', 'type message')
Cause = namedtuple('Cause', 'request_id')
CurrentPlaybackState = namedtuple('CurrentPlaybackState',
                                  'token offset_in_milliseconds '
                                  'player_activity')


class PlayerActivity(Enum):
    IDLE = 'IDLE'
    PAUSED = 'PAUSED'
    PLAYING = 'PLAYING'
    BUFFER_UNDERRUN = 'BUFFER_UNDERRUN'
    FINISHED = 'FINISHED'
    STOPPED = 'STOPPED'


def _from_json(json_obj, cls):
    return cls(json_obj['requestId'], json_obj['timestamp'],
                     json_obj['token'], json_obj['offsetInMilliseconds'])
    # elif json_obj['type'] in error_types:
    #     error_model = error_types[json_obj['type']]
    #     return error_model.from_json(json_obj)


class AudioPlayerState:
    def __init__(self, token, offset_in_milliseconds, player_activity):
        self.token = token
        self.offset_in_milliseconds = offset_in_milliseconds
        self.player_activity = player_activity


class AudioPlayerRequest:
    def __init__(self, type, request_id, timestamp, token,
                 offset_in_milliseconds, locale):
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.token = token
        self.offset_in_milliseconds = offset_in_milliseconds
        self.locale = locale

    @staticmethod
    def _build(self, **kwargs):
        cls = type(self)
        return cls(**kwargs)


class PlaybackStartedRequest(AudioPlayerRequest):
    """Sent on AMAZON.ResumeIntent"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PlaybackFinishedRequest(AudioPlayerRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PlaybackStoppedRequest(AudioPlayerRequest):
    """Sent on AMAZON.PauseIntent"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PlaybackNearlyFinishedRequest(AudioPlayerRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PlaybackFailedRequest:
    def __init__(self, type, request_id, timestamp, token, locale, error,
                 current_playback_state):
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.token = token
        self.locale = locale
        self.error = error
        self.current_playback_state = current_playback_state

    @staticmethod
    def _build(**kwargs):
        kwargs['error'] = Error(**kwargs['error'])
        kwargs['current_playback_state'] = \
            CurrentPlaybackState(**kwargs['current_playback_state'])
        return PlaybackFailedRequest(**kwargs)

    @staticmethod
    def from_json(json_obj):
        error = Error(json_obj['error']['type'], json_obj['error']['message'])
        json_state = json_obj['currentPlaybackState']
        state = CurrentPlaybackState(json_state['token'],
                                     json_state['offsetInMilliseconds'],
                                     json_state['playerActivity'])
        return PlaybackFailedRequest(json_obj['requestId'], json_obj['timestamp'],
                              json_obj['token'], json_obj['locale'], error,
                              state)


class ExceptionEncountered:
    def __init__(self, type, request_id, timestamp, locale, error, cause):
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.error = error
        self.cause = cause

    @staticmethod
    def _build(**kwargs):
        kwargs['error'] = Error(**kwargs['error'])
        kwargs['cause'] = Cause(**kwargs['cause'])
        return ExceptionEncountered(**kwargs)

    @staticmethod
    def from_json(json_obj):
        error = Error(json_obj['error']['type'], json_obj['error']['message'])
        cause = Cause(json_obj['cause']['requestId'])
        return ExceptionEncountered(json_obj['requestId'],
                                    json_obj['timestamp'], json_obj['locale'],
                                    error, cause)


def playback_started(func):
    handler_funcs[PLAYBACK_STARTED] = func


def playback_finished(func):
    handler_funcs[PLAYBACK_FINISHED] = func


def playback_stopped(func):
    handler_funcs[PLAYBACK_STOPPED] = func


def playback_nearly_finished(func):
    handler_funcs[PLAYBACK_NEARLY_FINISHED] = func


def playback_failed(func):
    handler_funcs[PLAYBACK_FAILED] = func


def exception(func):
    handler_funcs[EXCEPTION_ENCOUNTERED] = func


class AudioPlayer:
    def __init__(self, token=None, offset_in_milliseconds=None,
                 player_activity=None):
        self.token = token
        self.offset_in_milliseconds = offset_in_milliseconds
        self.player_activity = player_activity
