from collections import Iterable
from functools import reduce
from fptools.callable import curry


def to_path(path):
    '''
    Converts value to a property path tuple.
    '''
    if isinstance(path, str) or isinstance(path, int):
        return (path,)
    elif isinstance(path, Iterable):
        return path
    else:
        raise NotImplementedError(
            f'{path} is not a path. A path must be an iterable or a string not a {type(path)}')


@curry
def getitem(path, _dict):
    '''
    Gets the value at path of dictionary
    '''
    path = to_path(path)
    return reduce(lambda acc, item: acc.get(item) if acc is not None else None, path, _dict)


@curry
def setitem(path, value, _dict):
    '''
    Sets the value at path of dictionary. If a portion of path doesn't exist, it's created.
    '''
    path = to_path(path)
    return {
        **_dict,
        **{
            path[0]: setitem(path[1:], value, _dict.get(path[0])
                             or {}) if len(path) > 1 else value
        },
    }


@curry
def delitem(path, _dict):
    path = to_path(path)
    if len(path) > 1:
        return {
            **_dict,
            path[0]: delitem(path[1:], _dict.get(path[0]))
        }
    new_dict = {**_dict}
    del new_dict[path[0]]
    return new_dict


@curry
def update(path, modifier, _dict):
    '''
    This method is like set except that accepts updater to produce the value to set.
    '''
    path = to_path(path)
    value = getitem(path, _dict)
    return setitem(path, modifier(value), _dict)


@curry
def pick(keys, _dict):
    '''
    Creates an dictionary composed of the picked dictionary properties.
    '''
    return {key: _dict.get(key) for key in keys}

@curry
def omit(keys, _dict):
    return { key: value for key, value in _dict.items() if key not in keys }


@curry
def map_values(modifier, _dict):
    '''
    Creates a dictionary with the same keys as _dict and values generated by applying modifier(val) for each value.
    '''
    return {key: modifier(value) for key, value in _dict.items()}