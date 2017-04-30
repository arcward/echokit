from collections import namedtuple
import echokit

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

resume_json = {
  "session": {
    "sessionId": "SessionId.d06789a8-a48e-450c-a4ef-f4e25b0bc351",
    "application": {
      "applicationId": "some_app_id"
    },
    "attributes": {},
    "user": {
      "userId": "some_userid"
    },
    "new": True
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.83810a3b-2b23-450b-bd00-ad31b45cc17c",
    "locale": "en-US",
    "timestamp": "2017-04-24T14:45:45Z",
    "intent": {
      "name": "AMAZON.ResumeIntent",
      "slots": {}
    }
  },
  "version": "1.0"
}

pause_json = {

  "session": {
    "sessionId": "SessionId.3cec3682-31b1-41e1-bb59-c9a0c2ddae6e",
    "application": {
      "applicationId": "amzn1.ask.skill.3c392942-8efb-48a1-89ff-05af9eaa9c5e"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AEZQUQ4CYZSKQRADTPB4FQBYX6EI4DSLHE3VAAEQX3PE33EEWZOPUJY46NFKC4PW77CYQ7DXQNZJND2ANCYBX7SU5AZ2XXSSHGIVQBWUKUZPTPR4PIFZHF2BCHKBWKIG5V7WNFQO4POJHJQXJZAGA7GBF452E4F3A2H5XV4RGSSJPG47UM72R7G2IDKZMZ2G42ZVQ5C5BDINIEY"
    },
    "new": True
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.d580a39d-f090-46ca-9f67-b12b98ab3f3c",
    "locale": "en-US",
    "timestamp": "2017-04-24T14:49:11Z",
    "intent": {
      "name": "AMAZON.PauseIntent",
      "slots": {}
    }
  },
  "version": "1.0"
}


playback_failed_json = {
  "version": "string",
  "context": {
    "System": {
      "application": {},
      "user": {},
      "device": {}
    }
  },
  "request": {
    "type": "AudioPlayer.PlaybackFailed",
    "requestId": "string",
    "timestamp": "string",
    "token": "string",
    "locale": "string",
    "error": {
      "type": "string",
      "message": "string"
    },
    "currentPlaybackState": {
      "token": "string",
      "offsetInMilliseconds": 0,
      "playerActivity": "string"
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


@echokit.on_intent('AudioPlayer.PlaybackFailed')
def playback_failed(request_wrapper):
    request = request_wrapper.request
    context = request_wrapper.context
    print(request)
    print(context)

@echokit.on_session_launch
def start_ses(request_wrapper):
    return echokit.tell('You started a new session!')


@echokit.on_intent('AMAZON.PauseIntent')
def pause_audio(request_wrapper):
    pass


@echokit.on_session_end
def session_ended(request_wrapper):
    print(request_wrapper.request.reason)


@echokit.on_intent('SomeIntent')
def on_intent(request_wrapper):
    return echokit.tell('I did something with SomeIntent!')


@echokit.on_intent('OrderIntent')
def specific_intent(request_wrapper):
    request = request_wrapper.request
    asdf = request.intent.slots
    order = request.intent.slots['Order']
    session_attrs = {'last_order': order}
    response_text = f'You asked me to {order}'
    img_url = "http://i.imgur.com/PytSZCG.png"

    return echokit.tell(response_text)\
        .standard_card("Order", response_text, img_url, img_url)\
        .session_attributes(session_attrs)


@echokit.fallback
def unimplemented(request_wrapper):
    request = request_wrapper.request
    intent_name = request.intent.name
    return echokit.tell(f"Sorry, {intent_name} isn't implemented!")