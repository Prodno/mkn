from types import FunctionType
from typing import Any

CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    func_code = func.__code__
    pos_count = func_code.co_argcount
    arg_names = func_code.co_varnames
    positional = arg_names[:pos_count]

    pos_only_count = func_code.co_posonlyargcount

    keyword_only_count = func_code.co_kwonlyargcount
    keyword_only = arg_names[pos_count:pos_count + keyword_only_count]

    defaults = func.__defaults__ if func.__defaults__ is not None else ()
    kwdefaults = func.__kwdefaults__ if func.__kwdefaults__ is not None else ()

    # *args
    star_name = None
    if func_code.co_flags & CO_VARARGS:
        star_name = arg_names[pos_count + keyword_only_count]

    # **kwargs
    double_star_name = None
    if func_code.co_flags & CO_VARKEYWORDS:
        index = pos_count + keyword_only_count
        if func_code.co_flags & CO_VARARGS:
            index += 1
        double_star_name = arg_names[index]

    result: dict[Any, Any] = {}

    if star_name is not None:
        result[star_name] = []

    if double_star_name is not None:
        result[double_star_name] = {}

    for i, arg_val in enumerate(args):
        if i < pos_count:
            var = positional[i]
            result[var] = arg_val
        elif star_name is not None:
            result[star_name].append(arg_val)
        else:
            raise TypeError(ERR_TOO_MANY_POS_ARGS)

    # user keyword values
    for keyword in kwargs:
        # operate test with /
        # ERR_MISSING_KWONLY_ARGS
        # ERR_POSONLY_PASSED_AS_KW

        if keyword in positional:
            ind_keyword = positional.index(keyword)
            if ind_keyword < pos_only_count:
                if keyword not in result:
                    if double_star_name is None:
                        raise TypeError(ERR_POSONLY_PASSED_AS_KW)
                    else:
                        raise TypeError(ERR_MISSING_POS_ARGS)

                if double_star_name is None:
                    raise TypeError(ERR_POSONLY_PASSED_AS_KW)

                result[double_star_name][keyword] = kwargs[keyword]
                continue

        if (keyword in keyword_only) or (keyword in positional):
            if keyword in result:
                raise TypeError(ERR_MULT_VALUES_FOR_ARG)

            result[keyword] = kwargs[keyword]

        elif double_star_name is not None:
            result[double_star_name][keyword] = kwargs[keyword]

        else:
            raise TypeError(ERR_TOO_MANY_KW_ARGS)

    # if len(args) < pos_only_count:
    #     raise TypeError(ERR_MISSING_POS_ARGS)

    if star_name is not None:
        result[star_name] = tuple(result[star_name])

    # default positional values
    for i, default_val in enumerate(reversed(defaults)):
        arg = positional[-i - 1]
        if arg in result:
            continue
        result[arg] = default_val

    # default positional values
    for keyword in kwdefaults:
        if keyword in result:
            continue
        result[keyword] = kwdefaults[keyword]

    for arg in positional:
        if arg not in result:
            raise TypeError(ERR_MISSING_POS_ARGS)

    for arg in keyword_only:
        if arg not in result:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)

    return result
