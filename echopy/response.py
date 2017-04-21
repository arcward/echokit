"""Alexa response models

The ``Response`` object is what you'll return to the Alexa service. It 
will contain your ``OutputSpeech``, ``Card``, ``Reprompt``...
"""
from typing import Dict


class Response:
    """Container for response parameters and ``ResponseObject``"""
    def __init__(self, output_speech=None, card=None, reprompt=None,
                 should_end_session=None, directives=None,
                 session_attributes=None, version='1.0'):
        """
        
        :param output_speech: ``OutputSpeech`` object
        :param card: ``Card`` object
        :param reprompt: ``Reprompt`` object
        :param should_end_session: ``True`` or ``False``
        :param directives: Array of device-level directives 
            (such as for ``AudioPlayer``)
        :param session_attributes: dict of session attributes
        :param version: Default: *1.0*
        """
        self.response = ResponseObject(output_speech, card, reprompt,
                                       should_end_session, directives)
        self.version: str = version
        self.session_attributes: Dict[str, object] = session_attributes

    def to_json(self):
        resp_dict = {'version': self.version,
                     'response': self.response.to_json()}
        if self.session_attributes:
            resp_dict['sessionAttributes'] = self.session_attributes
        return resp_dict


class ResponseObject:
    """Response object inside response body. Instantiated by ``Response``"""
    def __init__(self, output_speech=None, card=None, reprompt=None,
                 should_end_session=None, directives=None):
        self.output_speech = output_speech
        self.card = card
        self.reprompt = reprompt
        self.should_end_session = should_end_session
        self.directives = directives

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


class OutputSpeech:
    def __init__(self, text=None, ssml=None, type='PlainText', ):
        """
        
        :param type: *PlainText* or *SSML*. If *PlainText*, then 
            the ``text`` parameter must be passed. If *SSML*, then 
            pass ``ssml``. Default: *PlainText* 
        :param text: *PlainText* response
        :param ssml: SSML response
        """
        self.type: str = type  #: PlainText or SSML
        self.text: str = text  #: Required if PlainText
        self.ssml: str = ssml  #: Required if SSML

    def to_json(self):
        speech_dict = {'type': self.type}
        if self.type == 'PlainText':
            speech_dict['text'] = self.text
        elif self.type == 'SSML':
            speech_dict['ssml'] = self.ssml
        return speech_dict


class SimpleCard:
    """Simple card, supporting only *title* and *content*"""
    card_type = 'Simple'

    def __init__(self, title=None, content=None):
        self.title = title
        self.content = content

    def to_json(self):
        simple_dict = {'type': self.card_type}
        if self.title:
            simple_dict['title'] = self.title
        if self.content:
            simple_dict['content'] = self.content
        return simple_dict


class StandardCard:
    """Standard card, supporting title/text and a (small/large) image"""
    card_type = 'Standard'

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
        card_dict = {'type': self.card_type}
        if self.title:
            card_dict['title'] = self.title
        if self.text:
            card_dict['text'] = self.text
        if self.image:
            card_dict['image'] = self.image
        return card_dict


class LinkAccountCard:
    """LinkAccount card, supporting only *content*"""
    card_type = 'LinkAccount'

    def __init__(self, content=None):
        self.content = content

    def to_json(self):
        link_dict = {'type': self.card_type}
        if self.content:
            link_dict['content'] = self.content
        return link_dict


class Reprompt:
    """Reprompt, only in respones to ``LaunchRequest`` or ``IntentRequest``"""
    def __init__(self, output_speech=None):
        self.output_speech = output_speech

    def to_json(self):
        rp_dict = {}
        if self.output_speech:
            rp_dict['outputSpeech'] = self.output_speech.to_json()
        return rp_dict
