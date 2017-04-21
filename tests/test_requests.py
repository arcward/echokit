from collections import namedtuple
from unittest import TestCase
import json
import echopy
from echopy.response import Response, OutputSpeech


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
      "userId": "amzn1.ask.account.AHZEHE57VH24IGDQSDWNBGJCNLXIKQWUOHENCOWOUGCWSDXTR4UAZYSNELZ6LAQTQC5BAUJRP33YQTZ75G3CC7LLWIPPXAOUWZLL3S5R3CQZDLJQXU5HLRGBUGCELDEJCUZVA74NHYKC3ZRFPGGVDXOUHCQOXE5O4TPRDAGH74CC67YDXU62OL5KVJCLQGK27GKD2NEZSC3UTII"
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
        r = echopy.handler(specific_json, fake_context)
        print(r)


