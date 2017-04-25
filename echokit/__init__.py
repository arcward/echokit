"""Handles initial requests/logging"""
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#: Skill's application ID, found in the Alexa dev portal
application_id = None

#: If True, will verify app ID in each request (raising exceptions if needed)
verify_application_id = True

from echokit.request_handler import handler
from echokit.requests import on_session_launch, on_session_end, \
    on_intent, fallback
from echokit.responses import Response
from echokit.speech import PlainTextOutputSpeech
from echokit.cards import SimpleCard, StandardCard, LinkAccountCard