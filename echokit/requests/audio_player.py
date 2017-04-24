import echokit
from collections import namedtuple
# from echokit import Context
from enum import Enum


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


class AudioPlayer:
    def __init__(self, type, request_id, timestamp, token,
                 offset_in_milliseconds, locale):
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.token = token
        self.offset_in_milliseconds = offset_in_milliseconds
        self.locale = locale


class PlaybackStarted(AudioPlayer):
    """Sent on AMAZON.ResumeIntent"""
    def __init__(self, request_id, timestamp, token, offset_in_milliseconds,
                 locale):
        super().__init__('AudioPlayer.PlaybackStarted', request_id,
                         timestamp, token, offset_in_milliseconds, locale)

    @staticmethod
    def from_json(json_obj):
        return _from_json(json_obj, PlaybackStarted)


class PlaybackFinished(AudioPlayer):
    def __init__(self, request_id, timestamp, token, offset_in_milliseconds,
                 locale):
        super().__init__('AudioPlayer.PlaybackFinished', request_id,
                         timestamp, token, offset_in_milliseconds, locale)

    @staticmethod
    def from_json(json_obj):
        return _from_json(json_obj, PlaybackFinished)


class PlaybackStopped(AudioPlayer):
    """Sent on AMAZON.PauseIntent"""
    def __init__(self, request_id, timestamp, token, offset_in_milliseconds,
                 locale):
        super().__init__('AudioPlayer.PauseIntent', request_id,
                         timestamp, token, offset_in_milliseconds, locale)

    @staticmethod
    def from_json(json_obj):
        return _from_json(json_obj, PlaybackStopped)


class PlaybackNearlyFinished(AudioPlayer):
    def __init__(self, request_id, timestamp, token, offset_in_milliseconds,
                 locale):
        super().__init__('AudioPlayer.PlaybackNearlyFinished', request_id,
                         timestamp, token, offset_in_milliseconds, locale)

    @staticmethod
    def from_json(json_obj):
        return _from_json(json_obj, PlaybackNearlyFinished)


class PlaybackFailed:
    def __init__(self, request_id, timestamp, token, locale, error,
                 current_playback_state):
        self.request_id = request_id
        self.timestamp = timestamp
        self.token = token
        self.locale = locale
        self.error = error
        self.current_playback_state = current_playback_state

    @staticmethod
    def from_json(json_obj):
        error = Error(json_obj['error']['type'], json_obj['error']['message'])
        json_state = json_obj['currentPlaybackState']
        state = CurrentPlaybackState(json_state['token'],
                                     json_state['offsetInMilliseconds'],
                                     json_state['playerActivity'])
        return PlaybackFailed(json_obj['requestId'], json_obj['timestamp'],
                              json_obj['token'], json_obj['locale'], error,
                              state)


class ExceptionEncountered:
    def __init__(self, request_id, timestamp, locale, error, cause):
        self.type = 'System.ExceptionEncountered'
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.error = error
        self.cause = cause

    @staticmethod
    def from_json(json_obj):
        error = Error(json_obj['error']['type'], json_obj['error']['message'])
        cause = Cause(json_obj['cause']['requestId'])
        return ExceptionEncountered(json_obj['requestId'],
                                    json_obj['timestamp'], json_obj['locale'],
                                    error, cause)


models = {
    PLAYBACK_STARTED: PlaybackStarted,
    PLAYBACK_FINISHED: PlaybackFinished,
    PLAYBACK_STOPPED: PlaybackStopped,
    PLAYBACK_NEARLY_FINISHED: PlaybackNearlyFinished,
    PLAYBACK_FAILED: PlaybackFailed,
    EXCEPTION_ENCOUNTERED: ExceptionEncountered
}


def playback_started(func):
    echokit.request_handlers[PLAYBACK_STARTED] = func


def playback_finished(func):
    echokit.request_handlers[PLAYBACK_FINISHED] = func


def playback_stopped(func):
    echokit.request_handlers[PLAYBACK_STOPPED] = func


def playback_nearly_finished(func):
    echokit.request_handlers[PLAYBACK_NEARLY_FINISHED] = func


def playback_failed(func):
    echokit.request_handlers[PLAYBACK_FAILED] = func


def exception_encountered(func):
    echokit.request_handlers[EXCEPTION_ENCOUNTERED] = func

