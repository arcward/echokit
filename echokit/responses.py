"""Alexa response models

The ``Response`` object is what you'll return to the Alexa service. It 
will contain your ``OutputSpeech``, ``Card``, ``Reprompt``...
"""
from echokit.models import _Response, ASKResponse


def ask(speech, reprompt_speech):
    return ASKResponse(speech=speech,  reprompt=reprompt_speech,
                       should_end_session=False)


def tell(speech, card_title=None, card_content=None):
    return ASKResponse(speech=speech).simple_card(card_title, card_content)


def audio_player()

class AudioPlayerResponse:
    def __init__(self, version, directives):
        self.version = version
        self.directives = directives

    def _dict(self):
        return {'version': self.version,
                'directives': [d._dict() for d in self.directives]}


class _Response:
    """``Response`` object in actual API response"""
    def __init__(self, outputSpeech=None, card=None, reprompt=None,
                 shouldEndSession=None, directives=None):
        """
        :param output_speech: ``PlainTextOutputSpeech`` or ``SSMLOutputSpeech``
        :param card: ``SimpleCard``, ``StandardCard`` or ``LinkAccountCard``
        :param reprompt: ``Reprompt``
        :param should_end_session: ``True`` or ``False``
        :param directives: 
        """
        self.outputSpeech = outputSpeech
        self.card = card
        self.reprompt: Reprompt = reprompt
        self.shouldEndSession: bool = shouldEndSession
        self.directives = directives

    def _dict(self):
        d = {'should_end_session': self.should_end_session}
        if self.output_speech is not None:
            d['output_speech'] = self.output_speech._dict()
        if self.card is not None:
            d['card'] = self.card._dict()
        if self.reprompt is not None:
            d['reprompt'] = self.reprompt._dict()
        if self.directives is not None:
            d['directives'] = [apd._dict() for apd in self.directives]
        return d


