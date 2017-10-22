"""Module to build responses to requests"""


class Response:
    """
    Response builder

    For example:

    .. code-block:: python

        response = Response("Is that Springfield Ohio, or Springfield Illinois?")
        response.reprompt("I didn't catch that. Was that Ohio or Illinois?")
        response.end_session = False
        return response


    """
    def __init__(self, speech, speech_type='PlainText', end_session=True,
                 session_attributes=None, version='1.0'):
        """

        :param speech: Speech to include with the response
        :param speech_type: *PlainText* or *SSML*, defining the content
            type passed to :attr:`speech`
        :param end_session: *True* if this response should end the session,
            or *False* if it should remain open
        :param session_attributes: Session attributes to persist
        :type session_attributes: dict
        :param version:
        """
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
        """The *shouldEndSession* attribute of the response"""
        return self._dict['shouldEndSession']

    @end_session.setter
    def end_session(self, end_session):
        self._dict['shouldEndSession'] = end_session

    @property
    def session_attributes(self):
        """Dictionary of session attributes to persist"""
        return self._dict['sessionAttributes']

    # TODO Investigate why setting @staticmethod on ._speech breaks .speech
    def _speech(self, speech, speech_type):
        """Include speech with the response

        :param speech: Speech text
        :type speech: str
        :param speech_type: *PlainText* or *SSML* (if passing a
            string with SSML)
        :return:
        """
        d = {'type': speech_type}
        if speech_type == 'PlainText':
            d['text'] = speech
        elif speech_type == 'SSML':
            d['ssml'] = speech
        else:
            # TODO exception
            raise Exception('')
        return d

    def speech(self, speech, speech_type='PlainText'):
        """Sets *outputSpeech* for the response

        :param speech: Speech text
        :param speech_type: *PlainText* or *SSML*
        :return:
        """
        self._dict['response']['outputSpeech'] = self._speech(speech, speech_type)
        return self

    def reprompt(self, speech, speech_type='PlainText'):
        """Include a reprompt in the response

        :param speech: Speech text
        :param speech_type: *PlainText* or *SSML*
        :return:
        """
        self._dict['response']['reprompt'] = {
            'outputSpeech': self._speech(speech, speech_type)
        }
        return self

    def simple_card(self, title, content):
        """Include a *SimpleCard* in the response

        :param title: Card title
        :param content: Card content (text)
        :return:
        """
        self._dict['response']['card'] = {
            'type': 'Simple',
            'title': title,
            'content': content
        }
        return self

    def standard_card(self, title, text, small_image_url=None,
                      large_image_url=None):
        """Include a *StandardCard* in the response

        :param title: Card title
        :param text: Card text (body)
        :param small_image_url: URL to small image (see Alexa docs)
        :param large_image_url: URL to large image (see Alexa docs)
        :return:
        """
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
        """Include a *LinkAccountCard* in the response

        :param content: Card content
        :type content: str
        :return:
        """
        self._dict['response']['card'] = {
            'type': 'LinkAccount',
            'content': content
        }
        return self
