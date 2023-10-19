import typing as tp


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    d = {key: [] for key in dct.values()}
    for i in dct:
        d[dct[i]].append(i)
    return d
