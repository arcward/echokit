from enum import Enum


class ASKObject:
    def __init__(self, **kwargs):
        for k, v in dict(kwargs).items():
            if isinstance(v, dict):
                setattr(self, k, ASKObject(**v))
            else:
                setattr(self, k, v)

    def _dict(self):
        d = self.__dict__
        for k, v in dict(d).items():
            if isinstance(v, ASKObject):
                d[k] = v._dict()
        return d


class ASKRequest(ASKObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _Response(ASKObject):
    def __init__(self, outputSpeech=None, card=None, reprompt=None,
                 shouldEndSession=None, directives=None):
        self.outputSpeech = outputSpeech
        self.card = card
        self.reprompt = reprompt
        self.shouldEndSession = shouldEndSession
        if not directives:
            directives = []
        self.directives = directives


class AudioPlayerResponse(ASKObject):
    def __init__(self, directives, version='1.0'):
        if not directives:
            directives = []
        super().__init__(directives=directives, version=version)

    play = ASKResponse.play_audio
    stop = ASKResponse.stop_audio
    clear_queue = ASKResponse.clear_queue


class ASKResponse(ASKObject):
    def __init__(self, response=None, session_attributes=None, version='1.0',
                 speech=None, ssml=None, should_end_session=None,
                 reprompt=None):
        if not response:
            response = _Response()
        super().__init__(response=response, version=version,
                         sessionAttributes=session_attributes)
        if speech:
            self.speech(speech)
        if ssml:
            self.ssml(ssml)
        if reprompt:
            self.reprompt(reprompt)
        if should_end_session is not None:
            self.should_end_session(should_end_session)

    def should_end_session(self, end_session):
        self.response.shouldEndSession = end_session
        return self

    def session_attributes(self, session_attributes):
        self.sessionAttributes = session_attributes
        return self

    def simple_card(self, title=None, content=None):
        self.response.card = Card(type='Simple', title=title, content=content)
        return self

    def standard_card(self, title=None, text=None, small_image_url=None,
                      large_image_url=None):
        self.response.card = Card(type='Standard', title=title, text=text,
                                  image={'smallImageUrl': small_image_url,
                                         'largeImageUrl': large_image_url})
        return self

    def link_account_card(self, content=None):
        self.response.card = Card(type='LinkAccount', content=content)
        return self

    def reprompt(self, speech, ssml=False):
        self.response.reprompt = ASKObject(outputSpeech=self.__speech(speech,
                                                                      ssml))
        return self

    def speech(self, text):
        return ASKObject(type='PlainText', text=text)

    def ssml(self, ssml):
        return ASKObject(type='SSML', ssml=ssml)

    def play_audio(self, behavior, url, token, offset_in_milliseconds=0,
                   expected_previous_token=None):
        audio_item = {
            'audioItem':
                {'stream': {
                    'url': url,
                    'token': token,
                    'offsetInMilliseconds': offset_in_milliseconds,
                    'expectedPreviousToken': expected_previous_token
                }}
        }
        directive = Directive(type='AudioPlayer.Play', playBehavior=behavior,
                              audioItem=audio_item)
        self.response.directives.append(directive)
        return self

    def stop_audio(self):
        self.response.directives.append(Directive(type='AudioPlayer.Stop'))
        return self

    def clear_audio_queue(self, behavior):
        self.response.directives\
            .append(ASKObject(type='AudioPlayer.ClearQueue',
                              clearBehavior=behavior.value))
        return self


class Card(ASKObject):
    def __init__(self, type, **kwargs):
        super().__init__(type=type, **kwargs)


class PlayBehavior(Enum):
    ENQUEUE = 'ENQUEUE'
    REPLACE_ALL = 'REPLACE_ALL'
    REPLACE_ENQUEUED = 'REPLACE_ENQUEUED'


class ClearBehavior(Enum):
    CLEAR_ENQUEUED = 'CLEAR_ENQUEUED'
    CLEAR_ALL = 'CLEAR_ALL'


class Directive(ASKObject):
    def __init__(self, type, **kwargs):
        self.type = type
        super().__init__(**kwargs)


