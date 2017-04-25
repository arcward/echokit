"""Models of objects in requests received from the Alexa service

https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#session-object
"""
import logging
from typing import Dict
from echokit.audio_player import AudioPlayer

logger = logging.getLogger(__name__)


class Session:
    """Session object included by standard request types
    
    Standard request types: ``LaunchRequest``, ``IntentRequest``, 
    ``SessionEndedRequest``
    
    Not included for requests from ``AudioPlayer`` and others
    """

    def __init__(self, session_id, new, attributes, application, user):
        """
        
        :param session_id: Unique identifier for a user's session
        :param new: Whether this is a new session (``True`` or ``False``)
        :param attributes: Key:value pairs (attribute name: object value)
        :param application: ``Application`` object, where 
            ``Application.application_id`` is the ID of your skill. Set the 
            expected ID at ``echokit.application_id``
        :param user: ``User`` object
        """
        self.session_id = session_id
        self.new: bool = new
        self.attributes: Dict[str, object] = attributes
        self.application = application
        self.user = user

    @staticmethod
    def __build(**kwargs):
        kwargs['application'] = Application(**kwargs['application'])
        kwargs['user'] = User(**kwargs['user'])
        return Session(**kwargs)


class Context:
    """Data on the current state of the Alexa service/device"""
    def __init__(self, system=None, audio_player=None):
        """
        :param system: ``System`` object
        :param audio_player: ``AudioPlayer`` object
        """
        self.system = system
        self.audio_player = audio_player

    @staticmethod
    def _build(**kwargs):
        audio_player = kwargs.get('audio_player')
        if audio_player:
            audio_player = AudioPlayer(**audio_player)

        system = kwargs.get('system')
        if system:
            system = System._build(**system)
        return Context(system, audio_player)


class Device:
    def __init__(self, device_id=None, supported_interfaces=None):
        self.device_id = device_id
        self.supported_interfaces = supported_interfaces


class System:
    """Info on the state of Alexa service/device interacting with your skill"""

    def __init__(self, application=None, user=None, device=None,
                 api_endpoint=None):
        """
        
        :param application: ``Application`` object
        :param user: ``User`` object
        :param device: ``System._Device`` object with info on the device 
            sending the request
        :param api_endpoint: Object referencing correct base URI to 
            refer to by region
        """
        self.application = application
        self.user = user
        self.device = device
        self.api_endpoint = api_endpoint

    @staticmethod
    def _build(**kwargs):
        app = kwargs.get('application')
        if app:
            kwargs['application'] = Application(**app)

        user = kwargs.get('user')
        if user:
            kwargs['user'] = User(**user)

        device = kwargs.get('device')
        if device:
            kwargs['device'] = Device(**device)

        return System(**kwargs)


class User:
    """Describes a user making a request"""

    def __init__(self, user_id=None, access_token=None, permissions=None):
        """

        :param user_id: User ID generated when user enables skill in 
            the Alexa app (max 255 chars)
        :param access_token: Identifies the user in another system
        :param permissions: Contains ``consentToken`` allowing the skill 
            access to information a user's consented o provide
        """
        self.user_id = user_id
        self.access_token = access_token
        self.permissions = permissions


class Intent:
    """Intent provided in ``IntentRequest``"""
    def __init__(self, name, confirmation_status=None, slots=None):
        """
        
        :param name: Name of the intent
        :param confirmation_status: Enumeration on whether user has 
            explicitly confirmed/denied the entire intent. Values: 
            ``NONE``, ``CONFIRMED``, ``DENIED``
        :param slots: Key:value pairs based on intent schema. Can be empty. 
            Key: name of the slot, value: ``Slot`` (also contains 
            name of the slot)
        """
        self.name = name
        self.confirmation_status = confirmation_status

        if slots is None:
            slots = {}
        self.slots: Dict[str, Slot] = slots

    @staticmethod
    def _build(**kwargs):
        slots = kwargs.get('slots', {})
        slot_objs = [Slot(**v) for v in slots.values()]
        kwargs['slots'] = {s.name: s for s in slot_objs}
        return Intent(**kwargs)


class Slot:
    """``Slot`` present in ``Intent.slots``"""
    def __init__(self, name=None, value=None, confirmation_status=None):
        """
        
        :param name: Slot name
        :param value: Value (**not required**)
        :param confirmation_status: Enumeration of whether 
            the user has confirmed/denied the slot value. 
            Values: ``NONE``, ``CONFIRMED``, ``DENIED``
        """
        self.name = name
        self.value = value
        self.confirmation_status = confirmation_status


class Application:
    def __init__(self, application_id):
        self.application_id = application_id


class Error:
    def __init__(self, type=None, message=None):
        self.type = type
        self.message = message
