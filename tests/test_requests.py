from unittest import TestCase
from tests.alexa_structs import *


class TestRequests(TestCase):
    def setUp(self):
        echokit.application_id = "amzn1.ask.skill.[unique-value-here]"
        echokit.verify_application_id = False
        self.basic_response_keys = ['version', 'response']

    def test_start_session(self):
        r = echokit.handler(start_session, mock_context)
        expected_speech = {'type': 'PlainText',
                           'text': 'You started a new session!'}
        self.assertDictEqual(expected_speech, r['response']['outputSpeech'])

    def test_end_session(self):
        r = echokit.handler(end_session, mock_context)
        expected_speech = {'type': 'PlainText',
                           'text': 'You ended our session :['}
        self.assertDictEqual(expected_speech, r['response']['outputSpeech'])

    def test_order_intent(self):
        order_intent = create_intent('OrderIntent', new=False,
                                     slots={"Order": {"name": "Order",
                                                      "value": "jump"}})
        r = echokit.handler(order_intent, mock_context)
        print(r)
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

        for ek in self.basic_response_keys:
            self.assertIn(ek, r.keys())

        self.assertEqual(r['version'], '1.0')

        expected_speech = {'type': 'PlainText',
                           'text': "I did something with SomeIntent!"}
        self.assertDictEqual(expected_speech, r['response']['outputSpeech'])

    def test_fallback_intent(self):
        weird_intent = create_intent('WeirdIntent', new=True)
        r = echokit.handler(weird_intent, mock_context)

        for ek in self.basic_response_keys:
            self.assertIn(ek, r.keys())

        self.assertEqual(r['version'], '1.0')

        expected_speech = {'type': 'PlainText',
                           'text': "Sorry, WeirdIntent isn't implemented!"}
        self.assertEqual(expected_speech, r['response']['outputSpeech'])

    def test_play_directive(self):
        r = echokit.handler(resume_json, mock_context)
        print(r)

