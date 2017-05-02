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

Handling Requests
-----------------
Setup/verification
^^^^^^^^^^^^^^^^^^
.. py:data:: application_id

   Set to your skill's application ID, found in the `Alexa dev portal`_.

.. py:data:: verify_application_id
    :annotation: = True

    If **True**, will verify the application ID in each request against
    :py:data:`echokit.application_id`, logging an error and raising a
    :py:exc:`ValueError` exception upon mismatch. If **False**, will ignore
    the ID and continue as normal.

    :type: :py:class:`bool`

.. py:function:: handler(event, context)

    Handles incoming Lambda requests and routes them to the appropriate
    function based on the
    :py:func:`@echokit.on_session_launch <echokit.on_session_launch>`,
    :py:func:`@echokit.on_session_ended <echokit.on_session_end>`,
    :py:func:`@echokit.on_intent() <echokit.on_intent>` and
    :py:func:`@echokit.fallback <echokit.fallback>` decorators.

    Assign ``handler == echokit.handler`` in your main module and set
    ``[your_module].handler`` as the handler in your Lambda function's
    configuration.

Responding
^^^^^^^^^^

.. py:function:: ask(speech, reprompt=None, ssml=False, session_attributes=None)

    Ask the user a question. By default, *shouldEndSession* is *False*

    :param str speech: *OutputSpeech* text for response
    :param str reprompt: *OutputSpeech* text to reprompt the user
    :param bool ssml: *True* if speech text is in SSML format
        (default: *False*)
    :param dict session_attributes: Session attributes to set

.. py:function:: tell(speech, ssml=False)

    Tell the user something. By default, *shouldEndSession* is *True*.
    Additions can be made via the :py:class:`ASKResponse` methods,
    such as adding a card like
    ``echokit.tell('Hi').simple_card('Hello!', 'How are you?')``

    :param str speech: *OutputSpeech* text for response
    :param bool ssml: *True* if speech text is in SSML format
        (default: *False*)

.. py:class:: ASKResponse()

    Base class for responses. :py:func:`echokit.ask()` and
    :py:func:`echokit.tell()` are convenience methods which generate this
    class.

    .. py:method:: should_end_session(end_session)

        :param bool end_session: *True* or *False* to end the session

    .. py:method:: simple_card(title=None, content=None)

        Attaches a *Simple* type card to your response

    .. py:method:: standard_card(title=None, text=None, small_image_url=None, large_image_url=None)

        Attaches a *Standard* type card to your response

        :param str title:
        :param str text:
        :param str small_image_url:
        :param str large_image_url:

    .. py:method:: link_account_card(content=None)

        Attaches a *LinkAccount* type card to your response

    .. py:method:: session_attributes(session_attributes)

        :param dict session_attributes: Session attributes to set in your
            response

    .. py:method:: reprompt(speech, ssml=False)

        Attaches a reprompt to your response

        :param str speech: Speech text
        :param bool ssml: Set to *True* if using SSML

    .. py:method:: speech(text, ssml=False)

        Attaches *OutputSpeech* to your response

        :param str text: Speech text
        :param bool ssml: *True* if speech text is in SSML format





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

.. py:decoratormethod:: on_session_ended

    Designates handler function for a :py:class:`SessionEndedRequest <request_models.SessionEndedRequest>`

.. py:decoratormethod:: on_intent(intent_name)

    Designates handler function for an :py:class:`IntentRequest <request_models.IntentRequest>` matching
    *intent_name*

    :param str intent_name: Name of the intent to handle (:py:attr:`Intent.name <request_models.Intent.name>`)

.. py:decoratormethod:: slot(name, dest=None)

    Causes the value of the slot to be passed to your function as keyword param
    *name*, or one set in *dest* (ex: if an IntentRequest sends you a slot
    named '*manufacturer*' in your interaction model, set
    ``@slot(name='manufacturer')`` and its value will be passed).

    :param str name: Name of the slot received in the request (by default,
        will be passed to your function as a keyword argument)
    :param str dest: (Default: *None*) Set to change the keyword argument
        passed to your function

.. py:decoratormethod:: fallback

   Designates the handler function for any :py:class:`IntentRequest <request_models.IntentRequest>` whose
   name doesn't have an associated handler via :py:func:`@echokit.on_intent() <on_intent>`. If not
   used, will default to:

    .. py:function:: fallback_default(request, session)

        The default handler for incoming intent requests where the intent name
        doesn't match anything handled via
        :py:func:`@echokit.on_intent() <echokit.on_intent>` and no handler has
        been specified via :py:func:`@echokit.fallback <echokit.fallback>`.

        :return: PlainText speech: "*Sorry, I didn't understand your request*"
        :rtype: :py:class:`Response`

Usage
~~~~~
Handler functions should accept a single argument, which will be a wrapper
for the request/session/context/version received. If you use the *@slot*
decorator, it should accept the slot's name or the value set for *dest*:


.. code-block:: python

    @echokit.on_session_launch
    def session_started(request_wrapper):
        return echokit.ask('You just started a new session!')

    @echokit.on_intent('OrderIntent')
    @echokit.slot('MenuItem', dest='menu_item')
    def order_intent(request_wrapper, menu_item):
        request = request_wrapper.request
        return echokit.tell(f"You just ordered {menu_item}")\
            .simple_card(title="Previous order", content=menu_item)


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
