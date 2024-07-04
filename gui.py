import tkinter as tk
from tkinter import filedialog

def browser_file():
  filepath = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
  if filepath:
    entry_var.set(filepath)

root = tk.Tk()
root.title("Scrapper Tutoría")

entry_var = tk.StringVar()

instructions = tk.Label(root, text="Selecciona el archivo .csv con los usuarios y contraseñas:")

entry = tk.Entry(root, textvariable=entry_var, width=70)

button = tk.Button(root, text="Buscar", command=browser_file)

instructions.grid(row=0, columnspan=2, padx=10, pady=10)
entry.grid(row=1, column=0, padx=10, pady=10)
button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()