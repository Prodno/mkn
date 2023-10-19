"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import types
import typing as tp

from typing import Any

CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(code: types.CodeType, defaults, kwdefaults, *args: Any, **kwargs: Any) -> dict[str, Any]:  # type: ignore
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param code: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    result: dict[Any, Any] = {}

    num_pos = code.co_posonlyargcount
    num_usual = code.co_argcount - code.co_posonlyargcount
    num_total = len(code.co_varnames)

    args_created = False
    kwargs_created = False
    args_name = ""
    kwargs_name = ""
    akw_num = 0

    flags = code.co_flags
    if bool(flags & CO_VARARGS) and bool(flags & CO_VARKEYWORDS):
        akw_num = 2
    elif bool(flags & CO_VARARGS):
        akw_num = 1
    elif bool(flags & CO_VARKEYWORDS):
        akw_num = 1

    num_local = len(code.co_varnames) - akw_num - code.co_kwonlyargcount - code.co_argcount
    num_total -= num_local

    if bool(flags & CO_VARARGS) and bool(flags & CO_VARKEYWORDS):
        args_created = True
        kwargs_created = True
        args_name = code.co_varnames[num_total - 2]
        kwargs_name = code.co_varnames[num_total - 1]
        result[args_name] = ()
        result[kwargs_name] = {}
        num_total -= 2

    elif bool(flags & CO_VARARGS):
        args_created = True
        args_name = code.co_varnames[num_total - 1]
        result[args_name] = ()
        num_total -= 1

    elif bool(flags & CO_VARKEYWORDS):
        kwargs_created = True
        kwargs_name = code.co_varnames[num_total - 1]
        result[kwargs_name] = {}
        num_total -= 1

    usual_in_kwargs = 0  # number of usual (middle) variables in kwargs
    for kw_name in kwargs:
        if kw_name in code.co_varnames[:num_total]:
            usual_in_kwargs += 1

    if len(args) > num_pos + num_usual and not args_created:
        raise TypeError(ERR_TOO_MANY_POS_ARGS)
    if not args_created:
        for i in range(len(args)):  # setting given in args arguments to it's places
            result[code.co_varnames[i]] = args[i]
    else:
        for i in range(min(len(args), num_pos + num_usual)):  # case args_created
            result[code.co_varnames[i]] = args[i]
        if len(args) > num_pos + num_usual:
            result[args_name] = tuple(args[num_pos + num_usual:])

    for key, value in kwargs.items():  # setting positional kwargs to it's places
        if key in code.co_varnames[num_pos:num_total]:
            if key in result:
                raise TypeError(ERR_MULT_VALUES_FOR_ARG)
            result[key] = value
        elif key in code.co_varnames[:num_pos] and not kwargs_created:
            raise TypeError(ERR_POSONLY_PASSED_AS_KW)
        elif key in code.co_varnames[:num_pos] and kwargs_created:
            result[kwargs_name][key] = kwargs[key]

    pos_usual_without_default = code.co_argcount  # check if not given position args have default value
    if defaults is not None:
        pos_usual_without_default -= len(defaults)
    for i in range(pos_usual_without_default, code.co_argcount):
        if code.co_varnames[i] not in result and defaults is not None:
            result[code.co_varnames[i]] = defaults[i - pos_usual_without_default]

    if kwdefaults is not None:  # check if not given name_only args have default value
        for arg_name in code.co_varnames[num_pos + num_usual:num_total]:
            if arg_name not in result and arg_name in kwdefaults:
                result[arg_name] = kwdefaults[arg_name]

    for arg_name in code.co_varnames[:num_pos + num_usual]:  # check if every position arg is given
        if arg_name not in result:
            raise TypeError(ERR_MISSING_POS_ARGS)

    for arg_name in code.co_varnames[num_pos + num_usual:num_total]:  # check if every position arg is given
        if arg_name not in result:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)

    for key in kwargs:
        if key not in result and not kwargs_created:
            raise TypeError(ERR_TOO_MANY_KW_ARGS)
        if key not in result and kwargs_created:
            result[kwargs_name][key] = kwargs[key]

    return result


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.9/Include/frameobject.h#L17

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.return_value = None
        self.bytecode_counter = 0

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:
        instructions = list(dis.get_instructions(self.code))
        while self.bytecode_counter < 2 * len(instructions):
            # print("*" * 100)
            # print(self.bytecode_counter)
            instruction = instructions[self.bytecode_counter // 2]
            getattr(self, instruction.opname.lower() + "_op")(
                instruction.argval)
            self.bytecode_counter += 2
            if instruction.opname == "RETURN_VALUE":
                break
        return self.return_value

    def call_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3496
        """
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def call_function_kw_op(self, argc: int) -> None:
        tos = self.pop()
        kwargs = {}
        values = self.popn(len(tos))
        for name, value in zip(tos, values):
            kwargs[name] = value
        args = self.popn(argc - len(tos))
        f = self.pop()
        self.push(f(*args, **kwargs))

    # def call_function_ex_op(self, flags: int):
    #

    def find(self, name: str) -> tp.Any:
        if name in self.builtins:
            return self.builtins[name]
        elif name in self.locals:
            return self.locals[name]
        elif name in self.globals:
            return self.globals[name]
        raise NameError

    def load_name_op(self, arg: str) -> None:
        """
        Partial realization

        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2416
        """
        self.push(self.find(arg))

    def load_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_GLOBAL

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2480
        """
        if arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.builtins:
            self.push(self.builtins[arg])

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1346
        """
        self.push(arg)
        b = 3
        max(b, 2)  # __build_class__, к моему великому сожалению, не имеет так называемой документации............

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-RETURN_VALUE

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1911
        """
        self.return_value = self.pop()

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-POP_TOP

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1361
        """
        self.pop()

    def rot_two_op(self, arg: str) -> None:
        tos, tos1 = self.pop(), self.pop()
        self.push(tos, tos1)

    def rot_three_op(self, arg: str) -> None:
        tos, tos1, tos2 = self.pop(), self.pop(), self.pop()
        self.push(tos, tos2, tos1)

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3571

        Parse stack:
            https://github.com/python/cpython/blob/3.9/Objects/call.c#L671

        Call function in cpython:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L4950
        """
        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)

        # TODO: use arg to parse function defaults

        kw_defaults = None
        if (arg & 0x02) == 0x02:
            kw_defaults = self.pop()
        defaults = None
        if (arg & 0x01) == 0x01:
            defaults = self.pop()

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args: dict[str, tp.Any] = bind_args(code, defaults, kw_defaults, *args, **kwargs)
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2280
        """
        const = self.pop()
        self.locals[arg] = const

    def store_global_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-STORE_GLOBAL
        """
        const = self.pop()
        self.globals[arg] = const

    def unpack_sequence_op(self, count: int) -> None:
        tos = self.pop()
        for i in range(1, count + 1):
            self.push(tos[-i])

    def compare_op_op(self, op: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        if op == "==":
            return self.push(tos1 == tos)
        elif op == "<":
            return self.push(tos1 < tos)
        elif op == ">":
            return self.push(tos1 > tos)
        elif op == "<=":
            return self.push(tos1 <= tos)
        elif op == ">=":
            return self.push(tos1 >= tos)
        elif op == "!=":
            return self.push(tos1 != tos)

    def inplace_add_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-INPLACE_ADD
        """
        tos = self.pop()
        tos1 = self.pop()
        tos1 += tos
        self.push(tos1)

    def inplace_power_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos = tos1 ** tos
        self.push(tos)

    def inplace_multiply_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 *= tos
        self.push(tos1)

    def inplace_floor_divide_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 //= tos
        self.push(tos1)

    def inplace_true_divide_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 /= tos
        self.push(tos1)

    def inplace_modulo_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 %= tos
        self.push(tos1)

    def inplace_subtract_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 -= tos
        self.push(tos1)

    def inplace_matrix_multiply_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 @= tos
        self.push(tos1)

    def inplace_lshift_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 <<= tos
        self.push(tos1)

    def inplace_rshift_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 >>= tos
        self.push(tos1)

    def inplace_and_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 &= tos
        self.push(tos1)

    def inplace_xor_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 ^= tos
        self.push(tos1)

    def inplace_or_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos1 |= tos
        self.push(tos1)

    def binary_add_op(self, arg: str) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-binary_ADD
        """
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 + tos)

    def binary_power_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 ** tos)

    def binary_multiply_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 * tos)

    def binary_floor_divide_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 // tos)

    def binary_true_divide_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 / tos)

    def binary_modulo_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 % tos)

    def binary_subtract_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 - tos)

    def binary_matrix_multiply_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 @ tos)

    def binary_lshift_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 << tos)

    def binary_rshift_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 >> tos)

    def binary_and_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 & tos)

    def binary_xor_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 ^ tos)

    def binary_or_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1 | tos)

    def unary_positive_op(self, arg: str) -> None:
        tos = self.pop()
        self.push(+tos)

    def unary_negative_op(self, arg: str) -> None:
        tos = self.pop()
        self.push(-tos)

    def unary_not_op(self, arg: str) -> None:
        tos = self.pop()
        self.push(not tos)

    def unary_invert_op(self, arg: str) -> None:
        tos = self.pop()
        self.push(~tos)

    def binary_subscr_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos = tos1[tos]
        self.push(tos)

    def store_subscr_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tos2 = self.pop()
        tos1[tos] = tos2
        self.push(tos1[tos])

    def delete_subscr_op(self, arg: str) -> None:
        tos = self.pop()
        tos1 = self.pop()
        self.push(tos1[tos])
        del tos1[tos]

    def get_iter_op(self, arg: str) -> None:
        tos = self.pop()
        self.push(iter(tos))

    def build_slice_op(self, argc: int) -> None:
        tos = self.pop()
        tos1 = self.pop()
        if argc == 2:
            self.push(slice(tos1, tos))
        else:
            tos2 = self.pop()
            self.push(slice(tos2, tos1, tos))

    def build_tuple_op(self, count: int) -> None:
        self.push(tuple(self.popn(count)))

    def build_list_op(self, count: int) -> None:
        self.push(list(self.popn(count)))

    def build_set_op(self, count: int) -> None:
        self.push(set(self.popn(count)))

    def build_map_op(self, count: int) -> None:
        m = {}
        for i in range(count):
            a = self.pop()
            b = self.pop()
            m[b] = a
        self.push(m)

    def list_to_tuple_op(self, arg: str) -> None:
        self.push(tuple(self.pop()))

    def build_string_op(self, count: int) -> None:
        self.push("".join(list(self.popn(count))))

    def format_value_op(self, flags: tuple[tp.Any, tp.Any]) -> None:
        fmt_spec = ""
        if flags[1]:
            fmt_spec = self.pop()
        value = self.pop()
        if flags[0] is None:
            pass
        elif (flags[0] & 0x03) == 0x01:
            value = str(value)
        elif (flags[0] & 0x03) == 0x02:
            value = repr(value)
        elif (flags[0] & 0x03) == 0x03:
            value = ascii(value)
        self.push(format(value, fmt_spec))

    def build_const_key_map_op(self, count: int) -> None:
        m = {}
        keys = self.pop()
        for key, value in zip(keys, self.popn(count)):
            m[key] = value
        self.push(m)

    def set_update_op(self, i: int) -> None:
        tos = self.pop()
        tosses = self.popn(i - 1)
        tos1 = self.pop()
        tos1.update(tos)
        self.push(tos1)
        self.push(*tosses)

    def dict_update_op(self, i: int) -> None:
        tos = self.pop()
        tosses = self.popn(i - 1)
        tos1 = self.pop()
        tos1.update(tos)
        self.push(tos1)
        self.push(*tosses)

    def dict_merge_op(self, i: int) -> None:
        tos = self.pop()
        tosses = self.popn(i - 1)
        tos1 = self.pop()
        for key in tos:
            if key in tos1:
                raise KeyError
            tos1[key] = tos[key]
        self.push(tos1)
        self.push(*tosses)

    def jump_forward_op(self, delta: int) -> None:
        self.bytecode_counter = delta - 2

    def pop_jump_if_true_op(self, target: int) -> None:
        tos = self.pop()
        if tos:
            self.bytecode_counter = target - 2

    def pop_jump_if_false_op(self, target: int) -> None:
        tos = self.pop()
        if not tos:
            self.bytecode_counter = target - 2

    # def jump_if_not_exc_match(self, target: int) -> None:
    #     tos = self.pop()
    #     tos1 = self.pop()
    #     if tos == tos1:
    #         self.bytecode_counter = target - 2

    def jump_if_true_or_pop_op(self, target: int) -> None:
        if self.top():
            self.bytecode_counter = target - 2
        else:
            self.pop()

    def jump_if_false_or_pop_op(self, target: int) -> None:
        if not self.top():
            self.bytecode_counter = target - 2
        else:
            self.pop()

    def jump_absolute_op(self, target: int) -> None:
        self.bytecode_counter = target - 2

    def map_add_op(self, i: int) -> None:
        tos = self.pop()
        tos1 = self.pop()
        tosses = self.popn(i - 1)
        tos2 = self.pop()
        tos2[tos1] = tos
        self.push(tos2)
        self.push(*tosses)

    def set_add_op(self, i: int) -> None:
        tos = self.pop()
        tosses = self.popn(i - 1)
        tos1 = self.pop()
        tos1.add(tos)
        self.push(tos1)
        self.push(*tosses)

class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
