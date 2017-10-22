"""
Alexa skill based on the 'Session' sample at
https://github.com/alexa/skill-samples-java
"""
from echokit import EchoKit

# When configuring the Lambda function, the handler here would be
# defined as `session.handler`
app = EchoKit("my_app_id", verify_app_id=False)
handler = app.handler


@app.launch
def launch(request, session):
    response = app.response("Welcome to the Alexa Skills Kit sample. Please "
                            "tell me your favorite color by saying, my "
                            "favorite color is red")
    response.reprompt("Please tell me your favorite color by saying, "
                      "my favorite color is red")
    response.end_session = False
    return response


@app.session_ended
def session_ended(request, session):
    return app.response("Goodbye")


@app.intent('WhatsMyColorIntent')
def whats_my_color_intent(request, session):
    color = session.attributes.get('color')
    if color:
        return app.response(f"Your favorite color is {color}")
    else:
        return app.response("I'm not sure what your favorite color is. "
                            "You can say, my favorite color is red.")


@app.intent('MyColorIsIntent')
@app.slot('color')
def my_color_is_intent(request, session, color):
    # Reprompt if the slot wasn't found in the request
    if not color:
        response = app.response("I'm not sure what your favorite color is, "
                                "please try again.")
        response.reprompt("I'm not sure what your favorite color is. You "
                          "can tell me your favorite color by saying, my "
                          "favorite color is red.")
        response.end_session = False
        return response

    # If we received the slot, retain it in session attributes and
    # include a card in the response, also reprompting to give the
    # user a chance to ask for it
    response = app.response(f"I now know that your favorite color is {color}. "
                            f"You can ask me what your favorite color is by "
                            f"saying, what's my favorite color?")
    response.reprompt("You can ask me your favorite color by saying, "
                      "what's my favorite color?")
    response.session_attributes['color'] = color
    response.simple_card(title="Your favorite color", content=color)
    response.end_session = False
    return response
