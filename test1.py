import tkinter as tk
from tkinter import colorchooser

def show_color_palette():
    color = colorchooser.askcolor()[1]
    return color

root = tk.Tk()
root.title("Color Chooser Example")

selected_color = None
print(selected_color)

def select_color():
    global selected_color
    selected_color = show_color_palette()
    if selected_color:
        color_label.config(bg=selected_color)
    print(selected_color)

color_label = tk.Label(root, text="Selected Color", bg="white", width=20, height=5)
color_label.pack(pady=10)

select_color_button = tk.Button(root, text="Select Color", command=select_color)
select_color_button.pack(pady=10)

root.mainloop()

print("Selected color:", selected_color)