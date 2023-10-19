import typing as tp


def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    ans = []
    for i in elements:
        ans.append(i ** 2)
    return ans


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    return list(range(1, len(elements) + 1))


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """
    if not elements:
        return None
    max_val = max(elements)
    return elements.index(max_val)


# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    return elements[1::2]


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    i = 0
    while i < len(elements) and elements[i] != 3:
        i += 1
    if i == len(elements):
        return None
    return i


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    a = list(reversed(elements))
    print(a)
    ans = get_first_three_index(a)
    if ans is not None:
        return len(elements) - ans - 1
    else:
        return None

# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)


# ====================================================================================================


def get_min_max(elements: list[int], default: tp.Optional[int]) -> tuple[tp.Optional[int], tp.Optional[int]]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    if not elements:
        return default, default
    return min(elements), max(elements)


# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    return x if (x := elements[i]) > boundary else None
