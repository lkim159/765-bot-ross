import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import customtkinter as ctk
import os
import asyncio
from openAI_funcs import get_description, get_critique, get_more_info, testing_func

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
        chat_right.insert('end', "You: " + user_input + "\n", "default")
        # Fill other chat box with same text as padding but make it hidden
        chat_left.insert('end', "You: " + user_input + "\n", "hidden")
        entry.delete(0, 'end')
        response = generate_response(user_input)

        chat_left.insert('end', "Bot: " + response + "\n", "default")
        chat_right.insert('end', "Bot: " + response + "\n", "hidden")

        # Scroll to end of chat
        chat_left.see('end') 
        chat_right.see('end')


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
        chat_left.insert('end', "Bot: Processing the image...\n", "default")
        chat_left.see('end')
        # Padding on the other chatbox but hidden to align the next message
        chat_right.insert('end', "Bot: Processing the image...\n", "hidden")
        chat_right.see('end')
        root.update_idletasks()

        # Get and display the image description and critique
        description = await get_description(file_path)
        critique = await get_critique(file_path)
        combined_description = ("Bot: Here is the description of the uploaded image:\n" + description + "\n")
        combined_critique = ("Bot: Here is the critique of the uploaded image:\n" + critique + "\n")

        chat_left.insert('end', combined_description, "default")
        chat_left.insert('end', combined_critique, "default")  
        chat_right.insert('end', combined_description, "hidden")
        chat_right.insert('end', combined_critique, "hidden")

        chat_left.see('end')
        chat_right.see('end')

# Link scrolling chat_left and chat_right with scrollbar
def on_scroll(*args):
    chat_left.yview(*args)
    chat_right.yview(*args)

def insert_hidden_text(textbox, text):
    textbox.configure(text_color="#1d1e1e")
    textbox.insert('end', text)
    textbox.configure(text_color="white")

# Create main window
root = ctk.CTk()
root.geometry("1024x568")
root.title("Chatbot")
ctk.set_appearance_mode("dark")

# Create image display label
image_label = ctk.CTkLabel(root, text="No Image Uploaded\nPlease Upload an Image to Start")
image_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Create frame to hold two chat text widgets
chat_frame = ctk.CTkFrame(root)
# Position it next to image_label and makes sure it spreads right as much as possible
chat_frame.grid(row=0, column=2, padx=5, pady=5, columnspan=2, sticky="nsew")

# Left chat text widget that will hold chatbot's responses
chat_left = ctk.CTkTextbox(chat_frame, wrap='word', bg_color="#1d1e1e", activate_scrollbars=False)
chat_left.pack(side="left", fill="both", expand=True)

# Right chat text widget that will hold user's responses
chat_right = ctk.CTkTextbox(chat_frame, wrap='word', bg_color="#1d1e1e", activate_scrollbars=False)
chat_right.pack(side="left", fill="both", expand=True)

# Tags to hide colour of text
chat_left.tag_config('hidden', foreground="#1d1e1e")
chat_left.tag_config('default', foreground="white")
chat_right.tag_config('hidden', foreground="#1d1e1e")
chat_right.tag_config('default', foreground="white")


# Function to handle mouse wheel scrolling
def handle_mousewheel(event):
    # Delta value 120 as each unit for mouse wheel scrolls
    if event.delta > 0:
        chat_left.yview_scroll(-1, "unit")
        chat_right.yview_scroll(-1, "unit")
    else:
        chat_left.yview_scroll(1, "unit")
        chat_right.yview_scroll(1, "unit")
    return "break"

# Bind scrolling together
chat_left.bind("<MouseWheel>", handle_mousewheel)
chat_right.bind("<MouseWheel>", handle_mousewheel)

# Create scrollbar linked to both text widgets
scrollbar = ctk.CTkScrollbar(chat_frame, command=lambda *args: on_scroll(*args))
scrollbar.pack(side="right", fill="y")
# Configure it to scroll
chat_left.configure(yscrollcommand=scrollbar.set)
chat_right.configure(yscrollcommand=scrollbar.set)

# Configure tags for left and right alignment
chat_left.tag_config('left', justify='left')
chat_right.tag_config('right', justify='left')

# Create input field for user messages
entry = ctk.CTkEntry(root)
entry.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
# Bind 'enter' to send
entry.bind('<Return>', send_message)

# Create button to send message or upload image
send_button = ctk.CTkButton(root, text="Upload Image", command=send_message, width=100)
send_button.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

# Configure column and row weights to make sure widgets expand correctly
root.grid_columnconfigure(0, weight=5)
root.grid_columnconfigure(1, weight=5)
root.grid_columnconfigure(2, weight=5)
root.grid_columnconfigure(3, weight=1)

root.grid_rowconfigure(0, weight=10)

# Start the GUI main loop
root.mainloop()
