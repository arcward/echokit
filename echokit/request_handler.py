import logging
from echokit._utils import convert_keys, revert_keys
from echokit.constants import INTENT_REQUEST, LAUNCH_REQUEST, \
    SESSION_ENDED_REQUEST
from echokit.models import ASKObject
from echokit.responses import tell


logger = logging.getLogger(__name__)


handler_funcs = {}


def handler(event, context):
    """Lambda service calls this method when sending us a request

    :param event: Contains data on the Alexa request, used to 
        create ``echokit.request.RequestWrapper``
    :param context: RequestWrapper context, used primarily for logging. 
        **Note**: *Not* the same as ``echokit.request.Context``
    :return: Dict of ``echokit.response.ResponseWrapper`` object
    """
    logger.info(f"Received event: {event}")
    logger.info(f"Log stream name: {context.log_stream_name}")
    logger.info(f"Log group name: {context.log_group_name}")
    logger.info(f"RequestWrapper ID: {context.aws_request_id}")
    logger.info(f"Mem. limits(MB): {context.memory_limit_in_mb}")

    ask_request = ASKObject(**event)
    handler_func = _get_handler(ask_request.request)
    response = handler_func(ask_request)
    # Won't always receive responses (ex: SessionEndedRequest)
    if response is not None:
        response_dict = response._dict()
        return response_dict


def fallback_default(request_wrapper):
    """Default handler for valid intent names without handlers"""
    return tell("Sorry, I didn't understand your request")


def _get_handler(request):
    if request.type == INTENT_REQUEST:
        func = handler_funcs.get(request.intent.name, fallback_default)
    else:
        func = handler_funcs[request.type]
    return func


def on_session_launch(func):
    handler_funcs[LAUNCH_REQUEST] = func


def on_session_end(func):
    handler_funcs[SESSION_ENDED_REQUEST] = func


def on_intent(intent_name):
    def func_wrapper(func):
        handler_funcs[intent_name] = func
    return func_wrapper


def fallback(func):
    fallback_default = func
