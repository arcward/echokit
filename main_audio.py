import echokit
from echokit import Response, PlainTextOutputSpeech, SimpleCard
from echokit import audio_player
from echokit.directives import AudioPlayerDirective, PlayBehavior

# In the Lambda config, 'handler' would be
# set to ``order_skill.handler``
handler = echokit.handler

# Your skill ID, as provided in the Alexa dev portal
echokit.verify_application_id = False


@echokit.on_intent('AMAZON.ResumeIntent')
def resume_audio(request_wrapper):
    play_directive = AudioPlayerDirective.play(PlayBehavior.REPLACE_ALL,
                                               "https://some_url.com",
                                               "random_token", 0)
    return Response(directives=[play_directive], should_end_session=True)


@echokit.audio_player.playback_failed
def started_playback(request_wrapper):
    print(request_wrapper.request)
    print(request_wrapper.session)
    return Response(directives=[AudioPlayerDirective.stop()])


@echokit.audio_player.exception
def playback_exc(request_wrapper):
    print(request_wrapper.request)
    print(request_wrapper.session)


# This example is for an intent that handles a slot,
# showing how to access the intent's 'Order' slot.
# This would return output speech like: 'You asked me to jump'
# The session variable would be returned on the next invocation
@echokit.on_intent('OrderIntent')
def order_intent(request_wrapper):
    request = request_wrapper.request
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
def unimplemented(request_wrapper):
    request = request_wrapper.request
    output_speech = PlainTextOutputSpeech(f"Sorry, {request.intent.name} "
                                          f"isn't implemented!")
    return Response(output_speech=output_speech)

0
