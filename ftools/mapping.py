"""
Utilities for mappings
"""

from typing import (
    Generic,
    Mapping,
    MutableMapping,
    TypeVar,
    Generator,
    Tuple,
    Iterable,
    Callable,
    Optional,
    cast,
    Union,
    Dict,
)
from copy import copy
from collections.abc import ItemsView
from .callable import curry


M = TypeVar("M", bound=MutableMapping)  # pylint: disable=invalid-name
K = TypeVar("K")  # pylint: disable=invalid-name
V = TypeVar("V")  # pylint: disable=invalid-name
K2 = TypeVar("K2")
V2 = TypeVar("V2")


def create_empty(mapping: M) -> M:
    """
    Create a new mapping of the type of given mapping
    """
    return type(mapping)()


def extract(*keys: K, **aliases: K2):
    """
    For given keys and aliases creates an extractor function that receives a
    mapping and returns a new mapping with the listed keys with their values
    in the mapping and values for keys listed in aliases under the parameter
    names provided
    """
    # pylint: disable=cyclic-import,import-outside-toplevel
    from .collection import getitem

    def extractor(mapping: Mapping[K, V]) -> Mapping[Union[K, str], V2]:
        return {
            **{key: getitem(value, mapping) for key, value in aliases.items()},
            **pick(keys, mapping),
        }

    return extractor


@curry
def pick(
    _items: Iterable[K], mapping: MutableMapping[K, V]
) -> MutableMapping[K, Optional[V]]:
    """
    Creates a mapping composed of the picked mapping items.
    """
    next_mapping = cast(MutableMapping[K, Optional[V]], create_empty(mapping))
    for item in _items:
        next_mapping[item] = mapping.get(item)
    return next_mapping


@curry
def pick_by_value(
    predicate: Callable[[V], bool], mapping: MutableMapping[K, V]
) -> MutableMapping[K, Optional[V]]:
    """
    Creates a mapping composed of the picked mapping items.
    """
    next_mapping = cast(MutableMapping[K, Optional[V]], create_empty(mapping))
    for key in mapping:
        value = mapping[key]
        if predicate(value):
            next_mapping[key] = value
    return next_mapping


@curry
def pick_by_key(
    predicate: Callable[[K], bool], mapping: MutableMapping[K, V]
) -> MutableMapping[K, Optional[V]]:
    """
    Creates a mapping composed of the picked mapping items.
    """
    next_mapping = cast(MutableMapping[K, Optional[V]], create_empty(mapping))
    for key in mapping:
        if predicate(key):
            next_mapping[key] = mapping[key]
    return next_mapping


def _omit_new_dictionary(
    _items: Iterable[K], mapping: MutableMapping[K, V]
) -> Dict[K, V]:
    """
    Like omit but always return a dictionary regardless of mapping type.
    """
    return {key: value for key, value in mapping.items() if key not in _items}


@curry
def omit(_items: Iterable[K], mapping: MutableMapping[K, V]) -> MutableMapping[K, V]:
    """
    Creates a mapping without the omitted mapping items.
    """
    try:
        next_mapping = copy(mapping)
    except TypeError:
        return _omit_new_dictionary(_items, mapping)
    for item in _items:
        try:
            next_mapping.pop(item)
        except KeyError:
            continue
    return next_mapping


@curry
def map_values(
    modifier: Callable[[V], V2], mapping: MutableMapping[K, V]
) -> MutableMapping[K, V2]:
    """
    Creates a dictionary with the same keys as _dict and values generated by
    applying modifier(val) for each value.
    """
    next_mapping = cast(MutableMapping[K, V2], create_empty(mapping))
    for key, value in mapping.items():
        next_mapping[key] = modifier(value)
    return next_mapping


@curry
def map_keys(
    modifier: Callable[[K], K2], mapping: MutableMapping[K, V]
) -> MutableMapping[K2, V]:
    """
    Creates a dictionary with the same values as _dict and keys generated by
    applying modifier(key) for each key.
    """
    next_mapping = cast(MutableMapping[K2, V], create_empty(mapping))
    for key, value in mapping.items():
        next_mapping[modifier(key)] = value
    return next_mapping


def is_dict(value):
    """
    Matches if value is a dictionary
    """
    return isinstance(value, dict)


class items(
    ItemsView, Generic[K, V]
):  # pylint: disable=invalid-name,too-many-ancestors
    """
    Mapping.items() for Mapping like objects that don't implement items()
    """

    _mapping: Mapping[K, V]

    def __init__(self, mapping: Mapping[K, V]):  # pylint: disable=super-init-not-called
        self._mapping = mapping

    def __len__(self):
        return self._mapping.__len__()

    def __contains__(self, item):
        return self._mapping.__contains__(item)

    def __iter__(self) -> Generator[Tuple[K, V], None, None]:
        for key in self._mapping:
            yield (key, self._mapping[key])
