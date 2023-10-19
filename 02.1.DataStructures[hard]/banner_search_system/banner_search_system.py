import re


def normalize(
        text: str
        ) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """
    s = re.sub(r'[0-9,.:?#@*&%!-]*', '', text)
    ans = ""
    for i in s:
        if ord(i) < ord('a'):
            ans += chr(ord(i) + ord('a') - ord('A'))
        else:
            ans += i
    return ans


def get_words(
        query: str
        ) -> list[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    return [s for s in query.split(" ") if len(s) > 3]


def build_index(
        banners: list[str]
        ) -> dict[str, list[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    banners_words = {i: get_words(banners[i]) for i in range(len(banners))}
    ans = {}


def get_banner_indices_by_query(
        query: str,
        index: dict[str, list[int]]
        ) -> list[int]:
    """
    Extract banners indices from index, if all words from query contains in indexed banner
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """


#########################
# Don't change this code
#########################

def get_banners(
        query: str,
        index: dict[str, list[int]],
        banners: list[str]
        ) -> list[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]

#########################
