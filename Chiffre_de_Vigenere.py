





def generate_vigenere_table_cyrillic():
    # Определяем русский алфавит
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    # Создаем пустой список для таблицы Виженера
    table = []
    # Заполняем таблицу Виженера
    for i in range(len(alphabet)):
        # Создаем пустой список для текущей строки
        row = []
        for j in range(len(alphabet)):
            # Добавляем символ с циклическим сдвигом в текущую строку
            row.append(alphabet[(i + j) % len(alphabet)])
        # Добавляем текущую строку в таблицу
        table.append(row)
    # Возвращаем заполненную таблицу Виженера
    return table

def extend_key_cyrillic(text, key):
    # Приводим ключ к верхнему регистру
    key = key.upper()
    # Инициализируем расширенный ключ значением ключа
    extended_key = key
    # Расширяем ключ до длины исходного текста
    while len(extended_key) < len(text):
        # Добавляем ключ к расширенному ключу
        extended_key += key
    # Обрезаем расширенный ключ до длины исходного текста
    return extended_key[:len(text)]

def vigenere_encrypt_cyrillic(plain_text, key):
    # Генерируем таблицу Виженера для русского алфавита
    table = generate_vigenere_table_cyrillic()
    # Приводим исходный текст к верхнему регистру
    plain_text = plain_text.upper()
    # Расширяем ключ до длины исходного текста
    key = extend_key_cyrillic(plain_text, key)
    
    # Инициализируем пустую строку для зашифрованного текста
    encrypted_text = ""
    # Русский алфавит 
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    # Шифруем каждый символ текста
    for p, k in zip(plain_text, key):
        if p in alphabet:  # Шифруем только буквы
            # Определяем строку в таблице для символа текста
            row = alphabet.index(p)
            # Определяем столбец в таблице для символа ключа
            col = alphabet.index(k)
            # Добавляем зашифрованный символ в результат
            encrypted_text += table[row][col]
        else:
            # Если символ не буква, добавляем его как есть
            encrypted_text += p
    # Возвращаем зашифрованный текст
    return encrypted_text

# Исходный текст
plain_text = "ЮЗГУ лучший"
# Ключ шифрования
key = "квадрокоптер"
# Зашифрованный текст
encrypted_text = vigenere_encrypt_cyrillic(plain_text, key)

# Вывод оригинального текста
print(f"Оригинальный текст: {plain_text}")
# Вывод зашифрованного текста
print(f"Зашифрованный текст: {encrypted_text}")