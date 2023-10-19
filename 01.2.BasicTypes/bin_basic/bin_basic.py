import typing as tp


def find_value(nums: tp.Union[list[int], range], value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    if not nums:
        return False
    i, j = 0, len(nums) - 1
    if i == j:
        return value == nums[0]
    while i + 1 != j:
        k = (i + j) // 2
        if nums[k] > value:
            j = k
        else:
            i = k
    return nums[i] == value or nums[j] == value
