from collections import namedtuple
import echokit
from echokit import Response, PlainTextOutputSpeech

Context = namedtuple('Context', 'log_stream_name log_group_name '
                                'aws_request_id memory_limit_in_mb')

mock_context = Context('log name', 'group name', 'req ID', '10mb')

start_session = {
  "session": {
    "new": True,
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
    "timestamp": "2016-10-27T18:21:44Z",
    "type": "LaunchRequest",
    "requestId": "amzn1.echo-api.request.[unique-value-here]"
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

end_session = {
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
    "timestamp": "2016-10-27T21:11:41Z",
    "reason": "USER_INITIATED",
    "type": "SessionEndedRequest",
    "requestId": "amzn1.echo-api.request.[unique-value-here]"
  },
  "context": {
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

base_intent = {
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
      "name": "BaseIntent"
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


def create_intent(intent_name, new=True, slots=None, attributes=None,
                  application_id=None):
    intent = dict(base_intent)
    intent['request']['intent']['name'] = intent_name
    intent['session']['new'] = new

    if attributes:
        intent['session']['attributes'] = attributes

    if slots:
        intent['request']['intent']['slots'] = slots

    if application_id:
        intent['session']['application']['applicationId'] = application_id
    return intent


@echokit.on_session_launch
def session_started(request, session):
    output_speech = PlainTextOutputSpeech("You started a new session!")
    return Response(output_speech=output_speech)


@echokit.on_session_end
def session_ended(request, session):
    print(request.reason)


@echokit.on_intent('SomeIntent')
def on_intent(request, session):
    output_speech = PlainTextOutputSpeech("I did something with SomeIntent!")
    return Response(output_speech=output_speech)


@echokit.on_intent('OrderIntent')
def specific_intent(request, session):
    order = request.intent.slots['Order'].value
    session_attrs = {'last_order': order}
    response_text = f'You asked me to {order}'
    card = echokit.StandardCard(
        title="Order",
        text=response_text,
        small_image_url="http://i.imgur.com/PytSZCG.png",
        large_image_url="http://i.imgur.com/PytSZCG.png"
    )
    return Response(output_speech=PlainTextOutputSpeech(response_text),
                    session_attributes=session_attrs, card=card)


@echokit.fallback
def unimplemented(request, session):
    intent_name = request.intent.name
    output_speech = PlainTextOutputSpeech(f"Sorry, {intent_name} isn't "
                                          f"implemented!")
    return Response(output_speech)