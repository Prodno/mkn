from collections import UserList
import typing as tp

# https://github.com/python/mypy/issues/5264#issuecomment-399407428
if tp.TYPE_CHECKING:
    BaseList = UserList[tp.Optional[tp.Any]]
else:
    BaseList = UserList


class First:
    def __get__(self, instance, owner):  # type: ignore
        if instance.data:
            return instance.data[0]

    def __set__(self, instance, value):  # type: ignore
        instance.data[0] = value


class Last:
    def __get__(self, instance, owner):  # type: ignore
        if instance.data:
            return instance.data[len(instance.data) - 1]

    def __set__(self, instance, value):  # type: ignore
        instance.data[len(instance.data) - 1] = value


class Reversed:
    def __get__(self, instance, owner):  # type: ignore
        return list(reversed(instance.data))


class Size:
    def __get__(self, instance, owner):  # type: ignore
        return len(instance.data)

    def __set__(self, instance, value):  # type: ignore
        if len(instance.data) >= value:
            instance.data = instance.data[:value]
        else:
            for i in range(value - len(instance.data)):
                instance.data.append(None)


class ListTwist(BaseList):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """
    first = First()
    last = Last()
    reversed = Reversed()
    size = Size()

    @property
    def F(self):  # type: ignore
        return self.first

    @F.setter
    def F(self, value):  # type: ignore
        self.first = value

    @property
    def L(self):  # type: ignore
        return self.last

    @L.setter
    def L(self, value):  # type: ignore
        self.last = value

    @property
    def R(self):  # type: ignore
        return self.reversed

    @property
    def S(self):  # type: ignore
        return self.size

    @S.setter
    def S(self, value):  # type: ignore
        self.size = value
