import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.Optional[tp.IO[bytes]] = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    if output is None:
        output = sys.stdout.buffer
    with open(filename, "rb") as f:
        n = lines_amount
        pos = n + 1
        lines: list[tp.Any] = []
        while len(lines) <= n:
            try:
                f.seek(-pos, 2)
            except IOError:
                f.seek(0)
                break
            finally:
                lines = list(f)
            pos *= 2
        if lines_amount == 0:
            output.write(b'')
        else:
            output.write(b''.join(lines[-n:]))
