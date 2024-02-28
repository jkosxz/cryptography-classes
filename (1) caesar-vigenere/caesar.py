def cipher_caesar(text, shift):
    """Ciphers entered text; returns ciphered text"""
    result = ""

    for i in range(len(text)):
        char = text[i]

        if char == ' ':
            result += ' '
            continue

        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)

        else:
            result += chr((ord(char) + shift - 97) % 26 + 97)

    return result


def decipher_caesar(text, shift):
    """Deciphers entered Caesar ciphered text; returns deciphered text"""
    result = ""

    for i in range(len(text)):
        char = text[i]

        if char == ' ':
            result += ' '
            continue

        if char.isupper():
            result += chr((ord(char) - shift - 65) % 26 + 65)

        else:
            result += chr((ord(char) - shift - 97) % 26 + 97)

    return result
