echopy
======

Python 3.6-compatible SDK for Alexa Skills Kit

**Requirements**: Python 3.6

**To install**: ``cd`` into the source directory and run::

    > python setup.py install

Basics
======
See ``example_main.py``

The top of your main module should have:

.. code-block:: python

    import echopy

    # Set as your skill's handler in Lambda
    def handler(event, context):
        return echopy.handler(event, context)

    # Set as your application ID from the Alexa dev portal
    echopy.application_id = "your_application_id"

There are decorators for the three basic requests Alexa skills need to
handle:

- ``LaunchRequest``: ``@echopy.on_session_launch`` :
- ``SessionEndedRequest``: ``@echopy.on_session_end``
- ``IntentRequest``: ``@echopy.on_intent('some_intent')`` and ``@echopy.fallback``

``@echopy.fallback`` is used for cases where you receive a request for
an intent that doesn't yet have a function to handle it.


Creating a deployment package
=============================
After installing echopy, you can use the command ``echodist`` from the
command line. When you specify your top-level package directory with ``--dir``,
this will create a ZIP file you can upload to Lambda.

For example, if your ``__init__.py`` is located at
``~/somepy/somepy/__init__.py`` you would run:

.. code-block:: bash

    ~ & echodist --dir ~/somepy/somepy

This would create ``somepy.zip`` in your home directory (or whever you
ran the command). If you unzip it, you can see it includes the entire
subtree of the directory you specified, as well as an ``echopy/`` directory.

