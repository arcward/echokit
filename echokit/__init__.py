"""Handles initial requests/logging"""
# noinspection PyProtectedMember
from echokit.models import _ASKObject, ASKResponse

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


# Handlers for requests/assigning intent handlers
__handler_funcs = {}
_LAUNCH_REQUEST = 'LaunchRequest'
_SESSION_ENDED_REQUEST = 'SessionEndedRequest'
_INTENT_REQUEST = 'IntentRequest'


# noinspection PyProtectedMember
def handler(event, context):
    """Lambda service calls this method when sending us a request

    :param event: Contains data on the Alexa request, used to 
        create ``echokit.request.RequestWrapper``
    :param context: RequestWrapper context, used primarily for logging. 
        **Note**: *Not* the same as ``echokit.request.Context``
    :return: Dict of ``echokit.response.ResponseWrapper`` object
    """
    print(f"Log stream: {context.log_stream_name}\n"
          f"Log group: {context.log_group_name}\n"
          f"Request ID: {context.aws_request_id}\n"
          f"Mem limits(MB): {context.memory_limit_in_mb}\n"
          f"Event received: {event}")
    ask_request = _ASKObject(**event)
    if (verify_application_id and
            ask_request.request.requestId != application_id):
        raise ValueError(f"App ID expected: '{application_id}' "
                         f"App ID received: {ask_request.request.requestId}")
    handler_func = __get_handler(ask_request.request)
    response = handler_func(ask_request)
    # Won't always receive responses (ex: SessionEndedRequest)
    if response:
        response_dict = response._dict()
        return response_dict


def __get_handler(request):
    """Gets the handler function for a request type/intent name"""
    if request.type == _INTENT_REQUEST:
        func = __handler_funcs.get(request.intent.name)
    else:
        func = __handler_funcs.get(request.type)
    if not func:
        func = __handler_funcs.get('fallback', __fallback_default)
    return func


# Decorators

def on_session_launch(func):
    """LaunchRequest decorator"""
    __handler_funcs[_LAUNCH_REQUEST] = func


def on_session_ended(func):
    """SessionEndedRequest decorator"""
    __handler_funcs[_SESSION_ENDED_REQUEST] = func


def on_intent(intent_name):
    """IntentRequest decorator"""

    def func_wrapper(func):
        __handler_funcs[intent_name] = func

    return func_wrapper


def slot(name, dest=None):
    """Slot wrapper

    :param name: Slot name. Will be passed to the handler as a keyword 
        argument unless specified in dest
    :param dest: Pass the slot value as a keyword parameter matching this name
    :return: 
    """

    def slot_checker(func):
        def handler_func(request_wrapper):
            s = request_wrapper.request.intent.slots[name]
            kw = {s.name: s.value}
            if dest:
                kw = {dest: s.value}
            return func(request_wrapper, **kw)

        return handler_func

    return slot_checker


def fallback(func):
    """Unhandled IntentRequest decorator"""
    __handler_funcs['fallback'] = func


def __fallback_default(request_wrapper):
    """Default @echokit.fallback handler if one isn't otherwise specified"""
    if request_wrapper.request.type == _INTENT_REQUEST:
        print(f"WARNING: Unhandled intent: "
              f"{request_wrapper.request.intent.name}")
    else:
        print(f"WARNING: No handler found for {request_wrapper.request.type}")
    return ASKResponse(should_end_session=True) \
        .speech("I wasn't able to process your request")
