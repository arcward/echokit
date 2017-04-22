"""Alexa response models

The ``Response`` object is what you'll return to the Alexa service. It 
will contain your ``OutputSpeech``, ``Card``, ``Reprompt``...
"""
from typing import Dict


class Response:
    """Wrapper for response parameters and ``Response``"""
    def __init__(self, output_speech=None, card=None, reprompt=None,
                 should_end_session=None, directives=None,
                 session_attributes=None, version='1.0'):
        """
        :param response: ``Response``
        :param session_attributes: dict of session attributes
        :param version: Default: *1.0*
        """
        self.response: _Response = _Response(output_speech, card, reprompt,
                                             should_end_session, directives)
        self.version: str = version

        if not session_attributes:
            session_attributes = {}
        self.session_attributes: Dict[str, object] = session_attributes

    @property
    def output_speech(self):
        return self.response.output_speech

    @output_speech.setter
    def output_speech(self, output_speech):
        self.response.output_speech = output_speech

    @property
    def card(self):
        return self.response.card

    @card.setter
    def card(self, card):
        self.response.card = card

    @property
    def reprompt(self):
        return self.response.reprompt

    @reprompt.setter
    def reprompt(self, reprompt):
        self.response.reprompt = reprompt

    @property
    def should_end_session(self):
        return self.response.should_end_session

    @should_end_session.setter
    def should_end_session(self, should_end_session):
        self.response.should_end_session = should_end_session

    @property
    def directives(self):
        return self.response.directives

    @directives.setter
    def directives(self, directives):
        self.response.directives = directives

    def to_json(self):
        return {
            'version': self.version,
            'response': self.response.to_json(),
            'sessionAttributes': self.session_attributes or {}
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
        self.directives: list[object] = directives

    def to_json(self):
        response_dict = {'shouldEndSession': self.should_end_session,
                         'directives': self.directives}

        if self.output_speech:
            response_dict['outputSpeech'] = self.output_speech.to_json()

        if self.card:
            response_dict['card'] = self.card.to_json()

        if self.reprompt:
            response_dict['reprompt'] = self.reprompt.to_json()

        return {k: v for (k, v) in response_dict.items() if v is not None}


class PlainTextOutputSpeech:
    def __init__(self, text):
        self.type = 'PlainText'
        self.text = text

    def to_json(self):
        return self.__dict__


class SSMLOutputSpeech:
    def __init__(self, ssml):
        self.type = 'ssml'
        self.ssml = ssml

    def to_json(self):
        return self.__dict__


class SimpleCard:
    """Simple card, supporting only *title* and *content*"""
    type = 'Simple'

    def __init__(self, title=None, content=None):
        self.title = title
        self.content = content

    def to_json(self):
        return self.__dict__


class StandardCard:
    """Standard card, supporting title/text and a (small/large) image"""
    type = 'Standard'

    def __init__(self, title=None, text=None, small_image_url=None,
                 large_image_url=None):
        self.title = title
        self.text = text
        self.small_image_url = small_image_url
        self.large_image_url = large_image_url

    @property
    def image(self):
        """If any image URL is provided, return dict, otherwose None"""
        if not (self.small_image_url or self.large_image_url):
            return None
        img = {}
        if self.small_image_url:
            img['smallImageUrl'] = self.small_image_url
        if self.large_image_url:
            img['largeImageUrl'] = self.large_image_url
        return img

    def to_json(self):
        card_dict = {'type': self.type}
        if self.title:
            card_dict['title'] = self.title
        if self.text:
            card_dict['text'] = self.text
        if self.image:
            card_dict['image'] = self.image
        return card_dict


class LinkAccountCard:
    """LinkAccount card, supporting only *content*"""
    type = 'LinkAccount'

    def __init__(self, content=None):
        self.content = content

    def to_json(self):
        return self.__dict__


class Reprompt:
    """Reprompt, only in respones to ``LaunchRequest`` or ``IntentRequest``"""
    def __init__(self, output_speech):
        """
        :param output_speech: ``PlainTextOutputSpeech`` or ``SSMLOutputSpeech``
        """
        self.output_speech = output_speech

    def to_json(self):
        rp_dict = {}
        if self.output_speech:
            rp_dict['outputSpeech'] = self.output_speech.to_json()
        return rp_dict
