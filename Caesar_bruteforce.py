def decrypt_caesar_cipher(ciphertext):
    # Определяем русский алфавит
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    decrypted_texts = []

    # Преобразуем шифротекст к верхнему регистру
    ciphertext = ciphertext.upper()

    # Перебираем все возможные ключи (0-32)
    for key in range(len(alphabet)):
        decrypted_text = ''

        # Расшифровываем каждый символ
        for char in ciphertext:
            if char in alphabet:
                index = (alphabet.index(char) - key) % len(alphabet)
                decrypted_text += alphabet[index]
            else:
                decrypted_text += char

        decrypted_texts.append((key, decrypted_text))

    return decrypted_texts

# Ввод зашифрованного текста от пользователя
ciphertext = input("Введите зашифрованный текст: ")
decrypted_texts = decrypt_caesar_cipher(ciphertext)

for key, decrypted_text in decrypted_texts:
    print(f'Ключ {key}: {decrypted_text}')
