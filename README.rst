=======
echokit
=======

**Lightweight SDK for the Alexa Skills Kit** (Python 3.6)

Why?
====
I felt other solutions were either too clunky, or not quite 
focused on deployment in AWS Lambda (execution time is money!). 
That's why echokit has **no dependencies** and includes a 
command-line tool *echodist* to package itself with your 
project for easier deployment to Lambda!

Installation
============
Requirements:
 - ``Python >= 3.6`` (that's it!)

**Using pip**:

.. code-block:: bash

    $ pip install echokit

**From GitHub**:

Clone/download this repo and run this from the ``echokit/`` directory:

.. code-block:: bash

    $ python setup.py install
    
Sample
======
A sample skill using echokit can be found at this repo:
https://github.com/arcward/echokit-example

=============
Documentation
=============
More comprehensive documentation can be found on ReadTheDocs_:

http://echokit.readthedocs.io/en/latest/

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

.. _ReadTheDocs: http://echokit.readthedocs.io/en/latest/
.. _flask-ask: https://github.com/johnwheeler/flask-ask
.. _flask: https://github.com/pallets/flask
.. _zappa: https://github.com/Miserlou/Zappa
.. _handler: http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html
.. _`Alexa dev portal`: https://developer.amazon.com/alexa
.. _`three basic request types`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference
.. _`official docs`: http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
