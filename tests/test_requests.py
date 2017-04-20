from collections import namedtuple
from unittest import TestCase
import json
import echopy
from echopy import request, response

echopy.application_id = "amzn1.ask.skill.[unique-value-here]"

request_body = {
  "session": {
    "new": False,
    "sessionId": "amzn1.echo-api.session.[unique-value-here]",
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.[unique-value-here]"
    },
    "application": {
      "applicationId": "amzn1.ask.skill.[unique-value-here]"
    }
  },
  "version": "1.0",
  "request": {
    "locale": "en-US",
    "timestamp": "2016-10-27T21:06:28Z",
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.[unique-value-here]",
    "intent": {
      "slots": {},
      "name": "SomeIntent"
    }
  },
  "context": {
    "AudioPlayer": {
      "playerActivity": "IDLE"
    },
    "System": {
      "device": {
        "supportedInterfaces": {
          "AudioPlayer": {}
        }
      },
      "application": {
        "applicationId": "amzn1.ask.skill.[unique-value-here]"
      },
      "user": {
        "userId": "amzn1.ask.account.[unique-value-here]"
      }
    }
  }
}
context = namedtuple('Context', 'log_stream_name log_group_name '
                                'aws_request_id memory_limit_in_mb')

fake_context = context('log name', 'group name', 'req ID', '10mb')


@echopy.on_session_launch
def session_started(event):
    output_speech = response.OutputSpeech(text="Woo!")
    return response.Response(output_speech=output_speech)


@echopy.on_intent('SomeIntent')
def on_intent(event):
    output_speech = response.OutputSpeech(text="Intent woo!")
    return response.Response(output_speech=output_speech)


class TestRequests(TestCase):
    def setUp(self):
        self.json_str = json.dumps(request_body)
        self.json_dict = json.loads(self.json_str)

    def test_handler(self):
        r = echopy.handler(self.json_dict, fake_context)
        print(r)


