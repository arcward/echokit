"""Handles initial requests/logging"""
import logging
from echokit.request_models import RequestWrapper
from echokit.response_models import Response, \
    PlainTextOutputSpeech, SSMLOutputSpeech, SimpleCard, StandardCard, \
    LinkAccountCard, Reprompt


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#: Skill's application ID, found in the Alexa dev portal
application_id = None

#: If True, will verify app ID in each request (raising exceptions if needed)
verify_application_id = True


def fallback_default(request, session):
    """Default handler for valid intent names without handlers"""
    speech = PlainTextOutputSpeech("Sorry, I didn't understand your request")
    return Response(output_speech=speech)

request_handlers = {'fallback': fallback_default}


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

    event = RequestWrapper.from_json(event)
    request = event.request
    session = event.session

    if request.request_type == 'IntentRequest':
        logger.info(f"Received intent: {request.intent.name}")
        # Recognized intent name and handler function
        if request.intent.name in request_handlers:
            resp = request_handlers.get(request.intent.name)
        #: Recognized intent name, but no handler function
        else:
            logger.debug(f"Unexpected intent '{request.intent.name}', "
                         f"falling back")
            resp = request_handlers.get('fallback')
    else:
        # Other requests are LaunchRequest and SessionEndedRequest
        resp = request_handlers.get(request.request_type)

    # Final return to Alexa service
    resp_json = resp(request, session).to_json()
    logger.info(f"Response: {resp_json}")
    return resp_json


# Decorators to register functions to handle requests. Ex:
#   @echokit.on_session_launch
#   def begin_session(request, session):
#       speech = echokit.PlainTextOutputSpeech("You started a new session!")
#       return echokit.Response(output_speech=speech)
def on_session_launch(func):
    request_handlers['LaunchRequest'] = func


def on_session_end(func):
    request_handlers['SessionEndedRequest'] = func


def on_intent(intent_name):
    def func_wrapper(func):
        request_handlers[intent_name] = func
    return func_wrapper


def fallback(func):
    request_handlers['fallback'] = func

__all__ = ['request_models', 'response_models']
