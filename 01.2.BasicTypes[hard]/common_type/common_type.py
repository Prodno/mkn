def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    if type1 is str or type2 is str or type1 in [int, float, complex, bool] \
            and type2 in [list, tuple, range] or \
            type2 in [int, float, complex, bool] and type1 in [list, tuple, range]:
        return str
    elif type1 is list and type2 in [list, tuple, range] or type2 is list and type1 in [list, tuple, range]:
        return list
    elif type1 is tuple and type2 in [tuple, range] or type2 is tuple and type1 in [tuple, range] or \
            type2 is range and type1 is range:
        return tuple
    elif type1 is bool and type2 is bool:
        return bool
    elif type1 in [bool, int] and type2 is int or type2 is bool and type1 is int:
        return int
    elif type1 in [bool, int, float] and type2 is float or type2 in [bool, int] and type1 is float:
        return float
    else:
        return complex
