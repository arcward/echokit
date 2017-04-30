"""Alexa response models

The ``Response`` object is what you'll return to the Alexa service. It 
will contain your ``OutputSpeech``, ``Card``, ``Reprompt``...
"""
from echokit.models import ASKResponse


def ask(speech, reprompt=None, ssml=False):
    if ssml:
        response = ASKResponse(ssml=speech, reprompt=reprompt,
                               should_end_session=False)
    else:
        response = ASKResponse(speech=speech,  reprompt=reprompt,
                               should_end_session=False)
    return response


def tell(speech, ssml=False):
    if ssml:
        response = ASKResponse(ssml=speech, should_end_session=True)
    else:
        response = ASKResponse(speech=speech, should_end_session=True)
    return response


class AudioPlayerResponse:
    def __init__(self, version, directives):
        self.version = version
        self.directives = directives

    def _dict(self):
        return {'version': self.version,
                'directives': [d._dict() for d in self.directives]}
