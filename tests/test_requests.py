from unittest import TestCase
from tests.mock_skill import *
from tests.mock_requests import *


class TestRequests(TestCase):
    def setUp(self):
        echokit.application_id = "amzn1.ask.skill.[unique-value-here]"
        echokit.verify_application_id = False
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
