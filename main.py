import echokit

# In the Lambda config, 'handler' would be
# set to ``order_skill.handler``
handler = echokit.handler

# Your skill ID, as provided in the Alexa dev portal
echokit.verify_application_id = False


# All apps are required to handle three basic requests,
# which have their own decorators:
# * LaunchRequest:          @echokit.on_session_launch
# * SessionEndedRequest:    @echokit.on_session_ended
# * IntentRequest:          @echokit.on_intent('your_intent_name')

# Handles: LaunchRequest
@echokit.on_session_launch
def session_started(request_wrapper):
    return echokit.ask('Welcome to Order Maker! WATCHU WANT?')


# Handles: SessionEndedRequest
@echokit.on_session_ended
def session_ended(request_wrapper):
    print(request_wrapper.request.reason)


# Handles: IntentRequest
@echokit.on_intent('HoursIntent')
def hours_intent(request_wrapper):
    return echokit.tell("We're open 5AM to 8PM!") \
        .simple_card(title="Hours", content="5AM-8PM")


@echokit.on_intent('SanicIntent')
def sanic_intent(request_wrapper):
    return echokit.tell("Gotta go fast")\
        .standard_card(title="Sanic", text="Gotta go fast",
                       large_image_url="https://i.imgur.com/PytSZCG.png")


@echokit.on_intent('SsmlIntent')
def ssml_intent(request_wrapper):
    ssml = ("<speak>Onomatopoeia: "
            "<say-as interpret-as=\"spell-out\">onomatopoeia</say-as>."
            "</speak>")
    return echokit.tell(speech=ssml, ssml=True)


# Handles: IntentRequest
# This example is for an intent that handles a slot,
# showing how to access the intent's 'Order' slot.
# This would return output speech like: 'You asked me to jump'
# The session variable would be returned on the next invocation
@echokit.on_intent('OrderIntent')
@echokit.slot('MenuItem', dest='menu_item')
def order_intent(request_wrapper, menu_item):
    print(menu_item)
    request = request_wrapper.request
    menu_item = request.intent.slots['MenuItem'].value
    return echokit.tell(f"You just ordered {menu_item}")\
        .simple_card(title="Previous order", content=menu_item)



# Handles: IntentRequest (unimplemented intent)
# For example, if 'WeaveBasketIntent' is defined in your
# interaction model, but you haven't defined a handler
# for it with @echokit.on_intent('WeaveBasketIntent'),
# this will catch it. If you don't define your own here,
# by default echokit will return a "Sorry, I didn't
# understand your request" speech response.
@echokit.fallback
def unimplemented(request_wrapper):
    return echokit.ask(speech="What did you say?", reprompt="Hello?")
