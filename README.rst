=======
echokit
=======

**Lightweight SDK for the Alexa Skills Kit** (Python 3.6)

Why?
====
I felt other solutions were either too clunky, or not quite 
focused on deployment in AWS Lambda (execution time is money!). 
That's why echokit has **no dependencies**!

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
When you configure your Lambda function, you need to specify a handler. And
when you configure your skill in the `Alexa dev portal`_, you'll be provided
an application ID for your skill. Set these at the top of your module:

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

    @echokit.on_session_launch
    def session_started(request_wrapper):
        return echokit.ask('Hello!')

    @echokit.on_session_ended
    def session_ended(request_wrapper):
        # Print statement will log the reason to CloudWatch
        print(request_wrapper.request.reason)

    @echokit.on_intent('OrderIntent')
    @echokit.slot('MenuItem', dest='menu_item')
    def order_intent(request_wrapper, menu_item):
        print(menu_item)
        request = request_wrapper.request
        menu_item = request.intent.slots['MenuItem'].value
        return echokit.tell(f"You just ordered {menu_item}")\
            .simple_card(title="Previous order", content=menu_item)

Creating a Lambda deployment package
====================================
For reference, see the `official docs`_.

echodist
--------
``echodist`` is a script included to help create ZIP deployment
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
