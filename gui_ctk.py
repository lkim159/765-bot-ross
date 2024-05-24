import os
import tkinter as tk
import customtkinter as ctk
from openAI_funcs import testing_func

root = ctk.CTk()
root.geometry("700x700")
root.title("Bot Ross")

ctk.set_appearance_mode("dark")

# Title label of GUI
title = ctk.CTkLabel(
    root, 
    text="Bot Ross", 
    font=ctk.CTkFont(size=30, weight="bold")
)
title.pack(padx=10, pady=10)

def send_message():
    user_input = user_input_entry.get()
    print (user_input)
     # Display user input in the chat display
    chat_display.configure(state="normal")
    chat_display.insert(tk.END, "You: " + user_input + "\n")
    chat_display.configure(state="disabled")
    
    # Clear the user input entry widget
    user_input_entry.delete(0, tk.END)
    
    # Send user input to GPT API and get response
    response = testing_func(user_input)
    
    # Display GPT response in the chat display
    chat_display.configure(state="normal")
    chat_display.insert(tk.END, "Bot Ross: " + response + "\n")
    chat_display.configure(state="disabled")
    
    # Scroll to the bottom of the chat display
    chat_display.see(tk.END)
    button_label.configure(text="Sent")

# Chat conversation display
chat_display = ctk.CTkTextbox(
    root,
    state="disabled",  
    wrap="word", 
    border_spacing=5,
    width = 600,
    height = 500
)
chat_display.pack(pady=20)

# Frame for user input
user_input_frame = ctk.CTkFrame(root)
user_input_frame.pack(pady=20)

# User's input textbox
user_input_entry = ctk.CTkEntry(
    user_input_frame,
    placeholder_text="Message Bot Ross",
    width=400,
    height=45
    #font=("Helvetica", 18)
)
user_input_entry.grid(row=0, column=0)

# Button to send user prompt to GPT
send_button = ctk.CTkButton(
    user_input_entry,
    text="Send",
    height=30,
    width=30,
    command=send_message
    #font=("Helvetica", 12)
    #fg_color=
    #hover_color=
)

#send_button.pack(pady=20)
#send_button.grid(row=0, column=0)
send_button.place(relx=0.95, rely=0.16, anchor="ne")


button_label = ctk.CTkLabel(
    root,
    text=""
)
button_label.pack(pady=20)

root.mainloop()

'''
# Create a big text area for displaying chat
chat_display = ctk.CTkTextbox(
    state="disabled", font=chat_font, wrap="word", border_spacing=5
)
chat_display.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

# Create a smaller text area for typing messages
message_input = ctk.CTkTextbox(
    font=chat_font, wrap="word", border_spacing=5
)
message_input.grid(row=3, column=0, padx=20, pady=(0, 0), sticky="nsew")

# Create a button for sending messages
send_button = ctk.CTkButton(
    height=40,
    text="Get Response",
    command=,
    font=ctk.CTkFont(family=FONT_FAMILY, size=17),
    fg_color=("#0C955A", "#106A43"),
    hover_color="#2c6e49",
)
send_button.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="ew")

'''





