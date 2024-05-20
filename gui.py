import tkinter as tk
from tkinter import scrolledtext
import openAI_funcs as gpt

# Function to handle user input and generate response
def send_message():
    user_input = entry.get()
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)
    response = generate_response(user_input)
    chat_history.insert(tk.END, "Bot Ross: " + response + "\n")
    chat_history.see(tk.END)  # Scroll to the bottom of the chat history

# Function to generate response (replace this with your chatbot logic)
def generate_response(user_input):
    # This is just a placeholder response
    answer = gpt.get_more_info(user_input)
    return answer

# Create main window
root = tk.Tk()
root.geometry("500x500")
root.title("Chatbot")

# Create chat history display
chat_history = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD)
chat_history.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
opener = gpt.bob_rossify("Welcome! My name is Bot Ross and I'm here to help with your art. How are you feeling today?")
chat_history.insert(tk.END, "Bot Ross: " + opener + "\n")

# Create input field for user messages
entry = tk.Entry(root, width=40)
entry.grid(row=1, column=0, padx=5, pady=5)

# Create button to send message
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=5, pady=5)

# Start the GUI main loop
root.mainloop()
