import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    for line in inp:
        parse = line.split('\t')
        s1 = line[0:7]
        s2 = parse[-1]
        out.write(s1 + '.'*(81-7-len(s2)) + s2)




