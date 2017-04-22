import echopy
from echopy import Response, OutputSpeech


# In the lambda console, you would set your
# handler to: ``example_main.handler``
def handler(event, context):
    return echopy.handler(event, context)

# Your skill ID, as provided in the Alexa dev portal
echopy.application_id = "amzn1.ask.skill.6188e162-d7e3-451b-9078-6399f1916373"


# All apps are required to handle three basic requests,
# which have their own decorators:
# * LaunchRequest:          @echopy.on_session_launch
# * SessionEndedRequest:    @echopy.on_session_end
# * IntentRequest:          @echopy.on_intent('your_intent_name')

# Handles: LaunchRequest
@echopy.on_session_launch
def session_started(event):
    output_speech = OutputSpeech(text="You started a new session!")
    return Response(output_speech=output_speech)


# Handles: SessionEndedRequest
@echopy.on_session_end
def session_ended(event):
    output_speech = OutputSpeech("You ended our session :[")
    return Response(output_speech=output_speech)


# Handles: IntentRequest
@echopy.on_intent('SomeIntent')
def on_intent(event):
    output_speech = OutputSpeech(text="I did something with SomeIntent!")
    return Response(output_speech=output_speech)


# Handles: IntentRequest
# This example is for an intent that handles a slot,
# showing how to access the intent's 'Order' slot.
# This would return output speech like: 'You asked me to jump'
# The session variable would be returned on the next invocation
@echopy.on_intent('OrderIntent')
def specific_intent(event):
    order = event.request.intent.slots['Order'].value
    session_attrs = {'last_order': order}
    response_text = f'You asked me to {order}'
    img_url = "https://i.imgur.com/PytSZCG.png"
    card = echopy.StandardCard(title="Order",
                               text=f"You wanted me to {order}",
                               large_image_url=img_url)
    return Response(output_speech=OutputSpeech(text=response_text),
                    session_attributes=session_attrs, card=card)


# Handles: IntentRequest (unimplemented intent)
# For example, if 'WeaveBasketIntent' is defined in your
# interaction model, but you haven't defined a handler
# for it with @echopy.on_intent('WeaveBasketIntent'),
# this will catch it. If you don't define your own here,
# by default echopy will return a "Sorry, I didn't
# understand your request" speech response.
@echopy.fallback
def unimplemented(event):
    intent_name = event.request.intent.name
    output_speech = OutputSpeech(f"Sorry, {intent_name} isn't implemented!")
    return Response(output_speech)

