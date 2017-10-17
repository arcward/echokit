"""Deserialization of incoming requests"""


class ASKRequest(dict):
    """Class to deserialize and access data for incoming requests

    Allows access to request data via dot notation by dynamically
    assigning attributes. Hopefully allows more graceful handling
    of requests in the face of possible future request structure
    changes. From the official Alexa Skills Kit documentation:

    *Important: Future versions of the Alexa Skills Kit may add new
    properties to the JSON request and response formats, while
    maintaining backward compatibility for the existing properties.
    Your code must be resilient to these types of changes. For example,
    your code for deserializing a JSON request must not break when it
    encounters a new, unknown property.*
    """
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        # Any value found to be another object/dict is
        # created as another `ASKObject`, which follows
        # the same initialization, recursvely converting
        # all nested objects.
        # Other value types are set normally.
        for k, v in dict(kwargs).items():
            if isinstance(v, dict):
                v = ASKRequest(**v)
            self[k] = v

    def _dict(self):
        """Return this `ASKObject` as a `dict`

        Removes any attribute whose value is `None`

        Calls this same function on any attributes of
        type `ASKObject` which recursively converts all
        nested ASKObjects back into a dictionary

        :return:
        """
        d = dict(self)
        for k, v in dict(d).items():
            if isinstance(v, ASKRequest):
                d[k] = v._dict()
            elif v is None:
                del d[k]
        return d

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, attr):
        return self.get(attr)
