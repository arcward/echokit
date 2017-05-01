import echokit


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


@echokit.on_intent('OrderIntent')
@echokit.slot(name='MenuItem')
def order_intent(request_wrapper, menu_item):
    print(menu_item)
    request = request_wrapper.request
    menu_item = request.intent.slots['MenuItem'].value
    return echokit.tell(f"You just ordered {menu_item}")\
        .simple_card(title="Previous order", content=menu_item)

# @echokit.fallback
# def unimplemented(request_wrapper):
#     return echokit.ask(speech="What did you say?", reprompt="Hello?")
