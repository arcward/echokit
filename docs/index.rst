.. echokit documentation master file, created by
   sphinx-quickstart on Sat Apr 22 22:31:19 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

echokit
===================================

.. toctree::
    :maxdepth: 5
    :caption: Contents:

.. py:module:: echokit

Requests
========
For more info, see: `JSON Interface Reference for Custom Skills`_

Handling
--------
Setup/verification
^^^^^^^^^^^^^^^^^^
.. py:data:: application_id

   Set to your skill's application ID, found in the `Alexa dev portal`_.

.. py:data:: verify_application_id
    :annotation: = True

    If **True**, will verify the application ID in each request against
    :py:data:`echokit.application_id`, logging an error and raising an
    :py:exc:`Exception` upon mismatch. If **False**, will ignore the ID and
    continue as normal.

    :type: :py:class:`bool`

.. py:function:: handler(event, context)

    Handles incoming Lambda requests and routes them to the appropriate
    function based on the
    :py:func:`@echokit.on_session_launch <echokit.on_session_launch>`,
    :py:func:`@echokit.on_session_end <echokit.on_session_end>`,
    :py:func:`@echokit.on_intent() <echokit.on_intent>` and
    :py:func:`@echokit.fallback <echokit.fallback>` decorators.

    Assign ``handler == echokit.handler`` in your main module and set
    ``[your_module].handler`` as the handler in your Lambda function's
    configuration.

Example
~~~~~~~
.. code-block:: python

    import echokit

    handler = echokit.handler
    echokit.application_id = "my_app_id"

Decorators
^^^^^^^^^^
.. py:decoratormethod:: on_session_launch

    Designates handler function for :py:class:`LaunchRequest <request_models.LaunchRequest>`

.. py:decoratormethod:: on_session_end

    Designates handler function for a :py:class:`SessionEndedRequest <request_models.SessionEndedRequest>`

.. py:decoratormethod:: on_intent(intent_name)

    Designates handler function for an :py:class:`IntentRequest <request_models.IntentRequest>` matching
    *intent_name*

    :param str intent_name: Name of the intent to handle (:py:attr:`Intent.name <request_models.Intent.name>`)

