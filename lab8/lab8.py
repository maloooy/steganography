import os
import random

EMPTY_DIR = "empty"
FILLED_DIR = "filled"


def embed_random_binary_to_text(text):
    words = []
    word = ''
    for ch in text:
        if ch.isspace():
            if word:
                words.append(word)
                word = ''
        else:
            word += ch
    if word:
        words.append(word)

    capacity = len(words)
    binary = ''.join(random.choice('01') for _ in range(capacity))

    embedded_text = ''
    for i, word in enumerate(words):
        embedded_text += word
        embedded_text += '  ' if binary[i] == '1' else ' '

    return embedded_text


def process_all_files():
    os.makedirs(FILLED_DIR, exist_ok=True)

    for i in range(1, 51):
        input_path = os.path.join(EMPTY_DIR, f"{i}.txt")
        output_path = os.path.join(FILLED_DIR, f"{i}.txt")

        if not os.path.exists(input_path):
            print(f"[Пропущен] Файл {input_path} не найден.")
            continue

        with open(input_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        embedded_text = embed_random_binary_to_text(original_text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(embedded_text)

        print(f"[Готово] {input_path} → {output_path}")


if __name__ == "__main__":
    process_all_files()
