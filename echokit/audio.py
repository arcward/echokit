"""AudioPlayer interface implementation
https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-audioplayer-interface-reference
"""
from echokit.request_handler import handler_funcs
from echokit.constants import PLAYBACK_STARTED, PLAYBACK_FAILED, \
    PLAYBACK_FINISHED, PLAYBACK_NEARLY_FINISHED, PLAYBACK_STOPPED, \
    EXCEPTION_ENCOUNTERED


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

