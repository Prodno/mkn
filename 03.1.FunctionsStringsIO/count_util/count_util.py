import typing as tp


def count_util(text: str, flags: tp.Optional[str] = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    ans = {}
    if flags is None or flags == '' or 'm' in flags:
        ans["chars"] = len(text)
    if flags is None or flags == '' or 'l' in flags:
        ans["lines"] = len(text.split('\n')) - 1
    if flags is None or flags == '' or 'L' in flags:
        ans["longest_line"] = max([len(s) for s in text.split("\n")])
    if flags is None or flags == '' or 'w' in flags:
        ans["words"] = 0
        lines = [s for s in text.split("\n")]
        for s in lines:
            ans["words"] += len([w for w in s.split(" ") if len(w) > 0])
    return ans




