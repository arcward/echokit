from unittest import TestCase
from tests.mock_requests import SESSION_ENDED_REQUEST, LAUNCH_REQUEST
from tests.mock_skill import *


class TestRequests(TestCase):
    def setUp(self):
        echokit.application_id = "amzn1.ask.skill.[unique-value-here]"
        echokit.verify_application_id = False
        self.basic_response_keys = ['version', 'response']

    def test_start_session(self):
        r = echokit.handler(LAUNCH_REQUEST, mock_context)
        expected_speech = {'type': 'PlainText',
                           'text': 'You started a new session!'}
        self.assertDictEqual(expected_speech, r['response']['outputSpeech'])

    def test_end_session(self):
        self.assertIsNone(echokit.handler(SESSION_ENDED_REQUEST, mock_context))

    def test_order_intent(self):
        order_intent = create_intent('OrderIntent', new=False,
                                     slots={"Order": {"name": "Order",
                                                      "value": "jump"}})
        r = echokit.handler(order_intent, mock_context)
        for ek in self.basic_response_keys:
            self.assertIn(ek, r.keys())
        self.assertEqual(r['version'], '1.0')

        expected_attrs = {'last_order': 'jump'}
        self.assertDictEqual(expected_attrs, r['sessionAttributes'])

        expected_speech = {'type': 'PlainText', 'text': 'You asked me to jump'}
        self.assertDictEqual(expected_speech, r['response']['outputSpeech'])

        expected_card = {'type': 'Standard',
                         'title': 'Order',
                         'text': 'You asked me to jump',
                         'image': {
                             'smallImageUrl': 'http://i.imgur.com/PytSZCG.png',
                             'largeImageUrl': 'http://i.imgur.com/PytSZCG.png'
                         }}
        self.assertDictEqual(expected_card, r['response']['card'])

    def test_some_intent(self):
        some_intent = create_intent('SomeIntent', new=False)
        r = echokit.handler(some_intent, mock_context)
        self.assertEqual(r['version'], '1.0')

        for ek in self.basic_response_keys:
            self.assertIn(ek, r.keys())

        expected_speech = {'type': 'PlainText',
                           'text': "I did something with SomeIntent!"}
        self.assertDictEqual(expected_speech, r['response']['outputSpeech'])


class Expected:
    SESSION_STARTED = {
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Welcome to Order Maker! WATCHU WANT?"
            },
            "reprompt": None,
            "card": None,
            "shouldEndSession": False,
            "directives": []
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