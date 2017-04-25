"""AudioPlayer interface implementation
https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-audioplayer-interface-reference
"""
from enum import Enum
from echokit.request_handler import handler_funcs

PLAYBACK_STARTED = 'AudioPlayer.PlaybackStarted'
PLAYBACK_FINISHED = 'AudioPlayer.PlaybackFinished'
PLAYBACK_STOPPED = 'AudioPlayer.PlaybackStopped'
PLAYBACK_NEARLY_FINISHED = 'AudioPlayer.PlaybackNearlyFinished'
PLAYBACK_FAILED = 'AudioPlayer.PlaybackFailed'
EXCEPTION_ENCOUNTERED = 'System.ExceptionEncountered'


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


class Error:
    def __init__(self, type=None, message=None):
        self.type = type
        self.message = message


class Cause:
    def __init__(self, request_id=None):
        self.request_id = request_id


class CurrentPlaybackState:
    def __init__(self, token=None, offset_in_milliseconds=None,
                 player_activity=None):
        self.token = token
        self.offset_in_milliseconds = offset_in_milliseconds
        self.player_activity = player_activity


class PlayerActivity(Enum):
    IDLE = 'IDLE'
    PAUSED = 'PAUSED'
    PLAYING = 'PLAYING'
    BUFFER_UNDERRUN = 'BUFFER_UNDERRUN'
    FINISHED = 'FINISHED'
    STOPPED = 'STOPPED'


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

