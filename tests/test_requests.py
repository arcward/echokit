from unittest import TestCase
import json
from echopy import request

request_body = {
  "version": "string",
  "session": {
    "new": True,
    "sessionId": "string",
    "application": {
      "applicationId": "string"
    },
    "attributes": {
      "string": {}
    },
    "user": {
      "userId": "string",
        "permissions": {
          "consentToken": "string"
      },
      "accessToken": "string"
    }
  },
  "context": {
    "System": {
      "application": {
        "applicationId": "string"
      },
      "user": {
        "userId": "string",
        "permissions": {
          "consentToken": "string"
      },
        "accessToken": "string"
      },
      "device": {
        "deviceId": "string",
        "supportedInterfaces": {
          "AudioPlayer": {}
        }
      },
      "apiEndpoint": "string"
    },
    "AudioPlayer": {
      "token": "string",
      "offsetInMilliseconds": 0,
      "playerActivity": "string"
    }
  },
  "request": {}
}


class TestRequests(TestCase):
    def setUp(self):
        self.json_str = json.dumps(request_body)
        self.json_dict = json.loads(self.json_str)

    def test_from_json(self):
        req = request.Request.from_json(self.json_dict)
        print('')
