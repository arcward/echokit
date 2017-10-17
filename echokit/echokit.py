import logging
from .request import ASKRequest
from .response import Response
from .exc import ASKException


class EchoKit:
    def __init__(self, app_id, verify_app_id=True):
        """

        :param app_id: Application ID for your skill
        :param verify_app_id: If *True*, the application ID of each
            incoming request will be compared against
            :attr:`EchoKit.app_id`, raising :exc:`ASKException` for
            any mismatched IDs. If *False*, incoming application IDs
            are ignored/
        """
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        #: The application ID for your skill
        self.app_id = app_id
        self.verify_app_id = verify_app_id
        self._handler_functions = {}
        if not verify_app_id:
            self.log.warning("App ID verification disabled, this skill will "
                             "attempt to respond to all incoming requests")
        self.session_attributes = {}

    def response(self, speech, type='PlainText'):
        """Create a response for the user

        :param speech: Outpuf speech
        :param type: Use _PlainText_ (default) if *speech* is
            formatted as plain text. Use _SSML_ if *speech*
            is a string of SSML markup.
        :return: :class:`Response`
        """
        return Response(
            speech=speech,
            speech_type=type,
            session_attributes=self.session_attributes
        )

    def launch(self, func):
        self._handler_functions['LaunchRequest'] = func

    def session_ended(self, func):
        self._handler_functions['SessionEndedRequest'] = func

    def intent(self, name):
        def intent_wrapper(func):
            self._handler_functions[name] = func
        return intent_wrapper

    def slot(self, *args):
        """Decorator to signal the presence of slots

        SLot names are case-sensitive, and will be passed into the
        handler function as keyword arguments.

        :param args: Slot names
        :return:
        """
        def slot_checker(func):
            def handler_func(request_, session_):
                kwargs = {}
                for slot_name in args:
                    slot_ = request_.intent.slots[slot_name]
                    kwargs[slot_.name] = slot_.value
                return func(request_, session_, **kwargs)
            return handler_func
        return slot_checker

    def handler(self, event, context):
        """Handler to specify in your Lambda function configuration

        For example:

        .. code-block:: python

            from echokit import EchoKit

            app = EchoKit("my_app_id")
            handler = app.handler


        In this scenario, the Lambda function would need to be
        configured to use *{your_module}.handler*.

        :param event:
        :param context:
        :return:
        """
        self.log.info({'event': event, 'context': context})
        event_ = ASKRequest(**event)
        request = event_.request
        session = event_.session

        # Validate incoming app ID if necessary
        request_id = session.application.applicationId
        if self.verify_app_id and (request_id != self.app_id):
            raise ASKException(f"Application ID mismatch. Expected: "
                               f"'{self.app_id}' Received: '{request_id}'")
        type_ = request.type
        if type_ == 'IntentRequest':
            type_ = request.intent.name
        if type_ not in self._handler_functions:
            raise ASKException(f"No handler defined for request: {type_}")
        request_handler = self._handler_functions[type_]
        # Retain any incoming session attributes
        if session.attributes:
            self.session_attributes = session.attributes._dict()
        else:
            self.session_attributes = {}
            session.attributes = self.session_attributes
        response = request_handler(request, session)._dict
        self.log.info({'response': response})
        return response
