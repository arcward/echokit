from collections import namedtuple
from unittest import TestCase
import echopy
from echopy.response import Response, OutputSpeech


order_intent = {
  "session": {
    "sessionId": "SessionId.a904e546-3b90-43d1-8580-d52da46d8927",
    "application": {
      "applicationId": "amzn1.ask.skill.[unique-value-here]"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.[unique-value-here]"
    },
    "new": False
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.c10f9d6a-3043-4b24-9356-dc4fb4a8e1fb",
    "locale": "en-US",
    "timestamp": "2017-04-21T18:38:14Z",
    "intent": {
      "name": "SpecificIntent",
      "slots": {
        "Order": {
          "name": "Order",
          "value": "jump"
        }
      }
    }
  },
  "version": "1.0"
}

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

specific_json = {
  "session": {
    "sessionId": "SessionId.002ea470-a416-408c-ac1e-7bfed95fe882",
    "application": {
      "applicationId": "amzn1.ask.skill.[unique-value-here]"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.[unique-value-here]"
    },
    "new": True
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.f8b24f3e-74a9-4a03-bfd2-1f669decbf50",
    "locale": "en-US",
    "timestamp": "2017-04-20T16:38:10Z",
    "intent": {
      "name": "SpecificIntent",
      "slots": {
        "Order": {
          "name": "Order",
          "value": "jump"
        }
      }
    }
  },
  "version": "1.0"
}

weird_intent = {
  "session": {
    "sessionId": "SessionId.cdf5f865-83ac-408c-a40c-73c6523bd960",
    "application": {
      "applicationId": "amzn1.ask.skill.[unique-value-here]"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.[unique-value-here]"
    },
    "new": True
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.a76e2587-6ad9-4b95-a66d-e53e9755a10a",
    "locale": "en-US",
    "timestamp": "2017-04-21T19:02:58Z",
    "intent": {
      "name": "WeirdIntent",
      "slots": {}
    }
  },
  "version": "1.0"
}
context = namedtuple('Context', 'log_stream_name log_group_name '
                                'aws_request_id memory_limit_in_mb')

fake_context = context('log name', 'group name', 'req ID', '10mb')


@echopy.on_session_launch
def session_started(event):
    output_speech = OutputSpeech(text="Woo!")
    return Response(output_speech=output_speech)


@echopy.on_intent('SomeIntent')
def on_intent(event):
    output_speech = OutputSpeech(text="Intent woo!")
    return Response(output_speech=output_speech)


@echopy.on_intent('SpecificIntent')
def specific_intent(event):
    response_text = (f"You asked me to "
                     f"{event.request.intent.slots['Order'].value}")
    return Response(output_speech=OutputSpeech(text=response_text))


class TestRequests(TestCase):
    def setUp(self):
        echopy.application_id = "amzn1.ask.skill.[unique-value-here]"

    def test_handler(self):
        r = echopy.handler(request_body, fake_context)
        print(r)

    def test_specific_intent(self):
        r = echopy.handler(order_intent, fake_context)
        print(r)

    def test_fallback_inten(self):
        r = echopy.handler(weird_intent, fake_context)
        print(r)


