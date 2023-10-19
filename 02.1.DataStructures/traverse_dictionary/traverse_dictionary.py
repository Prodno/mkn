import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result = []
    for key in dct:
        pref = key if prefix == "" else prefix + "." + key
        if type(dct[key]) is int:
            result.append((pref, dct[key]))
        else:
            result += traverse_dictionary_immutable(dct[key], pref)
    return result


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    for key in dct:
        pref = key if prefix == "" else prefix + "." + key
        if type(dct[key]) is int:
            result.append((pref, dct[key]))
        else:
            traverse_dictionary_mutable(dct[key], result, pref)


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """

    result = []
    dicts = [(dct, "")]
    while dicts:
        d, prefix = dicts.pop()
        for key, val in d.items():
            pref = key if prefix == "" else prefix + "." + key
            if type(val) is int:
                result.append((pref, val))
            else:
                dicts.append((val, pref))
    return result
