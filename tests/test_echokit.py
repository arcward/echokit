import json
from os.path import abspath, dirname, join as join_
from unittest import TestCase
from echokit.echokit import EchoKit


class TestEchoKit(TestCase):
    def setUp(self):
        self.app_id = "RandomAppID123"
        self.app = EchoKit(self.app_id, verify_app_id=False)
        set_color_intent_path = join_(
            dirname(abspath(__file__)),
            'set_color_intent.txt'
        )
        with open(set_color_intent_path) as f:
            self.set_color_intent = json.load(f)

        whats_my_color_intent_path = join_(
            dirname(abspath(__file__)),
            'whats_my_color_intent.txt'
        )
        with open(whats_my_color_intent_path) as f:
            self.whats_my_color_intent = json.load(f)

        multi_slot_intent_path = join_(
            dirname(abspath(__file__)),
            'multi_slot_intent.txt'
        )
        with open(multi_slot_intent_path) as f:
            self.multi_slot_intent = json.load(f)

    def test_set_color_intent(self):
        @self.app.on_intent('MyColorIsIntent')
        @self.app.slot('Color')
        def my_color_is_intent(request, session, Color):
            color = Color
            if not color:
                text = ("I'm not sure what your favorite color is, "
                        "please try again.")
                reprompt = (
                "I'm not sure what your favorite color is. Youc an tell "
                "me your favorite color by saying, my favorite color "
                "is red")
                return self.app.ask(text).reprompt(reprompt)
            text = (f"I now know that your favorite color is {color}. You "
                    f"can ask me what your favorite color is by saying, "
                    f"whats my favorite color?")
            reprompt = (
            "You can ask me your favorite color by saying, what's my "
            "favorite color?")
            return self.app.ask(text).reprompt(reprompt).session_attributes(
                {'Color': color})

        response = self.app.handler(self.set_color_intent, {})
        print(response)

    def test_whats_my_color_intent(self):
        @self.app.on_intent('WhatsMyColorIntent')
        def whats_my_color_intent(request, session):
            color = session.attributes.get('Color')
            if not color:
                return self.app.tell(
                    "I'm not sure what your favorite color is. You can "
                    "say, my favorite color is red")
            return self.app.tell(f"Your favorite color is {color}")

        response = self.app.handler(self.whats_my_color_intent, {})
        print(response)

    def test_multi_slot_intent(self):
        @self.app.on_intent("AnimalColorIntent")
        @self.app.slot("FirstColor", "SecondColor")
        def animal_color_intent(request, session, FirstColor, SecondColor):
            return self.app.tell(f"Your colors were {FirstColor} and {SecondColor}")

        response = self.app.handler(self.multi_slot_intent, {})
        print(response)

    def test_tell(self):
        self.fail()

    def test_ask(self):
        self.fail()

    def test_on_session_launch(self):
        self.fail()

    def test_on_session_ended(self):
        self.fail()

    def test_on_intent(self):
        self.fail()

    def test_slot(self):
        self.fail()

    def test__handler(self):
        self.fail()
