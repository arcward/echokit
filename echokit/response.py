class Response:
    def __init__(self, speech, speech_type='PlainText', end_session=True,
                 session_attributes=None, version='1.0'):
        self._dict = {
            'version': version,
            'shouldEndSession': end_session,
            'response': {}
        }
        self.speech(speech, speech_type)
        if session_attributes:
            self._dict['sessionAttributes'] = session_attributes
        else:
            self._dict['sessionAttributes'] = {}

    @property
    def end_session(self):
        return self._dict['shouldEndSession']

    @end_session.setter
    def end_session(self, end_session):
        self._dict['shouldEndSession'] = end_session

    @property
    def session_attributes(self):
        return self._dict['sessionAttributes']

    def should_end_session(self, should_end_session):
        self._dict['shouldEndSession'] = should_end_session
        return self

    def _speech(self, speech, type):
        d = {'type': type}
        if type == 'PlainText':
            d['text'] = speech
        elif type == 'SSML':
            d['ssml'] = speech
        else:
            # TODO exception
            raise Exception('')
        return d

    def speech(self, speech, type='PlainText'):
        self._dict['response']['outputSpeech'] = self._speech(speech, type)
        return self

    def reprompt(self, speech, type='PlainText'):
        self._dict['response']['reprompt'] = {
            'outputSpeech': self._speech(speech, type)
        }
        return self

    def simple_card(self, title, content):
        self._dict['response']['card'] = {
            'type': 'Simple',
            'title': title,
            'content': content
        }
        return self

    def standard_card(self, title, text, small_image_url=None,
                      large_image_url=None):
        self._dict['response']['card'] = {
            'type': 'Standard',
            'title': title,
            'text': text
        }
        img = {}
        if small_image_url:
            img['smallImageUrl'] = small_image_url
        if large_image_url:
            img['largeImageUrl'] = large_image_url
        if img:
            self._dict['response']['card']['image'] = img
        return self

    def link_account_card(self, content):
        self._dict['response']['card'] = {
            'type': 'LinkAccount',
            'content': content
        }
        return self
