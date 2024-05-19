import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import os
import asyncio
from openAI_funcs import get_description, get_critique, get_more_info

# Variable to keep track of whether an image has been uploaded
image_uploaded = False


# Function to handle user input and generate response
def send_message(event=None):
    global image_uploaded
    user_input = entry.get().strip()
    if not user_input and image_uploaded:
        return  # Do nothing if input is empty when image is uploaded
    if not image_uploaded:
        root.after(0, lambda: asyncio.run(upload_image()))
    else:
        chat_history.insert('end', "You: " + user_input + "\n")
        entry.delete(0, 'end')
        response = generate_response(user_input)
        chat_history.insert('end', "Bot: " + response + "\n")
        chat_history.see('end')  # scroll to end of chat history


# Function to generate response
def generate_response(user_input):
    global image_uploaded
    if image_uploaded:
        # If an image is uploaded, use get_more_info function to generate response
        response = get_more_info(user_input)
    else:
        # If no image is uploaded, provide a simple default response
        response = "Hi, please upload an image to start!"

    return response


# Function to upload and display an image
async def upload_image():
    global image_uploaded
    file_path = filedialog.askopenfilename(filetypes=[
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpeg"),
        ("JPG files", "*.jpg"),
        ("WEBP files", "*.webp"),
        ("GIF files", "*.gif")
    ])

    if file_path:
        file_size = os.path.getsize(file_path)
        if file_size > 20 * 1024 * 1024:  # 20 MB in bytes
            messagebox.showerror("File Size Error",
                                 "The selected image is larger than 20MB. Please choose a smaller file.")
            return

        img = Image.open(file_path)
        # Resize image to fit the display area while maintaining aspect ratio
        img.thumbnail((image_label.winfo_width(), image_label.winfo_height()))
        img_tk = ImageTk.PhotoImage(img)
        image_label.configure(image=img_tk, text="")
        image_label.image = img_tk  # Keep a reference to avoid garbage collection
        image_uploaded = True
        send_button.configure(text="Send")

        # Display loading messages while generating description and critique
        chat_history.insert('end', "Bot: Processing the image...\n")
        chat_history.see('end')
        root.update_idletasks()

        # Get and display the image description and critique
        description = await get_description(file_path)
        critique = await get_critique(file_path)

        chat_history.insert('end', "Bot: Here is the description of the uploaded image:\n" + description + "\n")
        chat_history.insert('end', "Bot: Here is the critique of the uploaded image:\n" + critique + "\n")
        chat_history.see('end')


# Create main window
root = ctk.CTk()
root.geometry("1024x768")
root.title("Chatbot")

# Create image display label
image_label = ctk.CTkLabel(root, text="No Image Uploaded")
image_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="nsew")

# Create chat history display
chat_history = scrolledtext.ScrolledText(root, width=50, height=20, wrap='word', bg=root["bg"], fg="white",
                                         highlightbackground="#999999", highlightthickness=1)
chat_history.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

# Create input field for user messages
entry = ctk.CTkEntry(root)
entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
entry.bind('<Return>', send_message)  # bind "Enter"

# Create button to send message or upload image
send_button = ctk.CTkButton(root, text="Upload Image", command=send_message, width=100)
send_button.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

# Configure column and row weights to make sure widgets expand correctly
root.grid_columnconfigure(0, weight=5)
root.grid_columnconfigure(1, weight=4)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=10)

# Start the GUI main loop
root.mainloop()
