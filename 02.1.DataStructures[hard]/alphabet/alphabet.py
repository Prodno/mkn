import enum


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: dict[str, set[str]]
        ) -> list[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    dct = {}
    for i in graph:
        dct[i] = 0
    for val in graph.values():
        for i in val:
            dct[i] += 1
    alphabet: list[str] = []
    while len(alphabet) < len(graph):
        v = min(dct, key=lambda x: dct[x])
        alphabet.append(v)
        for val in graph[v]:
            dct[val] -= 1
        del dct[v]
    return alphabet


def build_graph(
        words: list[str]
        ) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    res: dict[str, set[str]] = {}
    for word in words:
        for i in word:
            res[i] = set()
    for ind in range(len(words) - 1):
        word1 = words[ind]
        word2 = words[ind+1]
        i = 0
        while i < min(len(word1), len(word2)) and word1[i] == word2[i]:
            i += 1
        if i < min(len(word1), len(word2)):
            res[word1[i]].add(word2[i])
    return res


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
        ) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)

#########################
