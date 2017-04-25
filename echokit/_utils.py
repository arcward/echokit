import re


def _convert_case(alexa_dict, conversion_func):
    for k, v in dict(alexa_dict).items():
        alexa_dict[conversion_func(k)] = alexa_dict.pop(k)
        if k != 'session_attributes':
            if isinstance(v, dict):
                _convert_case(v, conversion_func)


def convert_keys(alexa_dict):
    _convert_case(alexa_dict, to_snake_case)


def revert_keys(alexa_dict):
    _convert_case(alexa_dict, to_camel_case)


def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(name):
    if name == 'system':
        return 'System'
    elif name == 'audio_player':
        return 'AudioPlayer'

    for match in re.finditer('(_)([a-z])', name):
        underscore, letter = match.group(0)
        name = list(name)
        name[match.start()+1] = letter.upper()
    return ''.join([n for n in name if n != '_'])


def enum_contains(value, enum_container):
    return value in [e.value for e in enum_container]