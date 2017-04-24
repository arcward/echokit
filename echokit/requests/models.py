"""Models of objects in requests received from the Alexa service

https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference#session-object
"""
import logging
from collections import namedtuple
from typing import Dict


logger = logging.getLogger(__name__)
Application = namedtuple('Application', 'application_id')
Error = namedtuple('Error', 'type message')
attr_map = {
    'accessToken': 'access_token',
    'applicationId': 'application_id',
    'sessionId': 'session_id',
    'AudioPlayer': 'audio_player',
    'System': 'system',
    'Device': 'device',
    'deviceId': 'device_id',
    'supportedInterfaces': 'supported_interfaces',
    'userId': 'user_id',
    'apiEndpoint': 'api_endpoint',
    'requestId': 'request_id',
    'dialogState': 'dialog_state',
    'confirmationStatus': 'confirmation_status',
    'offsetInMilliseconds': 'offset_in_milliseconds',
    'playerActivity': 'player_activity'
}


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
    def from_json(json_obj):
        app = Application(json_obj['application']['applicationId'])
        user = User(json_obj['user']['userId'],
                    json_obj['user'].get('accessToken'),
                    json_obj['user'].get('permissions'))
        session = Session(json_obj['sessionId'], json_obj['new'],
                          json_obj.get('attributes', {}), app, user)
        return session


class Context:
    """Data on the current state of the Alexa service/device"""

    def __init__(self, system, audio_player):
        """
        :param system: ``System`` object
        :param audio_player: ``AudioPlayer`` object
        """
        self.system = system
        self.audio_player = audio_player

    @staticmethod
    def from_json(json_obj):
        system = json_obj.get('System')
        if system:
            system = System.from_json(system)

        audio_player = json_obj.get('AudioPlayer')

        context = Context(system, audio_player)
        return context

    def to_json(self):
        context_dict = {'System': self.system.to_json()}
        if self.audio_player:
            context_dict['AudioPlayer'] = self.audio_player.to_json()
        return context_dict


class System:
    """Info on the state of Alexa service/device interacting with your skill"""
    _Device = namedtuple('Device', 'device_id supported_interfaces')

    def __init__(self, application, user, device, api_endpoint):
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
    def from_json(json_obj):
        application = json_obj.get('application')
        if application:
            application = Application(application.get('applicationId'))

        user = json_obj.get('user')
        if user:
            user = User(user.get('userId'), user.get('accessToken'),
                        user.get('permissions'))

        device = json_obj.get('device')
        if device:
            device = System._Device(device.get('deviceId'),
                                    device.get('supportedInterfaces'))

        api_endpoint = json_obj.get('apiEndpoint')
        system = System(application, user, device, api_endpoint)
        return system

    def to_json(self):
        sys_dict = {'apiEndpoint': self.api_endpoint}

        if self.application:
            sys_dict['application'] = {'applicationId':
                                       self.application['applicationId']}

        if self.user:
            sys_dict['user'] = self.user.to_json()

        if self.device:
            sys_dict['device'] = {
                'deviceId': self.device.device_id,
                'supportedInterfaces': self.device.supported_interfaces
            }

        return {k: v for (k, v) in sys_dict if v is not None}


class User:
    """Describes a user making a request"""

    def __init__(self, user_id, access_token, permissions):
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


class AudioPlayerRequest:
    def __init__(self, version, ):
        pass


class Intent:
    """Intent provided in ``IntentRequest``"""

    def __init__(self, name, confirmation_status, slots):
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
        self.slots: Dict[str, Slot] = slots

    @staticmethod
    def from_json(json_obj):
        json_slots = json_obj.get('slots', {})
        slots = {}
        for k, v in json_slots.items():
            slots[k] = Slot.from_json(v)
        intent = Intent(json_obj['name'], json_obj.get('confirmationStatus'),
                        slots)
        return intent


class Slot:
    """``Slot`` present in ``Intent.slots``"""

    def __init__(self, name, value, confirmation_status):
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

    @staticmethod
    def from_json(json_obj):
        slot = Slot(json_obj.get('name'), json_obj.get('value'),
                    json_obj.get('confirmationStatus'))
        return slot


# class AudioPlayer:
#     def __init__(self, token, offset_in_milliseconds, player_activity):
#         self.token = token
#         self.offset_in_milliseconds = offset_in_milliseconds
#         self.player_activity = player_activity
#
#     @staticmethod
#     def from_json(json_obj):
#         audio_player = AudioPlayer(json_obj.get('token'),
#                                    json_obj.get('offsetInMilliseconds'),
#                                    json_obj.get('playerActivity'))
#         set_unknown(json_obj, audio_player)
#         return audio_player
#
#     def to_json(self):
#         ap_dict = {
#             'token': self.token,
#             'offsetInMilliseconds': self.offset_in_milliseconds,
#             'playerActivity': self.player_activity
#         }
#         return {k: v for (k, v) in ap_dict.items() if v is not None}
#
#
# class AudioPlayerDirective:
#     def __init__(self):
#         pass
