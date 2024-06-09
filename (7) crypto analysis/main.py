import random
import textwrap

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
shuffled_alphabet = ''.join(random.sample(alphabet, len(alphabet)))

print(f"Permutacja alfabetu: {shuffled_alphabet}")


def create_substitution_dict(alphabet):
    shuffled_alphabet = ''.join(random.sample(alphabet, len(alphabet)))
    substitution_dict = {char: shuffled_char for char, shuffled_char in zip(alphabet, shuffled_alphabet)}
    return substitution_dict


def apply_substitution(text, substitution_dict):
    return ''.join(substitution_dict.get(char, char) for char in text.upper())


def transpose_columns(text, num_columns):
    rows = textwrap.wrap(text, num_columns)
    num_rows = len(rows)
    transposed = [''.join(row[i] if i < len(row) else '' for row in rows) for i in range(num_columns)]
    return ''.join(transposed)


def transpose_rows(text, num_columns):
    rows = textwrap.wrap(text, num_columns)
    random.shuffle(rows)
    return ''.join(rows)


def encrypt(text, num_columns):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    substitution_dict = create_substitution_dict(alphabet)
    substituted_text = apply_substitution(text, substitution_dict)
    column_transposed_text = transpose_columns(substituted_text, num_columns)
    fully_transposed_text = transpose_rows(column_transposed_text, num_columns)
    return fully_transposed_text


# Example text to encrypt
example_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore 
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est 
laborum."""

# Encrypt the text
encrypted_text = encrypt(example_text, 10)

# Save the encrypted text to a file
with open("./data/encrypted_text.txt", "w") as file:
    file.write(encrypted_text)