Example
~~~~~~~
.. code-block:: python

    @echokit.on_session_launch
    def session_started(launch_request, session):
        speech = "You just started a new session!"
        return Response(output_speech=PlainTextOutputSpeech(speech)

    @echokit.on_intent('SomeIntent')
    def some_intent(request, session):
        speech = f"You invoked {request.intent.name}"
        return Response(output_speech=PlainTextOutputSpeech(speech))

Unrecognized intents
^^^^^^^^^^^^^^^^^^^^
.. py:decoratormethod:: fallback

   Designates the handler function for any :py:class:`IntentRequest <request_models.IntentRequest>` whose
   name doesn't have an associated handler via :py:func:`@echokit.on_intent() <on_intent>`

.. py:function:: fallback_default(request, session)

    The default handler for incoming intent requests where the intent name
    doesn't match anything handled via
    :py:func:`@echokit.on_intent() <echokit.on_intent>` and no handler has
    been specified via :py:func:`@echokit.fallback <echokit.fallback>`.

    :return: PlainText speech: "*Sorry, I didn't understand your request*"
    :rtype: :py:class:`Response`

Models
------
RequestWrapper
^^^^^^^^^^^^^^
.. py:module:: echokit.request_models
.. py:class:: RequestWrapper

    Wrapper for an incoming request's parameters and body.

    :raises Exception: If :py:data:`echokit.verify_application_id`
        is **True** and  :py:data:`session.application.application_id \
        <Application.application_id>` doesn't match
        :py:data:`echokit.application_id`

    .. py:attribute:: request

        :type: :py:class:`LaunchRequest`, :py:class:`IntentRequest`,
            or :py:class:`SessionEndedRequest`

    .. py:attribute:: session

        :type: :py:class:`Session`

    .. py:attribute:: context

        :type: :py:class:`Context`

    .. py:attribute:: version
        :annotation: = '1.0'

Session
^^^^^^^
.. py:class:: Session

    .. py:attribute:: session_id
    .. py:attribute:: new
    .. py:attribute:: attributes

        :type: dict(str, object)
    .. py:attribute:: application

        :type: :py:class:`Application`
    .. py:attribute:: user

        :type: :py:class:`User`

Context
^^^^^^^
.. py:class:: Context

    .. py:attribute:: system

        :type: :py:class:`System`

    .. py:attribute:: audio_player

        :type: :py:class:`AudioPlayer`

System
^^^^^^
.. py:class:: System

    .. py:attribute:: api_endpoint

    .. py:attribute:: application

        :type: :py:class:`Application`
    .. py:attribute:: user

        :type: :py:class:`User`
    .. py:attribute:: device

        .. py:class:: Device

            .. py:attribute:: device_id
            .. py:attribute:: supported_interfaces

Application
^^^^^^^^^^^
.. py:class:: Application

    .. py:attribute:: application_id

User
^^^^
.. py:class:: User

    .. py:attribute:: user_id
    .. py:attribute:: access_token
    .. py:attribute:: permissions

AudioPlayer
^^^^^^^^^^^
.. py:class:: AudioPlayer

    **NOTE**: The AudioPlayer reference is not implemented, this is just
    a placeholder.

    For more info, see: `AudioPlayer Interface Reference`_

    .. py:attribute:: token
    .. py:attribute:: offset_in_milliseconds
    .. py:attribute:: player_activity

Standard Types
--------------
For more info, see: `Standard Request Types Reference`_

LaunchRequest
^^^^^^^^^^^^^
.. py:class:: LaunchRequest

    Register a handler for this type with the
    :py:func:`@echokit.on_session_launch <echokit.on_session_launch>`
    decorator.

    .. py:attribute:: request_id
    .. py:attribute:: timestamp
    .. py:attribute:: locale

SessionEndedRequest
^^^^^^^^^^^^^^^^^^^
.. py:class:: SessionEndedRequest

    Register a handler for this type with the
    :py:func:`@echokit.on_session_end <echokit.on_session_end>` decorator.

    .. py:attribute:: request_id
    .. py:attribute:: timestamp
    .. py:attribute:: locale
    .. py:attribute:: reason
    .. py:attribute:: error

        :type: :py:class:`SessionEndedRequest.Error`

    .. py:class:: Error

        .. py:attribute:: type
        .. py:attribute:: message

IntentRequest
^^^^^^^^^^^^^
.. py:class:: IntentRequest

    Register handlers for intent requests with the
    :py:func:`@echokit.on_intent() <echokit.on_intent>` decorator.

    **Unrecognized intents**:
        Use the :py:func:`@echokit.fallback <echokit.fallback>` decorator
        to register a function to handle any request received where
        :py:data:`IntentRequest.intent.name <Intent.name>` doesn't match
        anything handled by
        :py:func:`@echokit.on_intent() <echokit.on_intent>`.

        If :py:func:`@echokit.fallback <echokit.fallback>` isn't used,
        the default handler for this is :py:func:`echokit.fallback_default`

    .. py:attribute:: request_id
    .. py:attribute:: timestamp
    .. py:attribute:: locale
    .. py:attribute:: dialog_state
    .. py:attribute:: intent

        :type: :py:class:`Intent`

Intent
------
.. py:class:: Intent

    .. py:attribute:: name
    .. py:attribute:: confirmation_status
    .. py:attribute:: slots

        :type: list[:py:class:`Slot`]

.. py:class:: Slot

    .. py:attribute:: name
    .. py:attribute:: value
    .. py:attribute:: confirmation_status


Responses
=========
For more info, see: `JSON Interface Reference for Custom Skills`_

Response
--------
.. py:module:: echokit
.. py:class:: Response(output_speech=None, card=None, reprompt=None, \
                       should_end_session=None, session_attributes=None, \
                       directives=None, version='1.0')

    .. py:attribute:: output_speech
        :annotation: = None

        :type: :py:class:`PlainTextOutputSpeech`, :py:class:`SSMLOutputSpeech`

    .. py:attribute:: card
        :annotation: = None

        :type: :py:class:`SimpleCard`, :py:class:`StandardCard`, :py:class:`LinkAccountCard`

    .. py:attribute:: reprompt
        :annotation: = None

        :type: :py:class:`Reprompt`

    .. py:attribute:: should_end_session
        :annotation: = None

        :type: :py:class:`bool`

    .. py:attribute:: session_attributes
        :annotation: = None

        :type: :py:class:`dict[str, object]`

    .. py:attribute:: directives
        :annotation: = None

        :type: :py:class:`list`

    .. py:attribute:: version
        :annotation: = '1.0'

Output speech
-------------
PlainText
^^^^^^^^^
.. py:class:: PlainTextOutputSpeech(text)

    :param str text: Output speech text

    .. py:attribute:: type
            :annotation: = 'PlainText'


SSML
^^^^
.. py:class:: SSMLOutputSpeech(ssml)

    For more info, see: SSML_

    :param str ssml: SSML markup

Reprompt
--------
.. py:class:: Reprompt(output_speech)

    :param output_speech: Speech to return if a reprompt is needed
    :type output_speech: :py:class:`PlainTextOutputSpeech`,
        :py:class:`SSMLOutputSpeech`


Cards
-----

.. py:class:: SimpleCard(title=None, content=None)

    .. py:attribute:: title
        :annotation: = None

    .. py:attribute:: content
        :annotation: = None

.. py:class:: StandardCard(title=None, text=None, small_image_url=None, \
                           large_image_url=None)

    .. py:attribute:: title
        :annotation: = None

    .. py:attribute:: text
        :annotation: = None

    .. py:attribute:: small_image_url
        :annotation: = None

    .. py:attribute:: large_image_url
        :annotation: = None

.. py:class:: LinkAccountCard(content=None)

    .. py:attribute:: content
        :annotation: = None


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _`JSON Interface Reference for Custom Skills`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
.. _`Standard Request Types Reference`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-standard-request-types-reference
.. _`AudioPlayer Interface Reference`: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/custom-audioplayer-interface-reference
.. _`Alexa dev portal`: https://developer.amazon.com/edw/home.html
.. _SSML: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/speech-synthesis-markup-language-ssml-reference
