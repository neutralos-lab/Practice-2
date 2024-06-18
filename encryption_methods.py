def vigenere_encrypt(plain_text, key, alphabet):
    table = generate_vigenere_table(alphabet)
    plain_text = plain_text.upper()
    key = extend_key(plain_text, key)
    encrypted_text = ""
    for p, k in zip(plain_text, key):
        if p in alphabet:
            row = alphabet.index(p)
            col = alphabet.index(k)
            encrypted_text += table[row][col]
        else:
            encrypted_text += p
    return encrypted_text

def vigenere_decrypt(encrypted_text, key, alphabet):
    table = generate_vigenere_table(alphabet)
    encrypted_text = encrypted_text.upper()
    key = extend_key(encrypted_text, key)
    decrypted_text = ""
    for e, k in zip(encrypted_text, key):
        if e in alphabet:
            row = alphabet.index(k)
            col = table[row].index(e)
            decrypted_text += alphabet[col]
        else:
            decrypted_text += e
    return decrypted_text

def caesar_cipher(text, shift, alphabet):
    shift = int(shift) % len(alphabet)
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(table)

def generate_vigenere_table(alphabet):
    table = []
    for i in range(len(alphabet)):
        row = []
        for j in range(len(alphabet)):
            row.append(alphabet[(i + j) % len(alphabet)])
        table.append(row)
    return table

def extend_key(text, key):
    key = key.upper()
    extended_key = key
    while len(extended_key) < len(text):
        extended_key += key
    return extended_key[:len(text)]
