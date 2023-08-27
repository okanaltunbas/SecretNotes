from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet

# Anahtar oluşturma veya daha önce oluşturulanı yükleme
key_file_path = "key.key"

try:
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)


def clear_form():
    title_entry.delete(0, "end")
    message_text.delete("1.0", "end")
    key_entry.delete(0, "end")


def encrypt_text():
    key_data = key_entry.get()
    secret_text = key_data + " " + message_text.get("1.0", END)
    encoded_data = secret_text.encode()
    encrypted_data = cipher_suite.encrypt(encoded_data)

    return encrypted_data.decode()


def decrypt_data():
    try:
        entered_key = key_entry.get()
        encrypted_data = message_text.get("1.0", END).encode()
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()

        form_data = decrypted_data.split()
        stored_key = form_data[0]
        decrypted_text = " ".join(form_data[1:])

        clear_form()

        if entered_key == stored_key:
            message_text.insert("1.0", decrypted_text)
        else:
            messagebox.showinfo(title="Error!", message="Incorrect Key")

    except:
        clear_form()
        messagebox.showinfo(title="Error!", message="Decryption Error")

def save_encrypted_text():
    with open("mysecret.txt", "a") as file:
        title = title_entry.get()
        encrypted_data = encrypt_text()
        file.write(title + "\n")
        file.write(encrypted_data + "\n")
        clear_form()


window = Tk()
window.title("Secret Notes")
window.minsize(width=500, height=1000)

original_image = Image.open("C:/Users/okana/Masaüstü/secret.png")
original_image = original_image.resize((150, 150))
image = ImageTk.PhotoImage(original_image)
label = Label(window, image=image)
label.pack(pady=50)

title_label = Label(text="Enter Your Title", fg="black", font=("Arial", 13, "normal"))
title_label.pack(pady=10)

title_entry = Entry(width=50)
title_entry.pack()

message_label = Label(text="Enter Your Secret", fg="black", font=("Arial", 13, "normal"))
message_label.pack(pady=10)

message_text = Text(width=50)
message_text.pack()

key_label = Label(text="Enter master key", fg="black", font=("Arial", 13, "normal"))
key_label.pack(pady=10)

key_entry = Entry(width=50)
key_entry.pack()

save_button = Button(text="Save & Encrypt", command=save_encrypted_text)
save_button.pack(pady=10)

decrypt_button = Button(text="Decrypt", command=decrypt_data)
decrypt_button.pack()

window.mainloop()
