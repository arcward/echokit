======
echopy
======
A **Python 3.6** SDK for the Alexa Skills Kit

Sample
======
A sample skill using echopy:
https://github.com/arcward/echopy-example

Installation
============
Requirements:
 - ``Python >= 3.6`` (that's it!)

Clone/download the repo, and run this from the ``echopy/`` directory:

.. code-block:: bash

    $ python setup.py install

===============
Getting Started
===============
When you configure your Lambda function, you need to specify a handler_. And
when you configure your skill in the `Alexa dev portal`_, you'll be provided
an application ID for your skill. To provide these, the top of your module
should look like this:

.. code-block:: python

    import echopy

    # Set as your skill's handler in Lambda
    def handler(event, context):
        return echopy.handler(event, context)

    # Set as your application ID from the Alexa dev portal
    echopy.application_id = "your_application_id"

If your module is ``main.py``, in your Lambda configuration, you'd set
``main.handler`` as your handler.

Handling requests
=================
There are `three basic request types`_ to handle. In turn, echopy has
four decorators to make that easy:

 - ``@echopy.on_session_launch`` for *LaunchRequest*
 - ``@echopy.on_session_end`` for *SessionEndedRequest*
 - ``@echopy.on_intent(intent_name)`` for an *IntentRequest* matching
   ``intent_name``
   
   + ``@echopy.fallback`` for intent requests without a handler specified
     by ``@echopy.on_intent()``

Functions with these decorators should take a single argument, which will
be the ``echopy.Request`` object, through which you can access the
``Session`` and ``Context`` objects, as well at the request from the Alexa
service (either ``LaunchRequest``, ``SessionEndedRequest`` or ``IntentRequest``
objects).


Sending responses
=================
Request handlers should return ``echopy.Response``, for which you can set:
 - Output speech: ``echopy.OutputSpeech``
 - Session attributes (as ``dict[str, object]``)
 - A reprompt: ``echopy.Reprompt``
 - A card to display:
 
   + ``SimpleCard``
   + ``StandardCard``
   + ``LinkAccountCard``

Example
=======

.. code-block:: python

    import echopy
    from echopy import Response, OutputSpeech, SimpleCard

    def handler(event, context):
        return echopy.handler(event, context)

    echopy.application_id = "my_app_id"

    @echopy.on_session_started
    def start_session(event):
        output_speech = OutputSpeech(text="Hello!")
        return Response(output_speech=output_speech)

    @echopy.on_session_end
    def end_session(event):
        output_speech = OutputSpeech(text="Goodbye!")
        simple_card = SimpleCard(title="Goodbye", content="Seeya!")
        return Response(output_speech=output_speech, card=simple_card)

    @echopy.on_intent('OrderIntent')
    def send_order(event):
        menu_item = event.request.intent.slots['MenuItem'].value
        output_speech = OutputSpeech(text=f"You ordered a {menu_item}")
        return Response(output_speech=output_speech,
                        session_attributes={'last_ordered': menu_item})

Creating a Lambda deployment package
====================================
For reference, see the `official docs`_.

echodist
--------
``echodist`` is a script included to automatically create ZIP deployment
packages. If you installed via *setup.py*, you can run it from the command
line (try ``echodist --help``).

Specify your top-level package directory with ``--dir``. For example, if
your ``__init__.py`` is located at ``~/somepy/somepy/__init__.py`` you would
run:

.. code-block:: bash

    ~ & echodist --dir ~/somepy/somepy

This would create ``somepy.zip`` in your home directory (or whever you
ran the command). If you unzip it, you can see it includes the entire
subtree of the directory you specified, as well as an ``echopy/`` directory.

Manually
--------
Your ZIP file should be created from within your top-level package (don't
just zip the enclosing directory). You'll need to download/clone echopy
and include ``echopy/`` in in that same top-level directory. So if your
``__init__.py`` is in ``~/my_project/`` you should have ``~/my_project/echopy``.

See the `official docs`_ for more info.

.. _handler: http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html
.. _`Alexa dev portal`: https://developer.amazon.com/alexa
.. _`three basic request types`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference
.. _`official docs`: http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
