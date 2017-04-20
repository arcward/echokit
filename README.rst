echopy
======

Python 3.6-compatible SDK for Alexa Skills Kit


Example
=======

See ``example_main.py`` (shown below)

Set ``echopy.handler`` as your skill's handler in the Lambda console and
set ``echopy.application_id`` as your skill's app ID (as found in the
Alexa dev portal).

There are decorators for the three basic requests Alexa skills need to
handle: ``LaunchRequest``, ``SessionEndedRequest`` and ``IntentRequest``.
Those are ``@echopy.on_session_launch``, ``@echopy.on_session_end``, and
``@echopy.on_intent('some_intent')``

The ``example_main.py`` file:

.. code-block:: python

    import echopy
    from echopy import Response, OutputSpeech


    # In the lambda console, you would set your
    # handler to: ``example_main.handler``
    def handler(event, context):
        return echopy.handler(event, context)

    # Your skill ID, as provided in the Alexa dev portal
    echopy.application_id = "some_app_id"

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
        return Response(output_speech=OutputSpeech(text=response_text),
                        session_attributes=session_attrs)


Packaging
=========

The project structure for ``example_main.py`` would be::

    example_main.py
        echopy/

You would zip ``example_main.py`` and ``echopy/`` together (not their
parent directory) and upload to Lambda, and be on your way!