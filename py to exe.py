import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys
import threading

def check_pyinstaller():
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def install_pyinstaller():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        messagebox.showinfo("PyInstaller Installed", "PyInstaller has been successfully installed.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Installation Failed", "Failed to install PyInstaller. Please install it manually.")
        sys.exit()

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    if icon_path:
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, icon_path)

def select_output_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, dir_path)

def select_add_files():
    files = filedialog.askopenfilenames()
    add_files_entry.delete(0, tk.END)
    add_files_entry.insert(0, ";".join(files))

def convert_to_exe():
    threading.Thread(target=run_conversion).start()

def run_conversion():
    try:
        if not check_pyinstaller():
            install_pyinstaller()

        file_path = file_entry.get()
        icon_path = icon_entry.get()
        output_dir = output_entry.get()
        add_files = add_files_entry.get()

        if not file_path:
            raise ValueError("Please select a Python file")

        onefile = "--onefile" if onefile_var.get() else ""
        noconsole = "--noconsole" if noconsole_var.get() else ""
        icon = f'--icon="{icon_path}"' if icon_path else ""
        add_files_option = f'--add-data="{add_files}"' if add_files else ""
        output_option = f'--distpath="{output_dir}"' if output_dir else ""

        command = f'pyinstaller {onefile} {noconsole} {icon} {add_files_option} {output_option} "{file_path}"'
        
        progress_bar.start()
        output_text.delete(1.0, tk.END)

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            output_text.insert(tk.END, line)
            output_text.yview(tk.END)
            root.update_idletasks()

        process.wait()

        if process.returncode != 0:
            raise RuntimeError("Conversion failed with non-zero exit code")

        messagebox.showinfo("Success", "Successfully converted to EXE")
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"Error: {e}\n")
        messagebox.showerror("Error", "Conversion failed due to a subprocess error")
    except FileNotFoundError as e:
        output_text.insert(tk.END, f"File not found: {e}\n")
        messagebox.showerror("Error", "Required file not found")
    except ValueError as e:
        output_text.insert(tk.END, f"Value error: {e}\n")
        messagebox.showerror("Error", str(e))
    except RuntimeError as e:
        output_text.insert(tk.END, f"Runtime error: {e}\n")
        messagebox.showerror("Error", str(e))
    except Exception as e:
        output_text.insert(tk.END, f"Unexpected error: {e}\n")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        progress_bar.stop()

def clear_fields():
    file_entry.delete(0, tk.END)
    icon_entry.delete(0, tk.END)
    output_entry.delete(0, tk.END)
    add_files_entry.delete(0, tk.END)
    onefile_var.set(0)
    noconsole_var.set(0)
    progress_bar.stop()
    output_text.delete(1.0, tk.END)

root = tk.Tk()
root.title("Py to EXE Converter App")
root.geometry("700x700")
root.configure(bg="#212121")  # Dark background color

style = ttk.Style(root)
style.theme_use('clam')

# Configure style
style.configure("TButton", font=("Helvetica", 11), padding=6, background="#d32f2f", foreground="white")
style.map("TButton", background=[('active', '#c62828')])
style.configure("TLabel", font=("Helvetica", 11), padding=6, background="#212121", foreground="#e57373")  # Light red text

# File selection
file_label = ttk.Label(root, text="Select Python file:")
file_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
file_entry = ttk.Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10, pady=5)
file_button = ttk.Button(root, text="Browse", command=select_file)
file_button.grid(row=0, column=2, padx=10, pady=5)

# Icon selection
icon_label = ttk.Label(root, text="Select Icon file:")
icon_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
icon_entry = ttk.Entry(root, width=40)
icon_entry.grid(row=1, column=1, padx=10, pady=5)
icon_button = ttk.Button(root, text="Browse", command=select_icon)
icon_button.grid(row=1, column=2, padx=10, pady=5)

# Output directory selection
output_label = ttk.Label(root, text="Output Directory:")
output_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
output_entry = ttk.Entry(root, width=40)
output_entry.grid(row=2, column=1, padx=10, pady=5)
output_button = ttk.Button(root, text="Browse", command=select_output_dir)
output_button.grid(row=2, column=2, padx=10, pady=5)

# Additional files
add_files_label = ttk.Label(root, text="Add Files:")
add_files_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
add_files_entry = ttk.Entry(root, width=40)
add_files_entry.grid(row=3, column=1, padx=10, pady=5)
add_files_button = ttk.Button(root, text="Browse", command=select_add_files)
add_files_button.grid(row=3, column=2, padx=10, pady=5)

# Options
onefile_var = tk.IntVar()
noconsole_var = tk.IntVar()
onefile_check = ttk.Checkbutton(root, text="Onefile", variable=onefile_var)
onefile_check.grid(row=4, column=0, padx=10, pady=5, sticky='w')
noconsole_check = ttk.Checkbutton(root, text="No Console", variable=noconsole_var)
noconsole_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')

# Convert button
convert_button = ttk.Button(root, text="Convert", command=convert_to_exe)
convert_button.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

# Clear button
clear_button = ttk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
progress_bar.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky='we')

# Output text area
output_text = tk.Text(root, height=15, wrap='word', bg="#424242", fg="#ffffff", insertbackground='white')
output_text.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

root.mainloop()
