"""Alexa response models

The ``Response`` object is what you'll return to the Alexa service. It 
will contain your ``OutputSpeech``, ``Card``, ``Reprompt``...
"""


class Response:
    """Wrapper for response parameters and ``Response``"""

    def __init__(self, output_speech=None, card=None, reprompt=None,
                 should_end_session=None, session_attributes=None,
                 directives=None, version='1.0'):
        """

        :param output_speech: ``PlainTextOutputSpeech`` or ``SSMLOutputSpeech``
        :param card: ``SimpleCard``, ``StandardCard`` or ``LinkAccountCard``
        :param reprompt: ``Reprompt``
        :param should_end_session:  ``True`` or ``False``
        :param directives: List of directives
        :param session_attributes: dict of session attributes [str, object]
        :param version: Default: *1.0*
        """
        self.response: _Response = _Response(output_speech, card, reprompt,
                                             should_end_session, directives)
        self.version: str = version
        if not session_attributes:
            session_attributes = {}
        self.session_attributes = session_attributes

    @property
    def output_speech(self):
        """``PlainTextOutputSpeech`` or ``SSMLOutputSpeech``"""
        return self.response.output_speech

    @output_speech.setter
    def output_speech(self, output_speech):
        self.response.output_speech = output_speech

    @property
    def card(self):
        """``SimpleCard``, ``StandardCard`` or ``LinkAccountCard``"""
        return self.response.card

    @card.setter
    def card(self, card):
        self.response.card = card

    @property
    def reprompt(self):
        """``Reprompt``"""
        return self.response.reprompt

    @reprompt.setter
    def reprompt(self, reprompt):
        self.response.reprompt = reprompt

    @property
    def should_end_session(self):
        """``True`` or ``False``"""
        return self.response.should_end_session

    @should_end_session.setter
    def should_end_session(self, should_end_session):
        self.response.should_end_session = should_end_session

    @property
    def directives(self):
        """List of directives"""
        return self.response.directives

    @directives.setter
    def directives(self, directives):
        self.response.directives = directives

    def _dict(self):
        return {
            'session_attributes': self.session_attributes,
            'version': self.version,
            'response': self.response._dict()
        }

    def to_json(self):
        return {
            'version': self.version,
            'response': self.response.to_json(),
            'sessionAttributes': self.session_attributes
        }


class AudioPlayerResponse:
    def __init__(self, version, directives):
        self.version = version
        self.directives = directives

    def _dict(self):
        return {
            'version': self.version,
            'directives': [d._dict() for d in self.directives]
        }


class _Response:
    """``Response`` object in actual API response"""

    def __init__(self, output_speech=None, card=None, reprompt=None,
                 should_end_session=None, directives=None):
        """
        :param output_speech: ``PlainTextOutputSpeech`` or ``SSMLOutputSpeech``
        :param card: ``SimpleCard``, ``StandardCard`` or ``LinkAccountCard``
        :param reprompt: ``Reprompt``
        :param should_end_session: ``True`` or ``False``
        :param directives: 
        """
        self.output_speech = output_speech
        self.card = card
        self.reprompt: Reprompt = reprompt
        self.should_end_session: bool = should_end_session
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

    def to_json(self):
        response_dict = {
            'shouldEndSession': self.should_end_session,
            'directives': []
        }
        if self.output_speech:
            response_dict['outputSpeech'] = self.output_speech._dict()
        if self.card:
            response_dict['card'] = self.card._dict()
        if self.reprompt:
            response_dict['reprompt'] = self.reprompt._dict()
        if self.directives:
            response_dict['directives'] = [d._dict() for d in
                                           self.directives]
        return {k: v for (k, v) in response_dict.items() if v is not None}


class Reprompt:
    """Reprompt, only in respones to ``LaunchRequest`` or ``IntentRequest``"""

    def __init__(self, output_speech):
        """
        :param output_speech: ``PlainTextOutputSpeech`` or ``SSMLOutputSpeech``
        """
        self.output_speech = output_speech

    def _dict(self):
        rp_dict = {}
        if self.output_speech:
            rp_dict['outputSpeech'] = self.output_speech._dict()
        return rp_dict
