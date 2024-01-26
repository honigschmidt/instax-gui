import subprocess
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

proc_timeout = 10
ver = "1.0"
rel = "26-01-2024"
        
def init_gui():
    global button_load
    global input_filename
    global input_args
    global button_print

    gui = tk.Tk()
    gui.geometry("395x105")
    gui.title("InstaxGUI" + " v" + ver + " " + rel)
    frame= tk.Frame(gui)
    frame.pack()
    gui.columnconfigure(0, weight=1)
    gui.columnconfigure(1, weight=4)

    menubar = tk.Menu(gui)
    menubar.add_command(label="Help", command=show_help)
    gui.config(menu=menubar)

    button_load = tk.Button(frame, text="Select image", command=select_image)
    button_load.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    input_filename = tk.Entry(frame, width=40, state="disabled")
    input_filename.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

    label_args = tk.Label(frame, text="Arguments (optional):")
    label_args.grid(row=1, column=0, padx=5, pady=5)

    input_args = tk.Entry(frame)
    input_args.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

    button_print = tk.Button(frame, text="Print", state="disabled", command=print_image)
    button_print.grid(row=2, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)

    gui.mainloop()

def select_image():
    global file_in
    file_in = askopenfilename()
    update_filename(file_in)
    if "file_in" in globals():
        button_print.configure(state="active")
    return

def update_filename(filename):
    input_filename.config(state="normal")
    input_filename.delete(0, last="end")
    input_filename.insert(0, filename)
    input_filename.config(state="disabled")
    return

def print_image():
    opt_args = input_args.get()
    try:
        if (opt_args == ""):
            proc = subprocess.Popen(["python", "-m", "instax.print", file_in])
        else:
            proc = subprocess.Popen(["python", "-m", "instax.print", opt_args, file_in])
        proc.wait(timeout=proc_timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        return

def show_help():
    help_1 = "(1) Connect to your Instax printer via WiFi\n"
    help_2 = "(2) Press [Select image] to choose image to print\n"
    help_3 = "(3) Enter arguments (optional)\n"
    help_4 = "(4) Press [Print] to send image to the Instax printer"
    messagebox.showinfo("Help", help_1 + help_2 + help_3 + help_4)
    return

init_gui()