class ResponseBody:
    def __init__(self, response, session_attributes=None, version='1.0'):
        self.response = response
        self.session_attributes = session_attributes
        self.version = version

    def to_json(self):
        resp_json = {'version': self.version,
                     'response': self.response.to_json()}
        if self.session_attributes:
            resp_json['sessionAttributes'] = self.session_attributes
        return resp_json


class Response:
    def __init__(self, output_speech=None, card=None, reprompt=None,
                 should_end_session=None, directives=None):
        self.output_speech = output_speech
        self.card = card
        self.reprompt = reprompt
        self.should_end_session = should_end_session
        self.directives = directives

    @staticmethod
    def from_json(json_obj):
        output_speech = json_obj.get('outputSpeech')
        if output_speech:
            output_speech = OutputSpeech.from_json(output_speech)

        reprompt = json_obj.get('reprompt')
        if reprompt:
            reprompt = Reprompt.from_json(reprompt)

        card = json_obj.get('card', {})
        card_type = card.get('type')
        if card_type == 'Simple':
            card = SimpleCard.from_json(card)
        elif card_type == 'Standard':
            card = StandardCard.from_json(card)
        elif card_type == 'LinkAccount':
            card = LinkAccountCard.from_json(card)

        return Response(output_speech, card, reprompt,
                        json_obj.get('shouldEndSession'),
                        json_obj.get('directives'))

    def to_json(self):
        response_dict = {
            'shouldEndSession': self.should_end_session,
            'directives': self.directives
        }
        if self.output_speech:
            response_dict['outputSpeech'] = self.output_speech.to_json()

        if self.card:
            response_dict['card'] = self.card.to_json()

        if self.reprompt:
            response_dict['reprompt'] = self.reprompt.to_json()

        return {k: v for (k, v) in response_dict.items() if v is not None}


class OutputSpeech:
    def __init__(self, type='PlainText', text=None, ssml=None):
        self.type = type  #: PlainText or SSML
        self.text = text  #: Required if PlainText
        self.ssml = ssml  #: Required if SSML

    @staticmethod
    def from_json(json_obj):
        return OutputSpeech(json_obj.get('type'), json_obj.get('text'),
                            json_obj.get('ssml'))

    def to_json(self):
        speech_dict = {'type': self.type}
        if self.type == 'PlainText':
            speech_dict['text'] = self.text
        elif self.type == 'SSML':
            speech_dict['ssml'] = self.ssml
        return speech_dict


class SimpleCard:
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


class StandardCard:
    card_type = 'Standard'

    def __init__(self, title=None, text=None, small_image_url=None,
                 large_image_url=None):
        self.title = title
        self.text = text
        self.small_image_url = small_image_url
        self.large_image_url = large_image_url

    @property
    def image(self):
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
    card_type = 'LinkAccount'

    def __init__(self, content=None):
        self.content = content

    def to_json(self):
        link_dict = {'type': self.card_type}
        if self.content:
            link_dict['content'] = self.content
        return link_dict


class Reprompt:
    """Only in respones to ``LaunchRequest`` or ``IntentRequest``"""
    def __init__(self, output_speech=None):
        self.output_speech = output_speech

    @staticmethod
    def from_json(json_obj):
        return Reprompt(OutputSpeech.from_json(json_obj.get('outputSpeech')))

    def to_json(self):
        rp_dict = {}
        if self.output_speech:
            rp_dict['outputSpeech'] = self.output_speech.to_json()
        return rp_dict
