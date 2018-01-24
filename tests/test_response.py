import pytest
from echokit.response import Response


class TestSpeech:
    def test_plaintext_text(self):
        text = "Plaintext speech"
        response = Response(text)
        assert response._dict["response"]["outputSpeech"]["text"] == text

    def test_plaintext_type(self):
        response = Response("")
        type_ = response._dict["response"]["outputSpeech"]["type"]
        assert type_ == "PlainText"

    def test_ssml_type(self):
        response = Response("", speech_type="SSML")
        assert response._dict["response"]["outputSpeech"]["type"] == "SSML"


class TestReprompt:
    def test_plaintext_text(self):
        text = "Plaintext speech"
        response = Response("").reprompt(text)
        output_speech = response._dict["response"]["reprompt"]["outputSpeech"]
        assert output_speech["text"] == text

    def test_plaintext_type(self):
        response = Response("").reprompt("")
        type_ = response._dict["response"]["reprompt"]["outputSpeech"]["type"]
        assert type_ == "PlainText"

    def test_plaintext_type(self):
        response = Response("").reprompt("", speech_type="SSML")
        type_ = response._dict["response"]["reprompt"]["outputSpeech"]["type"]
        assert type_ == "SSML"


def test_session_attributes():
    attrs = {"color": "red"}
    response = Response("")
    response.session_attributes["color"] = "red"
    assert attrs == response._dict["sessionAttributes"]


def test_simple_card():
    response = Response("").simple_card("Title!", "Some content!")
    expected = {
        "type": "Simple",
        "title": "Title!",
        "content": "Some content!"
    }
    assert response._dict["response"]["card"] == expected


def test_standard_card():
    card_kwargs = {
        "title": "Title!",
        "text": "Some text!",
        "small_image_url": "https://i.imgur.com/f4lGkbD.gif",
        "large_image_url": "https://i.imgur.com/erkEpHh.jpg"
    }
    response = Response("").standard_card(**card_kwargs)
    expected = {
        "type": "Standard",
        "title": card_kwargs["title"],
        "text": card_kwargs["text"],
        "image": {
            "smallImageUrl": card_kwargs["small_image_url"],
            "largeImageUrl": card_kwargs["large_image_url"]
        }
    }
    assert response._dict["response"]["card"] == expected


def test_link_account_card():
    response = Response("").link_account_card("Some content!")
    expected = {
        "type": "LinkAccount",
        "content": "Some content!"
    }
    assert response._dict["response"]["card"] == expected


def test_end_session():
    response = Response("")
    assert response.end_session == True
    assert response._dict["response"]["shouldEndSession"] == True

    response.end_session = False
    assert response.end_session == False
    assert response._dict["response"]["shouldEndSession"] == False

def test_version():
    response = Response("")
    assert response._dict["version"] == "1.0"


def test_response_structure():
    response = Response("Hello!")
    response.session_attributes["who_loves_orange_soda"] = "kel_does"
    expected = {
        "version": "1.0",
        "sessionAttributes": {"who_loves_orange_soda": "kel_does"},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Hello!",
            },
            "shouldEndSession": True,
        }
    }
    assert response._dict == expected
