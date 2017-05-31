"""Handles initial requests/logging"""
from echokit.models import _ASKObject, ASKResponse
from echokit.responses import ask, tell
from echokit.handlers import (handler, on_intent, on_session_launch,
                              on_session_ended, fallback, slot)
#: Skill's application ID, found in the Alexa dev portal
application_id = None

#: If True, will verify app ID in each request (raising exceptions if needed)
verify_application_id = True


