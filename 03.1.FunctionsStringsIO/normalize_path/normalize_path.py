def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    if path == '':
        return '.'
    parse = [s for s in path.split('/') if len(s) > 0 and s != '.']
    ans = []
    count = 0
    flag = False
    if path[0] == '/':
        flag = True
        count = len(path)
    for s in parse:
        if s == "..":
            if count > 0:
                if len(ans) > 0:
                    ans.pop()
                count -= 1
            else:
                ans.append("..")
        else:
            count += 1
            ans.append(s)
    norm = '/'.join(ans)
    if flag:
        norm = '/' + norm
    if len(norm) == 0:
        return '.'
    return norm
