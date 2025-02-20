import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os


def extract_bit(image_path, bit_position):
    image = Image.open(image_path)
    pixels = np.array(image)
    print(pixels)
    bit_layer = (pixels >> (7 - bit_position)) & 1
    print('________________________________')
    visual_attack_image = (bit_layer * 255).astype(np.uint8)
    print(visual_attack_image)
    print('________________________________')
    result = Image.fromarray(visual_attack_image)
    return result


def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("BMP Files", "*.bmp"), ("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
    if not file_path:
        return

    global processed_image, original_image, selected_bit
    original_image = Image.open(file_path)
    processed_image = extract_bit(file_path, selected_bit.get())

    display_images()


def display_images():
    global original_image, processed_image, img_label, result_label

    original_image.thumbnail((512, 512))
    processed_image.thumbnail((512, 512))

    img = ImageTk.PhotoImage(original_image)
    result_img = ImageTk.PhotoImage(processed_image)

    img_label.config(image=img)
    img_label.image = img

    result_label.config(image=result_img)
    result_label.image = result_img


def save_result():
    if processed_image is None:
        return

    save_directory = filedialog.askdirectory()
    if not save_directory:
        return

    save_path = os.path.join(save_directory, "extracted_bit.png")
    processed_image.save(save_path)
    messagebox.showinfo("Сохранение", f"Изображение сохранено в: {save_path}")


def update_bit(*args):
    global processed_image, original_image, selected_bit
    if original_image:
        processed_image = extract_bit(original_image.filename, selected_bit.get())
        display_images()


root = tk.Tk()
root.title("Визуальная атака битов изображения")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_open = tk.Button(frame, text="Открыть изображение", command=open_image)
btn_open.grid(row=0, column=0, padx=10)

btn_save = tk.Button(frame, text="Сохранить результат", command=save_result)
btn_save.grid(row=0, column=1, padx=10)

selected_bit = tk.IntVar(value=0)
selected_bit.trace("w", update_bit)

bit_label = tk.Label(root, text="Выберите бит:")
bit_label.pack()
bit_selector = ttk.Combobox(root, textvariable=selected_bit, values=list(range(8)), state="readonly")
bit_selector.pack()
bit_selector.current(0)

img_label = tk.Label(root)
img_label.pack(side=tk.LEFT, padx=10)

result_label = tk.Label(root)
result_label.pack(side=tk.RIGHT, padx=10)

root.mainloop()
