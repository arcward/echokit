import pytest
import echokit
import json


@pytest.fixture(scope="module")
def set_color_intent_request():
    request = None
    with open("requests/set_color_intent.txt") as f:
        request = json.load(f)
    return request


def test_app_id():
    app = echokit.EchoKit("my_app_id")
    assert app.app_id == "my_app_id"
    app.app_id = "A new one!"
    assert app.app_id == "A new one!"


def test_verify_app_id_override():
    app = echokit.EchoKit("", verify_app_id=False)
    assert app.verify_app_id == False


def test_verify_app_id(set_color_intent_request):
    app = echokit.EchoKit("RandomID")
    @app.intent("MyColorIsIntent")
    def tmp_handler(request, session):
        return app.response("Hi")
    # Application ID in fixture doesn't match, should throw exc
    from echokit.exc import ASKException
    with pytest.raises(ASKException):
        app.handler(set_color_intent_request, {})


