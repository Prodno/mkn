from contextlib import contextmanager
from typing import Iterator, Optional, TextIO, Type


@contextmanager
def supresser(*types_: Type[BaseException]) -> Iterator[None]:
    pass


@contextmanager
def retyper(type_from: Type[BaseException], type_to: Type[BaseException]) -> Iterator[None]:
    pass


@contextmanager
def dumper(stream: Optional[TextIO] = None) -> Iterator[None]:
    pass
