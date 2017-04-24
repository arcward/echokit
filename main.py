import echokit
from echokit import Response, PlainTextOutputSpeech, SimpleCard
from echokit.audio_player import directives

# In the Lambda config, 'handler' would be
# set to ``order_skill.handler``
handler = echokit.handler

# Your skill ID, as provided in the Alexa dev portal
echokit.verify_application_id = False


@echokit.on_intent('AMAZON.ResumeIntent')
def resume_audio(request, session):
    stream = directives.Stream("https://url.com", "random_token", 0)
    play = directives.Play(directives.PlayBehavior.REPLACE_ALL, stream)
    return Response(directives=[play], should_end_session=True)


@echokit.playback_failed
def started_playback(request, session):
    print(request)
    print(session)
    return Response(directives=[directives.Stop()])


@echokit.playback_exception
def playback_exc(request, session):
    print(request)
    print(session)



# All apps are required to handle three basic requests,
# which have their own decorators:
# * LaunchRequest:          @echokit.on_session_launch
# * SessionEndedRequest:    @echokit.on_session_end
# * IntentRequest:          @echokit.on_intent('your_intent_name')

# Handles: LaunchRequest
@echokit.on_session_launch
def session_started(request, session):
    output_speech = PlainTextOutputSpeech("Welcome to Order Maker!")
    return Response(output_speech=output_speech)


# Handles: SessionEndedRequest
@echokit.on_session_end
def session_ended(request, session):
    output_speech = PlainTextOutputSpeech("See you later")
    return Response(output_speech=output_speech)


# Handles: IntentRequest
@echokit.on_intent('HoursIntent')
def hours_intent(request, session):
    output_speech = PlainTextOutputSpeech("We're open today from 5am to 8pm")
    return Response(output_speech=output_speech)


# Handles: IntentRequest
# This example is for an intent that handles a slot,
# showing how to access the intent's 'Order' slot.
# This would return output speech like: 'You asked me to jump'
# The session variable would be returned on the next invocation
@echokit.on_intent('OrderIntent')
def order_intent(request, session):
    menu_item = request.intent.slots['MenuItem'].value
    response_text = f'You ordered: {menu_item}'
    card = SimpleCard(title="Order", content=response_text)
    return Response(output_speech=PlainTextOutputSpeech(response_text),
                    session_attributes={'last_order': menu_item},
                    card=card)


# Handles: IntentRequest (unimplemented intent)
# For example, if 'WeaveBasketIntent' is defined in your
# interaction model, but you haven't defined a handler
# for it with @echokit.on_intent('WeaveBasketIntent'),
# this will catch it. If you don't define your own here,
# by default echokit will return a "Sorry, I didn't
# understand your request" speech response.
@echokit.fallback
def unimplemented(request, session):
    output_speech = PlainTextOutputSpeech(f"Sorry, {request.intent.name} "
                                          f"isn't implemented!")
    return Response(output_speech=output_speech)

0
