import typing as tp
import heapq


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    h: list[tp.Any] = []

    en = enumerate(input_streams)
    for i, input_stream in en:
        line = input_stream.readline()
        if line:
            heapq.heappush(h, (int(line), i))

    if not h:
        output_stream.write(b"\n")

    while h:
        value, i = heapq.heappop(h)
        output_stream.write(b'%d\n' % value)

        line = input_streams[i].readline()
        if line:
            heapq.heappush(h, (int(line), i))
