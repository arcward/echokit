import echopy
from echopy import Response, OutputSpeech, SimpleCard


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
    order = event.request.intent.slots['Order'].value
    session_attrs = {'last_order': order}
    response_text = f'You asked me to {order}'
    return Response(output_speech=OutputSpeech(text=response_text),
                    session_attributes=session_attrs)


@echopy.on_intent('CardIntent')
def card_intent(event):
    card_hand = event.request.intent.slots['Suit'].value
    simple_card = SimpleCard(title="Simple", content=f"Played {card_hand}")
    output_speech = OutputSpeech(text=f"Was your card a(n)... {card_hand}?")
    return Response(output_speech=output_speech, card=simple_card)
