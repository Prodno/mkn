import typing as tp


def filter_list_by_list(lst_a: tp.Union[list[int], range], lst_b: tp.Union[list[int], range]) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    i, j = 0, 0
    ans = []
    if not lst_b:
        return lst_a
    while i < len(lst_a):
        while (j < len(lst_b) - 1) and (lst_b[j] < lst_a[i]):
            j += 1
        if lst_a[i] != lst_b[j]:
            ans.append(lst_a[i])
        i += 1
    return ans
