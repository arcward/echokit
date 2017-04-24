import logging
from echokit import requests
from echokit.requests import standard
from echokit.requests.models import Session, Context
from echokit.responses.models import Response, PlainTextOutputSpeech

logger = logging.getLogger(__name__)

request_handlers = {}


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

    version = event.get('version')

    context = event.get('context')
    if context:
        context = Context.from_json(context)

    session = event.get('session')
    if session:
        session = Session.from_json(session)

    handler_func = _get_handler(event['request'])
    request = requests.request_type_model(event['request'])
    if requests.is_audio_player(event['request']):
        return handler_func(request, context).to_json()
    else:
        return handler_func(request, session).to_json()


def fallback_default(request, session):
    """Default handler for valid intent names without handlers"""
    speech = PlainTextOutputSpeech("Sorry, I didn't understand your request")
    return Response(output_speech=speech)


def _get_handler(request):
    if requests.is_intent(request):
        func = request_handlers.get(request['intent']['name'],
                                    standard.fallback)
    else:
        func = request_handlers[request['type']]
    return func


def _in_enum(value, enum_container):
    return value in [e.value for e in enum_container]

# Decorators to register functions to handle requests. Ex:
#   @echokit.on_session_launch
#   def begin_session(request, session):
#       speech = echokit.PlainTextOutputSpeech("You started a new session!")
#       return echokit.Response(output_speech=speech)




