import echopy


def handler(event, context):
    return echopy.handler(event, context)

echopy.application_id = 'amzn1.ask.skill.[unique-value-here]'


@echopy.on_session_launch
def session_started(event):
    output_speech = echopy.OutputSpeech(text="Test!")
    return echopy.Response(output_speech=output_speech)


@echopy.on_session_end
def session_ended(event):
    output_speech = echopy.OutputSpeech("Seeya!")
    return echopy.Response(output_speech=output_speech)


@echopy.on_intent('SomeIntent')
def some_intent(event):
    output_speech = echopy.OutputSpeech("Some intent thing!")
    return echopy.Response(output_speech=output_speech)
