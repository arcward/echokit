=========================================
echokit: Alexa Skills Kit SDK (Python 3.6)
=========================================
"**Why not Flask-Ask ?**"

Flask-Ask_ carries a number 
of dependencies (such as Flask_) and requires Zappa_ 
to deploy to AWS Lambda. Given that Lambda is billed based 
on memory footprint / execution duration / number of requests, 
I wanted something more lightweight and more easily deployed 
to Lambda. 

That's why **echokit** has **no dependencies** and includes
a CLI utility ``echodist`` to package skills for deployment.

Sample
======
A sample skill using echokit can be found at this repo:
https://github.com/arcward/echokit-example

Installation
============
Requirements:
 - ``Python >= 3.6`` (that's it!)

Clone/download the repo, and run this from the ``echokit/`` directory:

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

    import echokit

    # Set as your skill's handler in Lambda
    handler = echokit.handler
    # Set as your application ID from the Alexa dev portal
    echokit.application_id = "your_application_id"

If your module is ``main.py``, in your Lambda configuration, you'd set
``main.handler`` as your handler.

Handling requests
=================
There are `three basic request types`_ to handle. In turn, echokit has
four decorators to make that easy:
 - ``@echokit.on_session_launch`` for *LaunchRequest*
 - ``@echokit.on_session_ended`` for *SessionEndedRequest*
 - ``@echokit.on_intent(intent_name)`` for an *IntentRequest* matching
   ``intent_name``

   + ``@echokit.fallback`` for intent requests without a handler specified
     by ``@echokit.on_intent()``

Functions with these decorators should take two arguments, one for
the ``Request`` object and one for the ``Session`` object.
The request object will either be a ``LaunchRequest``, ``SessionEndedRequest``
or ``IntentRequest``.

Sending responses
=================
Request handlers should return ``Response``, for which you can set:
 - Output speech: ``PlainTextOutputSpeech`` or ``SSMLOutputSpeech``
 
Functions with these decorators should take a single argument, which will
be the ``echokit.Request`` object, through which you can access the
``Session`` and ``Context`` objects, as well at the request from the Alexa
service (either ``LaunchRequest``, ``SessionEndedRequest`` or ``IntentRequest``
objects).

Sending responses
=================
Request handlers should return ``echokit.Response``, for which you can set:
 - Output speech: ``echokit.OutputSpeech``
 - Session attributes (as ``dict[str, object]``)
 - A reprompt: ``Reprompt``
 - A card to display:

   + ``SimpleCard``
   + ``StandardCard``
   + ``LinkAccountCard``

Example
=======
.. code-block:: python

    import echokit
    from echokit import Response, PlainTextOutputSpeech, SimpleCard

    handler = echokit.handler
    echokit.application_id = "my_app_id"

    @echokit.on_session_started
    def start_session(request, session):
        output_speech = PlainTextOutputSpeech("Hello!")
        return Response(output_speech=output_speech)

    @echokit.on_session_ended
    def end_session(request, session):
        output_speech = PlainTextOutputSpeech("Goodbye!")
        simple_card = SimpleCard(title="Goodbye", content="Seeya!")
        return Response(output_speech=output_speech, card=simple_card)

    @echokit.on_intent('OrderIntent')
    def send_order(request, session):
        menu_item = request.intent.slots['MenuItem'].value
        output_speech = PlainTextOutputSpeech(f"You ordered a {menu_item}")
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
subtree of the directory you specified, as well as an ``echokit/`` directory.

Manually
--------
Your ZIP file should be created from within your top-level package (don't
just zip the enclosing directory). You'll need to download/clone echokit
and include ``echokit/`` in in that same top-level directory. So if your
``__init__.py`` is in ``~/my_project/`` you should have ``~/my_project/echokit``.

See the `official docs`_ for more info.

.. _flask-ask: https://github.com/johnwheeler/flask-ask
.. _flask: https://github.com/pallets/flask
.. _zappa: https://github.com/Miserlou/Zappa
.. _handler: http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html
.. _`Alexa dev portal`: https://developer.amazon.com/alexa
.. _`three basic request types`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference
.. _`official docs`: http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
