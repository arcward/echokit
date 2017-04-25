import re
from pprint import pprint

pause_json = {

  "session": {
    "sessionId": "SessionId.3cec3682-31b1-41e1-bb59-c9a0c2ddae6e",
    "application": {
      "applicationId": "amzn1.ask.skill.3c392942-8efb-48a1-89ff-05af9eaa9c5e"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AEZQUQ4CYZSKQRADTPB4FQBYX6EI4DSLHE3VAAEQX3PE33EEWZOPUJY46NFKC4PW77CYQ7DXQNZJND2ANCYBX7SU5AZ2XXSSHGIVQBWUKUZPTPR4PIFZHF2BCHKBWKIG5V7WNFQO4POJHJQXJZAGA7GBF452E4F3A2H5XV4RGSSJPG47UM72R7G2IDKZMZ2G42ZVQ5C5BDINIEY"
    },
    "new": True
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.d580a39d-f090-46ca-9f67-b12b98ab3f3c",
    "locale": "en-US",
    "timestamp": "2017-04-24T14:49:11Z",
    "intent": {
      "name": "AMAZON.PauseIntent",
      "slots": {}
    }
  },
  "version": "1.0"
}


def _convert_case(alexa_dict, conversion_func, indent='  '):
    for k, v in dict(alexa_dict).items():
        alexa_dict[conversion_func(k)] = alexa_dict.pop(k)
        #print(f'{indent}{k}')
        if isinstance(v, dict):
            _convert_case(v, conversion_func, indent+'  ')


def convert_keys(alexa_dict):
    _convert_case(alexa_dict, to_snake_case)


def revert_keys(alexa_dict):
    _convert_case(alexa_dict, to_camel_case())


def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(name):
    for match in re.finditer('(_)([a-z])', name):
        underscore, letter = match.group(0)
        name = list(name)
        name[match.start()+1] = letter.upper()
    return ''.join([n for n in name if n != '_'])


