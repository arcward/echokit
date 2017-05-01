



def verify(name, values):
    def slot_dec(func):
        def wrapped_func(orig):
            if orig['name'] != name:
                raise ValueError('bad name')
            if orig['value'] not in values:
                raise ValueError('bad value')
            return func(orig)
        return wrapped_func
    return slot_dec


@verify(name='ham', values=['rum'])
def confirm(orig):
    return orig


o = {'name': 'ham', 'value': 'rum'}
print(confirm(o))
