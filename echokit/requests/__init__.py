from echokit.request_handler import handler_funcs
from echokit import audio_player
from echokit.requests.models import Error, Session, Context, Intent

LAUNCH = 'LaunchRequest'
SESSION_ENDED = 'SessionEndedRequest'
INTENT = 'IntentRequest'


class RequestWrapper:
    def __init__(self, request=None, session=None, context=None, version=None):
        self._request = None
        self._session = None
        self._context = None

        self.request = request
        self.session = session
        self.context = context
        self.version = version

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        if not request:
            self._request = request
            return
        self._request = RequestWrapper.__build_request(request)

    @staticmethod
    def __build_request(request):
        types = {**standard_models, **audio_models}
        model = types[request['type']]
        return model._build(**request)

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        if session:
            session = Session(**session)
        self._session = session

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        if context:
            context = Context._build(**context)
        self._context = context


class LaunchRequest:
    """Received when the user didn't provide a specific intent"""
    def __init__(self, type=None, request_id=None, timestamp=None,
                 locale=None):
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale

    @staticmethod
    def _build(**kwargs):
        return LaunchRequest(**kwargs)


class SessionEndedRequest:
    """Received upon user exit, lack of response, or error.

    Not received if the session is ended because you set the 
    ``should_end_session`` flag to ``True``
    """
    def __init__(self, type=None, request_id=None, timestamp=None,
                 locale=None, reason=None, error=None):
        """

        :param request_id: 
        :param timestamp: 
        :param locale: 
        :param reason: Describes reason for session end. Values: 
            ``USER_INITIATED``, ``ERROR``, ``EXCEEDED_MAX_REPROMPTS``
        :param error: ``Error`` object with more info on any error
        """
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.reason = reason
        self.error = error

    @staticmethod
    def _build(**kwargs):
        if 'error' in kwargs:
            kwargs['error'] = Error(**kwargs['error'])
        return SessionEndedRequest(**kwargs)


class IntentRequest:
    """Received when the user supplies an intent"""
    def __init__(self, type=None, request_id=None, timestamp=None,
                 locale=None, dialog_state=None, intent=None):
        """
        
        :param request_id: 
        :param timestamp: 
        :param locale: 
        :param dialog_state: Enumeration of status of multi-turn dialog. 
            Values: ``STARTED``, ``IN_PROGRESS``, ``COMPLETED``
        :param intent: ``Intent`` object
        """
        self.type = type
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.dialog_state = dialog_state
        self.intent = intent

    @staticmethod
    def _build(**kwargs):
        kwargs['intent'] = Intent._build(**kwargs['intent'])
        return IntentRequest(**kwargs)


standard_models = {
    LAUNCH: LaunchRequest,
    SESSION_ENDED: SessionEndedRequest,
    INTENT: IntentRequest
}

audio_models = {
    audio_player.PLAYBACK_STARTED: audio_player.PlaybackStartedRequest,
    audio_player.PLAYBACK_FINISHED: audio_player.PlaybackFinishedRequest,
    audio_player.PLAYBACK_STOPPED: audio_player.PlaybackStoppedRequest,
    audio_player.PLAYBACK_FAILED: audio_player.PlaybackFailedRequest,
    audio_player.EXCEPTION_ENCOUNTERED: audio_player.ExceptionEncountered,
    audio_player.PLAYBACK_NEARLY_FINISHED:
    audio_player.PlaybackNearlyFinishedRequest,

}


def on_session_launch(func):
    handler_funcs[LAUNCH] = func


def on_session_end(func):
    handler_funcs[SESSION_ENDED] = func


def on_intent(intent_name):
    def func_wrapper(func):
        handler_funcs[intent_name] = func
    return func_wrapper


def fallback(func):
    fallback_default = func
