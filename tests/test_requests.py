from unittest import TestCase
from tests.mock_requests import *
import echokit

echokit.application_id = 'amzn1.ask.skill.[unique-value-here]'
echokit.verify_application_id = False


# Handles: LaunchRequest
@echokit.on_session_launch
def session_started(request_wrapper):
    return echokit.ask('Welcome to Order Maker! WATCHU WANT?')


# Handles: SessionEndedRequest
@echokit.on_session_ended
def session_ended(request_wrapper):
    print(request_wrapper.request.reason)


# Handles: IntentRequest
@echokit.on_intent('HoursIntent')
def hours_intent(request_wrapper):
    return echokit.tell("We're open 5AM to 8PM!") \
        .simple_card(title="Hours", content="5AM-8PM")


@echokit.on_intent('SanicIntent')
def sanic_intent(request_wrapper):
    return echokit.tell("Gotta go fast")\
        .standard_card(title="Sanic", text="Gotta go fast",
                       large_image_url="https://i.imgur.com/PytSZCG.png")


@echokit.on_intent('SsmlIntent')
def ssml_intent(request_wrapper):
    ssml = ("<speak>Onomatopoeia: "
            "<say-as interpret-as=\"spell-out\">onomatopoeia</say-as>."
            "</speak>")
    return echokit.tell(speech=ssml, ssml=True)


@echokit.on_intent('OrderIntent')
@echokit.slot('MenuItem', dest='menu_item')
def order_intent(request_wrapper, menu_item):
    print(menu_item)
    request = request_wrapper.request
    return echokit.tell(f"You just ordered {menu_item}")\
        .simple_card(title="Previous order", content=menu_item)


# @echokit.fallback
# def unimplemented(request_wrapper):
#     return echokit.ask(speech="What did you say?", reprompt="Hello?")


class TestRequests(TestCase):
    def setUp(self):
        self.basic_response_keys = ['version', 'response']
        self.sanic_intent = build_intent('SanicIntent')
        self.hours_intent = build_intent('HoursIntent')
        self.ssml_intent = build_intent('SsmlIntent')
        self.unknown_intent = build_intent('UnknownIntent')
        self.order_intent = build_intent('OrderIntent', slots=build_slot(
            'MenuItem', 'spaghetti'), new=False)

    def test_start_session(self):
        r = echokit.handler(LAUNCH_REQUEST, MockContext)
        self.assertDictEqual(r, Expected.SESSION_STARTED)

    def test_end_session(self):
        r = echokit.handler(SESSION_ENDED_REQUEST, MockContext)
        self.assertIsNone(r)

    def test_order_intent(self):
        r = echokit.handler(self.order_intent, MockContext)
        self.assertDictEqual(r, Expected.ORDER_INTENT)

    def test_ssml_intent(self):
        r = echokit.handler(self.ssml_intent, MockContext)
        self.assertDictEqual(r, Expected.SSML_INTENT)

    def test_unknown_intent(self):
        r = echokit.handler(self.unknown_intent, MockContext)
        self.assertDictEqual(r, Expected.FALLBACK_DEFAULT)

    def test_incorrect_app_id(self):
        echokit.application_id = 'asdf'
        echokit.verify_application_id = True
        self.assertRaises(ValueError, echokit.handler, event=LAUNCH_REQUEST,
                          context=MockContext)
        echokit.verify_application_id = False


class Expected:
    SESSION_STARTED = {
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Welcome to Order Maker! WATCHU WANT?"
            },
            "shouldEndSession": False,
        },
        "version": "1.0",
        "sessionAttributes": {}
    }
    HOURS_INTENT = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
              "type": "PlainText",
              "text": "We're open 5AM to 8PM!"
            },
            "card": {
              "content": "5AM-8PM",
              "title": "Hours",
              "type": "Simple"
            },
            "shouldEndSession": True
        },
        "sessionAttributes": {}
    }
    SSML_INTENT = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": ("<speak>Onomatopoeia: <say-as "
                         "interpret-as=\"spell-out\">onomatopoeia</say-as>."
                         "</speak>")
            },
            "shouldEndSession": True
        },
        "sessionAttributes": {}
    }
    SANIC_INTENT = {
      "version": "1.0",
      "response": {
        "outputSpeech": {
          "type": "PlainText",
          "text": "Gotta go fast"
        },
        "card": {
          "text": "Gotta go fast",
          "title": "Sanic",
          "image": {
            "largeImageUrl": "https://i.imgur.com/PytSZCG.png"
          },
          "type": "Standard"
        },
        "shouldEndSession": True
      },
      "sessionAttributes": {}
    }
    ORDER_INTENT = {
          "version": "1.0",
          "response": {
            "outputSpeech": {
              "type": "PlainText",
              "text": "You just ordered spaghetti"
            },
            "card": {
              "content": "spaghetti",
              "title": "Previous order",
              "type": "Simple"
            },
            "shouldEndSession": True
          },
          "sessionAttributes": {}
        }
    FALLBACK_DEFAULT = {
          "version": "1.0",
          "response": {
            "outputSpeech": {
              "type": "PlainText",
              "text": "I wasn't able to process your request"
            },
            "shouldEndSession": True
          },
          "sessionAttributes": {}
        }
