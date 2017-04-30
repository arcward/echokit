"""Alexa response models

The ``Response`` object is what you'll return to the Alexa service. It 
will contain your ``OutputSpeech``, ``Card``, ``Reprompt``...
"""
from echokit.models import _Response, ASKResponse


def ask(speech, reprompt=None):
    return ASKResponse(speech=speech,  reprompt=reprompt,
                       should_end_session=False)


def tell(speech):
    return ASKResponse(speech=speech, should_end_session=True)


class AudioPlayerResponse:
    def __init__(self, version, directives):
        self.version = version
        self.directives = directives

    def _dict(self):
        return {'version': self.version,
                'directives': [d._dict() for d in self.directives]}
