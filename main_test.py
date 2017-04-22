import echopy
from echopy import Response, PlainTextOutputSpeech


# In the lambda console, you would set your
# handler to: ``example_main.handler``
def handler(event, context):
    return echopy.handler(event, context)

# Your skill ID, as provided in the Alexa dev portal
echopy.application_id = "your_key_here"


# All apps are required to handle three basic requests,
# which have their own decorators:
# * LaunchRequest:          @echopy.on_session_launch
# * SessionEndedRequest:    @echopy.on_session_end
# * IntentRequest:          @echopy.on_intent('your_intent_name')

# Handles: LaunchRequest
@echopy.on_session_launch
def session_started(request, session):
    output_speech = PlainTextOutputSpeech("You started a new session!")
    return Response(output_speech=output_speech)


# Handles: SessionEndedRequest
@echopy.on_session_end
def session_ended(request, session):
    output_speech = PlainTextOutputSpeech("You ended our session :[")
    return Response(output_speech=output_speech)


# Handles: IntentRequest
@echopy.on_intent('HoursIntent')
def on_intent(request, session):
    output_speech = PlainTextOutputSpeech("We're open 8am to 6pm")
    return Response(output_speech=output_speech)


# Handles: IntentRequest
# This example is for an intent that handles a slot,
# showing how to access the intent's 'Order' slot.
# This would return output speech like: 'You asked me to jump'
# The session variable would be returned on the next invocation
@echopy.on_intent('OrderIntent')
def specific_intent(request, session):
    menu_item = request.intent.slots['MenuItem'].value
    session_attrs = {'last_order': menu_item}
    response_text = f'You ordered {menu_item}'
    img_url = "https://i.imgur.com/PytSZCG.png"
    card = echopy.StandardCard(title="Order",
                               text=f"You ordered {menu_item}",
                               large_image_url=img_url)
    return Response(output_speech=PlainTextOutputSpeech(response_text),
                    session_attributes=session_attrs, card=card)


# Handles: IntentRequest (unimplemented intent)
# For example, if 'WeaveBasketIntent' is defined in your
# interaction model, but you haven't defined a handler
# for it with @echopy.on_intent('WeaveBasketIntent'),
# this will catch it. If you don't define your own here,
# by default echopy will return a "Sorry, I didn't
# understand your request" speech response.
@echopy.fallback
def unimplemented(request, session):
    intent_name = request.intent.name
    speech = PlainTextOutputSpeech(f"Sorry, {intent_name} isn't implemented!")
    return Response(output_speech=speech)

