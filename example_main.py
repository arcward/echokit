import echopy
from echopy import Response, OutputSpeech


# In the lambda console, you would set your
# handler to: ``example_main.handler``
def handler(event, context):
    return echopy.handler(event, context)

# Your skill ID, as provided in the Alexa dev portal
echopy.application_id = "some_app_id"


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
@echopy.on_intent('OrderIntent')
def specific_intent(event):
    response_text = (f"You asked me to "
                     f"{event.request.intent.slots['Order'].value}")
    return Response(output_speech=OutputSpeech(text=response_text))