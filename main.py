import tkinter as tk
from tkinter import filedialog, messagebox, font
from rapidfuzz import process, fuzz
import docx
import webbrowser

# Function to find duplicate names with accuracy
def find_duplicates(file_path, accuracy):
    doc = docx.Document(file_path)
    guest_list = [para.text for para in doc.paragraphs if para.text.strip()]

    duplicates = []
    for i, name in enumerate(guest_list):
        matches = process.extract(
            name, guest_list[i+1:], scorer=fuzz.token_sort_ratio)
        # Save results as (original name, duplicate name, match percentage)
        duplicates.extend([(name, match[0], match[1])
                          for match in matches if match[1] >= accuracy])

    # Sort results by match percentage in descending order
    duplicates.sort(key=lambda x: x[2], reverse=True)
    return duplicates


# Function to center the window on the screen
def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    # Set the geometry to center the window
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


# Function to display the results
def display_results(result):
    result_window = tk.Toplevel(root)
    result_window.title("Results")
    
    # Set the result window size and center it
    window_width = 700
    window_height = 500
    center_window(result_window, window_width, window_height)

    # Create a text box with large font size and line spacing
    text = tk.Text(result_window, font=("Arial", 10), spacing1=10, wrap="word")
    text.insert("1.0", result)
    text.config(state="disabled")  # Disable editing the content
    text.pack(expand=True, fill="both", padx=10, pady=10)


# Function called when "Run" button is clicked
def run_program():
    accuracy = accuracy_scale.get()
    if not file_path.get():
        messagebox.showwarning(
            "Warning", "Please select a data file (.docx)")
        return

    # Find duplicate entries
    duplicates = find_duplicates(file_path.get(), accuracy)
    if duplicates:
        result = "\n".join(f"{original} <-> {duplicate} ({percent:.1f}% match)"
                           for original, duplicate, percent in duplicates)
        display_results(f"Duplicate entries:\n{result}")
    else:
        messagebox.showinfo("Results", "No duplicates found.")


# Function called when "Choose file" button is clicked
def choose_file():
    file_selected = filedialog.askopenfilename(
        filetypes=[("Word Documents", "*.docx")])
    file_path.set(file_selected)


# Function to exit the program
def exit_program():
    root.destroy()


# Function to open the GitHub link when clicked
def open_github_link(event):
    webbrowser.open("https://github.com/kitepea")


# Tkinter interface
root = tk.Tk()
root.title("Duplicate Finder")

# Set the main window size and center it
window_width = 400
window_height = 315
center_window(root, window_width, window_height)

# Choose data file
file_path = tk.StringVar()
tk.Label(root, text="Choose data file (.docx):").pack(pady=10)
tk.Button(root, text="Choose file", command=choose_file).pack()
tk.Entry(root, textvariable=file_path, width=50, state="readonly").pack(pady=5)

# Accuracy setting
tk.Label(root, text="Accuracy (default 72):").pack(pady=10)
accuracy_scale = tk.Scale(root, from_=0, to=100, orient="horizontal")
accuracy_scale.set(72)  # Set default value
accuracy_scale.pack()

# Run button
tk.Button(root, text="Run", command=run_program, width=15).pack(pady=10)

# Exit button
tk.Button(root, text="Exit", command=exit_program, width=15).pack(pady=10)

# Add a clickable GitHub link
link_label = tk.Label(root, text="GitHub: https://github.com/kitepea", fg="blue", cursor="hand2")
link_label.pack(pady=10)
link_label.bind("<Button-1>", open_github_link)  # Bind the click event to the function

root.mainloop()
