import collections

# Русский алфавит
alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alphabet_length = len(alphabet)

# Частоты букв в русском языке
russian_freq = {
    'А': 0.0801, 'Б': 0.0159, 'В': 0.0454, 'Г': 0.0170, 'Д': 0.0298, 'Е': 0.0845, 'Ж': 0.0094, 'З': 0.0165,
    'И': 0.0735, 'Й': 0.0121, 'К': 0.0349, 'Л': 0.0440, 'М': 0.0321, 'Н': 0.0670, 'О': 0.1097, 'П': 0.0281,
    'Р': 0.0473, 'С': 0.0547, 'Т': 0.0633, 'У': 0.0262, 'Ф': 0.0026, 'Х': 0.0097, 'Ц': 0.0048, 'Ч': 0.0144,
    'Ш': 0.0073, 'Щ': 0.0036, 'Ъ': 0.0004, 'Ы': 0.0190, 'Ь': 0.0174, 'Э': 0.0032, 'Ю': 0.0064, 'Я': 0.0201
}

# Функция для декодирования текста с использованием ключа
def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key_length = len(key)
    key_indices = [alphabet.index(k) for k in key]
    for i, letter in enumerate(ciphertext):
        if letter in alphabet:
            letter_index = alphabet.index(letter)
            key_index = key_indices[i % key_length]
            decrypted_letter = alphabet[(letter_index - key_index) % alphabet_length]
            decrypted_text.append(decrypted_letter)
        else:
            decrypted_text.append(letter)
    return ''.join(decrypted_text)

# Функция для нахождения вероятного ключа
def find_key(ciphertext, key_length):
    key = ''
    for i in range(key_length):
        nth_letters = ''.join([ciphertext[j] for j in range(i, len(ciphertext), key_length)])
        if not nth_letters:
            return None  # Если нет букв для анализа, возвращаем None
        freqs = collections.Counter(nth_letters)
        most_common = freqs.most_common(1)[0][0]
        key_letter_index = (alphabet.index(most_common) - alphabet.index('О')) % alphabet_length
        key += alphabet[key_letter_index]
    return key

# Основная функция взлома
def vigenere_crack(ciphertext, max_key_length=10):
    ciphertext = ciphertext.upper().replace(' ', '').replace('\n', '')
    best_key = ''
    best_score = float('inf')
    
    for key_length in range(1, max_key_length + 1):
        key = find_key(ciphertext, key_length)
        if key is None:
            continue  # Пропускаем длину ключа, если она не подошла
        decrypted_text = vigenere_decrypt(ciphertext, key)
        freqs = collections.Counter(decrypted_text)
        score = sum((freqs.get(c, 0) / len(decrypted_text) - russian_freq.get(c, 0)) ** 2 for c in alphabet)
        
        if score < best_score:
            best_score = score
            best_key = key
    
    return vigenere_decrypt(ciphertext, best_key), best_key

# Ввод зашифрованного текста
ciphertext = input("Введите зашифрованный текст: ")

# Взлом шифра Виженера
decrypted_text, key = vigenere_crack(ciphertext)

# Вывод расшифрованного текста и ключа
print("\nРасшифрованный текст:")
print(decrypted_text)
print("\nНайденный ключ:")
print(key)
