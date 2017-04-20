from echopy.request import Request
from echopy.response import Response, OutputSpeech, SimpleCard, \
    StandardCard, LinkAccountCard, Reprompt

__all__ = ['request', 'response']

application_id = None

request_handlers = {}


def handler(event, context):
    print(f"Log stream name: {context.log_stream_name}")
    print(f"Log group name: {context.log_group_name}")
    print(f"Request ID: {context.aws_request_id}")
    print(f"Mem. limits(MB): {context.memory_limit_in_mb}")

    event = Request.from_json(event)
    if event.request.request_type == 'IntentRequest':
        resp = request_handlers.get(event.request.intent.name)
    else:
        resp = request_handlers.get(event.request.request_type)

    return resp(event).to_json()


def on_session_launch(func):
    request_handlers['LaunchRequest'] = func


def on_intent(intent_name):
    def func_wrapper(func):
        request_handlers[intent_name] = func
    return func_wrapper


def on_session_end(func):
    request_handlers['SessionEndedRequest'] = func



