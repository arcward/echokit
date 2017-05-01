"""Handlers for requests/assigning intent handlers"""
# noinspection PyProtectedMember
from echokit.models import _ASKObject, ASKResponse

__handler_funcs = {}


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
    handler_func = __get_handler(ask_request.request)
    response = handler_func(ask_request)
    # Won't always receive responses (ex: SessionEndedRequest)
    if response:
        response_dict = response._dict()
        return response_dict


_LAUNCH_REQUEST = 'LaunchRequest'
_SESSION_ENDED_REQUEST = 'SessionEndedRequest'
_INTENT_REQUEST = 'IntentRequest'


def __get_handler(request):
    """Gets the handler function for a request type/intent name"""
    if request.type == _INTENT_REQUEST:
        func = __handler_funcs.get(request.intent.name)
    else:
        func = __handler_funcs.get(request.type)

    if not func:
        func = __handler_funcs.get('fallback', __fallback_default)
    return func


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


def slot(name):
    def slot_checker(func):
        def handler_func(request_wrapper):
            s = request_wrapper.request.intent.slots[name]
            # if s.value not in values:
            #     raise ValueError(f"Unexpected value for '{name}'. "
            #                      f"Received: '{s.value}'. "
            #                      f"Expected: {values}")
            return func(request_wrapper, s.value)
        return handler_func
    return slot_checker


def fallback(func):
    """Unhandled IntentRequest decorator"""
    __handler_funcs['fallback'] = func


def __fallback_default(request_wrapper):
    if request_wrapper.request.type == _INTENT_REQUEST:
        print(f"WARNING: Unhandled intent: "
              f"{request_wrapper.request.intent.name}")
    else:
        print(f"WARNING: No handler found for {request_wrapper.request.type}")
    return ASKResponse(should_end_session=True)\
        .speech("I wasn't able to process your request")
