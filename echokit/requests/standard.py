from echokit.requests.models import Error, Intent
from echokit.requests.handler import request_handlers

LAUNCH = 'LaunchRequest'
SESSION_ENDED = 'SessionEndedRequest'
INTENT = 'IntentRequest'


class LaunchRequest:
    """Received when the user didn't provide a specific intent"""
    def __init__(self, request_id, timestamp, locale):
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale

    @staticmethod
    def from_json(json_obj):
        launch_request = LaunchRequest(json_obj['requestId'],
                                       json_obj['timestamp'],
                                       json_obj['locale'])
        return launch_request


class SessionEndedRequest:
    """Received upon user exit, lack of response, or error.

    Not received if the session is ended because you set the 
    ``should_end_session`` flag to ``True``
    """
    def __init__(self, request_id, timestamp, locale, reason, error):
        """

        :param request_id: 
        :param timestamp: 
        :param locale: 
        :param reason: Describes reason for session end. Values: 
            ``USER_INITIATED``, ``ERROR``, ``EXCEEDED_MAX_REPROMPTS``
        :param error: ``Error`` object with more info on any error
        """
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.reason = reason
        self.error = error

    @staticmethod
    def from_json(json_obj):
        error = Error(json_obj.get('type'), json_obj.get('message'))
        end_request = SessionEndedRequest(json_obj['requestId'],
                                          json_obj['timestamp'],
                                          json_obj['locale'],
                                          json_obj.get('dialogState'),
                                          error)
        return end_request


class IntentRequest:
    """Received when the user supplies an intent"""
    def __init__(self, request_id, timestamp, locale, dialog_state, intent):
        """
        
        :param request_id: 
        :param timestamp: 
        :param locale: 
        :param dialog_state: Enumeration of status of multi-turn dialog. 
            Values: ``STARTED``, ``IN_PROGRESS``, ``COMPLETED``
        :param intent: ``Intent`` object
        """
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.dialog_state = dialog_state
        self.intent = intent

    @staticmethod
    def from_json(json_obj):
        intent_request = IntentRequest(json_obj['requestId'],
                                       json_obj['timestamp'],
                                       json_obj['locale'],
                                       json_obj.get('dialogState'),
                                       Intent.from_json(json_obj['intent']))
        return intent_request


models = {
    LAUNCH: LaunchRequest,
    SESSION_ENDED: SessionEndedRequest,
    INTENT: IntentRequest
}


def on_session_launch(func):
    request_handlers[LAUNCH] = func


def on_session_end(func):
    request_handlers[SESSION_ENDED] = func


def on_intent(intent_name):
    def func_wrapper(func):
        request_handlers[intent_name] = func
    return func_wrapper


def fallback(func):
    fallback_default = func
