from echokit.requests.standard import models as standard_models
from echokit.requests.audio_player import models as audio_player_models
from echokit.requests.playback_controller import models as \
    playback_controller_models


def is_standard(request):
    return request['type'] in standard_models


def is_intent(request):
    return request['type'] == 'IntentRequest'


def is_audio_player(request):
    return request['type'] in audio_player_models


def is_playback_controller(request):
    return request['type'] in playback_controller_models


def request_type_model(request):
    if request['type'] in standard_models:
        return standard_models[request['type']].from_json(request)
    elif request['type'] in audio_player_models:
        return audio_player_models[request['type']].from_json(request)
    else:
        raise KeyError()
