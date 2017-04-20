import echopy
from echopy import Response, OutputSpeech


def handler(event, context):
    return echopy.handler(event, context)

echopy.application_id = "amzn1.ask.skill.8e45280b-d9ce-4a48-a1c9-f77f07925a14"


@echopy.on_session_launch
def session_started(event):
    output_speech = echopy.OutputSpeech(text="Test!")
    return echopy.Response(output_speech=output_speech)


@echopy.on_session_end
def session_ended(event):
    output_speech = echopy.OutputSpeech("Seeya!")
    return echopy.Response(output_speech=output_speech)


@echopy.on_intent('SomeIntent')
def on_intent(event):
    output_speech = OutputSpeech(text="Intent woo!")
    return Response(output_speech=output_speech)


@echopy.on_intent('SpecificIntent')
def specific_intent(event):
    response_text = (f"You asked me to "
                     f"{event.request.intent.slots['Order'].value}")
    return Response(output_speech=OutputSpeech(text=response_text))