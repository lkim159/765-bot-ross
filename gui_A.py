import asyncio
import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

import customtkinter as ctk
from PIL import Image, ImageTk
from itertools import cycle
from no_bob_openAI_funcs import make_art, summarise_context, get_description, get_critique, get_more_info, \
    upload_image_async

# Variable to keep track of whether an image has been uploaded
image_uploaded = False
summary = "you're talking to a art student who is going to ask you to critique some art they will upload, respond to any messages the user sent and ask them to describe their piece"
feedback = ""
image_url = None
is_processing = False  # Variable to control spinner animation


def get_summary():
    global summary
    return summary


def set_summary(s):
    global summary
    summary = s
    print(s)
    return


# Function to process the message (get gpt response)
def process_message(user_input):
    global image_url

    # Insert temporary "Typing" to let user know that Bot Ross is coming up with an response
    chat_left.insert('end', "Bot Ross Typing...\n")

    summ = get_summary()

    summ2 = feedback + summ

    response = generate_response(summ2, user_input, image_url)

    # Remove it after response has been generated
    chat_left.delete("end-2l", "end-1l")
    chat_left.see('end')
    chat_right.see('end')

    chat_left.insert('end', "Bot Ross: " + response + "\n", "default")
    chat_right.insert('end', "Bot Ross: " + response + "\n", "hidden")

    # Scroll to end of chat
    chat_left.see('end')
    chat_right.see('end')

    summ = summarise_context(summ + user_input)
    set_summary(summ)


# Function to process the image (get description and critique)
def process_image(file_path):
    async def generate_initial_description_critique():
        global is_processing, image_url
        # Show the button with "Processing..." text and start animation
        is_processing = True
        feedback_button.configure(text="Processing... |", command=None)
        feedback_button.grid()
        animate_button()  # Start the spinner animation

        chat_left.insert('end',
                         "Bot Ross: " + "While I have a look at your masterpiece, tell me, how has your day been?" + "\n",
                         "default")
        chat_right.insert('end',
                          "Bot Ross: " + "While I have a look at your masterpiece, tell me, how has your day been?" + "\n",
                          "hidden")
        chat_left.see('end')
        chat_right.see('end')

        # Upload the image and get the URL
        image_url = await upload_image_async(file_path)
        print(image_url)

        # Get and display the image description and critique
        description = await get_description(image_url)
        critique = await get_critique(image_url)

        completed_description = ("Bot Ross: Here is the description of the uploaded image:\n" + description + "\n")
        completed_critique = ("Bot Ross: Here is the critique of the uploaded image:\n" + critique + "\n")

        #chat_left.insert('end', completed_description, "default")
        #chat_left.insert('end', completed_critique, "default")
        #chat_right.insert('end', completed_description, "hidden")
        #chat_right.insert('end', completed_critique, "hidden")

        chat_left.see('end')
        chat_right.see('end')

        global feedback
        feedback = completed_description + completed_critique

        # Update and show the button since feedback is completed
        is_processing = False  # Stop the spinner
        feedback_button.configure(text="View your feedback!", command=show_feedback)
        feedback_button.grid()

    asyncio.run(generate_initial_description_critique())


# Show feedback in chat when button is clicked
def show_feedback():
    global feedback
    chat_left.insert('end', feedback, "default")
    chat_right.insert('end', feedback, "hidden")
    chat_left.see('end')
    chat_right.see('end')
    # Remove button after feedback has been added
    feedback_button.grid_remove()


# Function to handle user input and generate response
def send_message(event=None):
    global image_uploaded
    user_input = entry.get().strip()
    if not user_input and image_uploaded:
        return  # Do nothing if input is empty when image is uploaded
    if not image_uploaded:
        open_image()
    else:
        chat_right.insert('end', "You: " + user_input + "\n", "default")
        # Fill other chat box with same text as padding but make it hidden
        chat_left.insert('end', "You: " + user_input + "\n", "hidden")
        # Scroll to end of chat
        chat_left.see('end')
        chat_right.see('end')
        entry.delete(0, 'end')

        # Start a new thread to process the image
        threading.Thread(target=process_message, args=(user_input,)).start()


# Function to generate response
def generate_response(s, user_input, image_url):
    global image_uploaded
    if image_uploaded:
        # If an image is uploaded, use get_more_info function to generate response
        response = get_more_info(s, user_input, image_url)
    else:
        # If no image is uploaded, provide a simple default response
        response = "Hi, please upload an image to start!"

    return response


# Function to open and display an image
def open_image():
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

        # Start a new thread to process the image
        threading.Thread(target=process_image, args=(file_path,)).start()


# Link scrolling chat_left and chat_right with scrollbar
def on_scroll(*args):
    chat_left.yview(*args)
    chat_right.yview(*args)


# Create main window
root = ctk.CTk()
root.geometry("1024x768")
root.title("Chatbot")
ctk.set_appearance_mode("dark")

# Create image display label
image_label = ctk.CTkLabel(root, text="No Image Uploaded\nPlease Upload an Image to Start")
image_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Create feedback button (initially hidden)
feedback_button = ctk.CTkButton(root, text="", command=None)
feedback_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="n")
# Hide the button until feedback is created
feedback_button.grid_remove()

# Create chat history display
opener = "Welcome! My name is Bot Ross and I'm here to help with your art. How are you feeling today?"

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

# Spinner characters
spinner_cycle = cycle(["|", "/", "-", "\\"])


# Start the spinner animation
def animate_button():
    global image_url
    if is_processing:  # Only animate if processing
        current_char = next(spinner_cycle)
        if not image_url:
            feedback_button.configure(text=f"Image Uploading... {current_char}", command=None)
        else:
            feedback_button.configure(text=f"Bot Ross Processing... {current_char}", command=None)
        root.after(200, animate_button)  # Update frame every 200ms


# Start the GUI main loop
root.mainloop()
