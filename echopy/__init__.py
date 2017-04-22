"""Handles initial requests/logging"""
import logging
from echopy.request_models import RequestWrapper
from echopy.response_models import Response, \
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
    return ResponseWrapper(output_speech=speech)

request_handlers = {'fallback': fallback_default}


def handler(event, context):
    """Lambda service calls this method when sending us a request
    
    :param event: Contains data on the Alexa request, used to 
        create ``echopy.request.RequestWrapper``
    :param context: RequestWrapper context, used primarily for logging. **Note**: 
        *Not* the same as ``echopy.request.Context``
    :return: Dict of ``echopy.response.ResponseWrapper`` object
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
        intent_name = request.intent.name
        logger.info(f"Received intent: {intent_name}")
        # Recognized intent name and handler function
        if intent_name in request_handlers:
            resp = request_handlers.get(intent_name)
        #: Recognized intent name, but no handler function
        else:
            logger.info(f"Unexpected intent '{intent_name}', falling back")
            resp = request_handlers.get('fallback')
    else:
        # Other requests are LaunchRequest and SessionEndedRequest
        resp = request_handlers.get(request.request_type)
    resp_json = resp(request, session).to_json()
    logger.info(f"ResponseWrapper: {resp_json}")
    return resp_json


# Decorators to register functions to handle requests. Ex:
#   @echopy.on_session_launch
#   def begin_session(event):
#       output_speech = echopy.OutputSpeech(text="You started a new session!")
#       return echopy.ResponseWrapper(output_speech=output_speech)

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

__all__ = ['request', 'response']
