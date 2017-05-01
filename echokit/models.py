"""Models/classes for interpreting requests and generating responses"""


class _ASKObject(dict):
    """Base class for objects found in requests/sent as responses"""
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        for k, v in dict(kwargs).items():
            if isinstance(v, dict):
                v = _ASKObject(**v)
            self[k] = v

    def _dict(self):
        """Convert all attributes to dict"""
        d = dict(self)
        for k, v in dict(d).items():
            if isinstance(v, _ASKObject):
                d[k] = v._dict()
            elif v is None:
                del d[k]
        return d

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, attr):
        return self.get(attr)


# noinspection PyPep8Naming
class _Response(_ASKObject):
    """Response object contained in response body"""
    def __init__(self, outputSpeech=None, card=None, reprompt=None,
                 shouldEndSession=None, directives=None):
        super().__init__(outputSpeech=outputSpeech, reprompt=reprompt,
                         card=card, shouldEndSession=shouldEndSession,
                         directives=directives)


class ASKResponse(_ASKObject):
    """Response body"""
    def __init__(self, response=None, session_attributes=None, version='1.0',
                 speech=None, ssml=None, should_end_session=None,
                 reprompt=None):
        """
        :param response: ``_Response`` object
        :param session_attributes: dict
        :param version: 
        :param speech: Speech (if plaintext)
        :param ssml: Speech (if SSML)
        :param should_end_session: True or False
        :param reprompt: Reprompt speech (same format as speech/SSML)
        """
        if not response:
            response = _Response()
        super().__init__(response=response, version=version,
                         sessionAttributes=session_attributes)
        self.sessionAttributes = {}
        if session_attributes:
            self.session_attributes(session_attributes)
        if should_end_session is not None:
            self.should_end_session(should_end_session)
        if speech:
            self.speech(speech)
        if ssml:
            self.ssml(ssml)
        if reprompt and speech:
            self.reprompt(reprompt, ssml=False)
        elif reprompt and ssml:
            self.reprompt(reprompt, ssml=True)

    def should_end_session(self, end_session):
        """Set *response['shouldEndSession']*"""
        self.response.shouldEndSession = end_session
        return self

    def session_attributes(self, session_attributes):
        """Set *sessionAttributes* (dict)"""
        self.sessionAttributes = session_attributes
        return self

    def simple_card(self, title=None, content=None):
        """Set *response['card']* to a *Simple* type card"""
        self.response.card = _Card(type='Simple', title=title, content=content)
        return self

    def standard_card(self, title=None, text=None, small_image_url=None,
                      large_image_url=None):
        """Set *response['card']* to a *Standard* type card"""
        self.response.card = _Card(type='Standard', title=title, text=text,
                                   image={'smallImageUrl': small_image_url,
                                          'largeImageUrl': large_image_url})
        return self

    def link_account_card(self, content=None):
        """Set *response['card'] to a *LinkAccount* type card"""
        self.response.card = _Card(type='LinkAccount', content=content)
        return self

    def reprompt(self, speech, ssml=False):
        """Set *response['reprompt']*"""
        self.response.reprompt = self._speech(speech, ssml)
        return self

    @staticmethod
    def _speech(speech, ssml=False):
        """Create an *OutputSpeech* object
        
        :param speech: Speech in either plaintext or SSML format
        :param ssml: *True* if speech is in SSML format, *False* if 
            plaintext (default: *False*)
        :return: *OutputSpeech* object
        """
        if ssml:
            return _ASKObject(type='SSML', ssml=speech)
        else:
            return _ASKObject(type='PlainText', text=speech)

    def speech(self, text, ssml=False):
        """Set *response['outputSpeech']

        :param text: 
        :param ssml: *True* if speech string is in SSML format, *False* 
            if plaintext. (Default: *False*)
        :return: self
        """
        self.response.outputSpeech = self._speech(text, ssml)
        return self

    def ssml(self, ssml):
        """Set *response['outputSpeech'] to an *SSML* type"""
        self.response.outputSpeech = self._speech(ssml, True)
        return self


# noinspection PyShadowingBuiltins
class _Card(_ASKObject):
    """Base class for cards"""
    def __init__(self, type, **kwargs):
        """
        :param type: *Simple*, *Standard* or *LinkAccount*
        :param kwargs: For Simple cards: *title, content*. 
            
            For *Standard* cards: *title*, *text*, *smallImageUrl*, 
            *largeImageUrl*.
            
            For *LinkAccount* cards: *content*
        """
        super().__init__(type=type, **kwargs)
