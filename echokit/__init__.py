"""Handles initial requests/logging"""
from echokit.handler import handler, on_session_launch, \
    on_session_ended, on_intent, fallback, slot
from echokit.models import ASKResponse

#: Skill's application ID, found in the Alexa dev portal
application_id = None

#: If True, will verify app ID in each request (raising exceptions if needed)
verify_application_id = True


def ask(speech, reprompt=None, ssml=False, session_attributes=None):
    """Ask the user a question, leaving the session open
    
    :param speech: Question text
    :param reprompt: Reprompt text
    :param ssml: True if speech/reprompts are in SSML format, 
        False if plaintext (default: False) 
    :param session_attributes: dict of session attributes to set
    :return: ``ASKResponse`` object
    """
    response = ASKResponse(should_end_session=False,
                           session_attributes=session_attributes)\
        .speech(speech, ssml)
    if reprompt:
        response = response.reprompt(speech, ssml)
    return response


def tell(speech, ssml=False):
    """Tell the user something and end the session
    
    :param speech: Statement text
    :param ssml: True if speech is in SSML format, 
        False if speech is plaintext (default: False) 
    :return: ``ASKResponse`` object
    """
    return ASKResponse(should_end_session=True).speech(speech, ssml)
