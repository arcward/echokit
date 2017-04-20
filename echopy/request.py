from collections import namedtuple
import echopy

Application = namedtuple('Application', 'application_id')


class User:
    def __init__(self, user_id, access_token, permissions):
        self.user_id = user_id
        self.access_token = access_token
        self.permissions = permissions


class Request:
    def __init__(self, version, session, context, request):
        self.version = version
        self.session = session
        self.context = context
        self.request = request

        if self.session.application.application_id != echopy.application_id:
            raise Exception(f"Expected appID {echopy.application_id} "
                            f"but received "
                            f"{self.session.application.application_id}")

    @staticmethod
    def from_json(json_obj):
        return Request(json_obj['version'],
                       Session.from_json(json_obj['session']),
                       Context.from_json(json_obj['context']),
                       Request._factory(json_obj['request']))

    @staticmethod
    def _factory(json_request):
        request_types = {
            'LaunchRequest': LaunchRequest,
            'IntentRequest': IntentRequest,
            'SessionEndedRequest': SessionEndedRequest
        }
        request_type = json_request.get('type')
        if request_type:
            return request_types[request_type].from_json(json_request)
        else:
            return {}


class Session:
    attr_map = {
        'application': 'application',
        'sessionId': 'session_id',
        'user': 'user',
        'attributes': 'attributes',
        'new': 'new'
    }

    def __init__(self, session_id, new, attributes, application, user):
        self.session_id = session_id
        self.new = new
        self.attributes = attributes
        self.application = application
        self.user = user

    @staticmethod
    def from_json(json_obj):
        app = Application(json_obj['application']['applicationId'])
        user = User(json_obj['user']['userId'],
                    json_obj['user'].get('accessToken'),
                    json_obj['user'].get('permissions'))
        return Session(json_obj['sessionId'], json_obj['new'],
                       json_obj.get('attributes'), app, user)


class Context:
    def __init__(self, system, audio_player):
        self.system = system
        self.audio_player = audio_player

    @staticmethod
    def from_json(json_obj):
        system = json_obj.get('System')
        if system:
            system = System.from_json(system)
        audio_player = json_obj.get('AudioPlayer')
        if audio_player:
            audio_player = AudioPlayer.from_json(audio_player)
        return Context(system, audio_player)

    def to_json(self):
        context_dict = {'System': self.system.to_json()}
        if self.audio_player:
            context_dict['AudioPlayer'] = self.audio_player.to_json()
        return context_dict


class System:
    _Device = namedtuple('Device', 'device_id supported_interfaces')

    def __init__(self, application, user, device, api_endpoint):
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
        return System(application, user, device, api_endpoint)

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


class LaunchRequest:
    request_type = 'LaunchRequest'

    def __init__(self, request_id, timestamp, locale):
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale

    @staticmethod
    def from_json(json_obj):
        return LaunchRequest(json_obj['requestId'], json_obj['timestamp'],
                             json_obj['locale'])


class IntentRequest:
    request_type = 'IntentRequest'

    def __init__(self, request_id, timestamp, locale, dialog_state, intent):
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.dialog_state = dialog_state
        self.intent = intent

    @staticmethod
    def from_json(json_obj):
        return IntentRequest(json_obj['requestId'], json_obj['timestamp'],
                             json_obj['locale'], json_obj.get('dialogState'),
                             Intent.from_json(json_obj['intent']))


class Intent:
    _Slot = namedtuple('Slot', 'name value confirmation_status')

    def __init__(self, name, confirmation_status, slots):
        self.name = name
        self.confirmation_status = confirmation_status
        self.slots = slots

    @staticmethod
    def from_json(json_obj):
        json_slots = json_obj.get('slots', {})
        slots = {}
        for k, v in json_slots.items():
            slots[k] = Intent._Slot(v.get('name'), v.get('value'),
                                    v.get('confirmationStatus'))
        return Intent(json_obj['name'], json_obj.get('confirmationStatus'),
                      slots)


class SessionEndedRequest:
    request_type = 'SessionEndedRequest'
    _Error = namedtuple('Error', 'type message')

    def __init__(self, request_id, timestamp, locale, reason, error):
        self.request_id = request_id
        self.timestamp = timestamp
        self.locale = locale
        self.reason = reason
        self.error = error

    @staticmethod
    def from_json(json_obj):
        error = SessionEndedRequest._Error(json_obj.get('type'),
                                           json_obj.get('message'))
        return SessionEndedRequest(json_obj['requestId'],
                                   json_obj['timestamp'],
                                   json_obj['locale'],
                                   json_obj.get('dialogState'),
                                   error)


class AudioPlayer:
    def __init__(self, token, offset_in_milliseconds, player_activity):
        self.token = token
        self.offset_in_milliseconds = offset_in_milliseconds
        self.player_activity = player_activity

    @staticmethod
    def from_json(json_obj):
        return AudioPlayer(json_obj.get('token'),
                           json_obj.get('offsetInMilliseconds'),
                           json_obj.get('playerActivity'))

    def to_json(self):
        ap_dict = {
            'token': self.token,
            'offsetInMilliseconds': self.offset_in_milliseconds,
            'playerActivity': self.player_activity
        }
        return {k: v for (k, v) in ap_dict.items() if v is not None}


class AudioPlayerDirective:
    def __init__(self):
        pass
