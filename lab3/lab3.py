import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from math import log10, sqrt


def binary_function(y1, y2):
    return (y1 // 2 + y2) % 2


def embed_message(image_path, message, output_path):
    image = Image.open(image_path).convert('L')
    pixels = np.array(image)
    height, width = pixels.shape

    message_bits = ''.join(format(ord(char), '08b') for char in message)
    message_bits = [int(bit) for bit in message_bits]

    index = 0
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            if index >= len(message_bits):
                break

            x1 = pixels[i, j]
            x2 = pixels[i, j + 1]

            m1 = message_bits[index]
            if m1 != x1 % 2:
                if binary_function(x1 - 1, x2) == message_bits[index + 1]:
                    pixels[i, j] = np.clip(x1 - 1, 0, 255)
                else:
                    pixels[i, j] = np.clip(x1 + 1, 0, 255)

            m2 = message_bits[index + 1]
            if binary_function(pixels[i, j], x2) != m2:
                if binary_function(pixels[i, j], np.clip(x2 + 1, 0, 255)) == m2:
                    pixels[i, j + 1] = np.clip(x2 + 1, 0, 255)
                else:
                    pixels[i, j + 1] = np.clip(x2 - 1, 0, 255)

            index += 2

    stego_image = Image.fromarray(pixels)
    stego_image.save(output_path)


def extract_message(image_path, message_length):
    image = Image.open(image_path).convert('L')
    pixels = np.array(image)
    height, width = pixels.shape

    extracted_bits = []
    index = 0
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            if index >= message_length * 8:
                break

            y1 = pixels[i, j]
            y2 = pixels[i, j + 1]

            extracted_bits.append(y1 % 2)

            extracted_bits.append(binary_function(y1, y2))

            index += 2

    message = []
    for i in range(0, len(extracted_bits), 8):
        byte = extracted_bits[i:i + 8]
        message.append(chr(int(''.join(map(str, byte)), 2)))
    return ''.join(message)


def calculate_psnr(original_image_path, stego_image_path):
    original = np.array(Image.open(original_image_path).convert('L'))
    print(original)
    stego = np.array(Image.open(stego_image_path).convert('L'))
    print(stego)
    mse = np.mean((original - stego) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


def calculate_capacity(image_path):
    image = Image.open(image_path).convert('L')
    width, height = image.size
    capacity = (width * height) // 2 * 2
    return capacity


class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LSB Matching Steganography")
        self.root.geometry("600x600")

        self.image_path = tk.StringVar()
        self.message = tk.StringVar()
        self.output_path = tk.StringVar()
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        tk.Label(root, text="Выберите изображение:").pack(pady=5)
        tk.Entry(root, textvariable=self.image_path, width=50).pack(pady=5)
        tk.Button(root, text="Обзор", command=self.browse_image).pack(pady=5)

        tk.Label(root, text="Введите сообщение:").pack(pady=5)
        self.message_entry = tk.Entry(root, textvariable=self.message, width=50)
        self.message_entry.pack(pady=5)
        self.message_entry.bind("<Control-v>", self.paste_text)

        tk.Button(root, text="Внедрить сообщение", command=self.embed).pack(pady=10)

        tk.Label(root, text="Выберите стего-изображение для извлечения:").pack(pady=5)
        tk.Entry(root, textvariable=self.output_path, width=50).pack(pady=5)
        tk.Button(root, text="Обзор", command=self.browse_stego_image).pack(pady=5)

        tk.Button(root, text="Извлечь сообщение", command=self.extract).pack(pady=10)

        self.capacity_label = tk.Label(root, text="Ёмкость встраивания: ")
        self.capacity_label.pack(pady=5)

        self.psnr_label = tk.Label(root, text="PSNR: ")
        self.psnr_label.pack(pady=5)


    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image_path.set(file_path)
            self.show_image(file_path)
            capacity = calculate_capacity(file_path)
            self.capacity_label.config(text=f"Ёмкость встраивания: {capacity} бит")


    def browse_stego_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.output_path.set(file_path)
            self.show_image(file_path)

    def show_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def embed(self):
        if not self.image_path.get():
            messagebox.showerror("Ошибка", "Выберите изображение!")
            return
        if not self.message.get():
            messagebox.showerror("Ошибка", "Введите сообщение!")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
        if output_path:
            embed_message(self.image_path.get(), self.message.get(), output_path)
            messagebox.showinfo("Успех", "Сообщение успешно внедрено!")

            psnr_value = calculate_psnr(self.image_path.get(), output_path)
            self.psnr_label.config(text=f"PSNR: {psnr_value:.2f} dB")

    def extract(self):
        if not self.output_path.get():
            messagebox.showerror("Ошибка", "Выберите стего-изображение!")
            return

        message_length = len(self.message.get()) if self.message.get() else 100
        extracted_message = extract_message(self.output_path.get(), message_length)
        messagebox.showinfo("Извлеченное сообщение", f"Извлеченное сообщение: {extracted_message}")

    def paste_text(self, event=None):
        try:
            text = self.root.clipboard_get()
            self.message_entry.insert(tk.INSERT, text)
        except tk.TclError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()