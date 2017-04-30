"""Handles initial requests/logging"""
import logging
from echokit.request_handler import handler, on_session_launch, \
    on_session_end, on_intent, fallback
from echokit.responses import ask, tell


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#: Skill's application ID, found in the Alexa dev portal
application_id = None

#: If True, will verify app ID in each request (raising exceptions if needed)
verify_application_id = True12