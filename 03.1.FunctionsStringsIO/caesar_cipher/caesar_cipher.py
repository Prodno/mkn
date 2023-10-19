def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    ans = ""
    n = n % 26
    for i in message:
        code = ord(i) + n
        if ord('Z') >= ord(i) >= ord('A'):
            if code > ord('Z'):
                code -= 26
            ans += chr(code)
        elif ord('z') >= ord(i) >= ord('a'):
            if code > ord('z'):
                code -= 26
            ans += chr(code)
        else:
            ans += i
    return ans

