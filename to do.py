import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import os

FILE_NAME = "advanced_tasks.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}


def save_data():
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


def add_folder():
    name = simpledialog.askstring("New Folder", "Enter folder name:")
    if name and name not in data:
        data[name] = []
        save_data()
        render()


def delete_folder(folder):
    if messagebox.askyesno("Delete", f"Delete folder '{folder}'?"):
        del data[folder]
        save_data()
        render()


def add_task(folder):
    task = simpledialog.askstring("New Task", f"Add task to '{folder}':")
    if task:
        data[folder].append({"text": task, "done": False})
        save_data()
        render()


def delete_task(folder, index):
    data[folder].pop(index)
    save_data()
    render()


def toggle_task(folder, index):
    data[folder][index]["done"] = not data[folder][index]["done"]
    save_data()
    render()


def toggle_folder(folder):
    folder_states[folder] = not folder_states.get(folder, True)
    render()

def render():
    for widget in container.winfo_children():
        widget.destroy()

    if not data:
        tk.Label(container,
                 text="✨ No folders yet. Click '+ Folder' to create one.",
                 bg="white",
                 fg="gray",
                 font=("Segoe UI", 12)).pack(pady=30)
        return

    for folder in data:
        tasks = data[folder]
        completed = sum(t["done"] for t in tasks)
        total = len(tasks)

        folder_frame = tk.Frame(container, bg="#e8f0ff", padx=10, pady=6)
        folder_frame.pack(fill="x", pady=8, padx=10)

        header = tk.Frame(folder_frame, bg="#e8f0ff")
        header.pack(fill="x")

        arrow = "▼" if folder_states.get(folder, True) else "▶"

        toggle_btn = tk.Button(header, text=arrow,
                               command=lambda f=folder: toggle_folder(f),
                               bg="#e8f0ff", bd=0)
        toggle_btn.pack(side="left")

        folder_label = tk.Label(header,
                                text=f"📁 {folder}  ({completed}/{total})",
                                bg="#e8f0ff",
                                font=("Segoe UI", 12, "bold"))
        folder_label.pack(side="left", padx=5)

        tk.Button(header, text="+ Task",
                  command=lambda f=folder: add_task(f),
                  bg="#4a7cff", fg="white",
                  bd=0, padx=8).pack(side="right", padx=3)

        tk.Button(header, text="Delete",
                  command=lambda f=folder: delete_folder(f),
                  bg="#ff6b6b", fg="white",
                  bd=0, padx=8).pack(side="right", padx=3)

        if folder_states.get(folder, True):
            for i, task in enumerate(tasks):
                task_frame = tk.Frame(container, bg="#f5f7fb", padx=20, pady=5)
                task_frame.pack(fill="x", padx=30, pady=3)

                var = tk.BooleanVar(value=task["done"])

                chk = ttk.Checkbutton(task_frame,
                                      variable=var,
                                      command=lambda f=folder, i=i: toggle_task(f, i))
                chk.pack(side="left")

                font_style = ("Segoe UI", 11, "overstrike") if task["done"] else ("Segoe UI", 11)

                tk.Label(task_frame,
                         text=task["text"],
                         bg="#f5f7fb",
                         font=font_style).pack(side="left", padx=5)

                tk.Button(task_frame,
                          text="🗑",
                          command=lambda f=folder, i=i: delete_task(f, i),
                          bg="#ff6b6b",
                          fg="white",
                          bd=0).pack(side="right")

root = tk.Tk()
root.title("To-Do Manager")
root.geometry("650x600")
root.minsize(450, 500)
root.configure(bg="#8eaaff")

data = load_data()
folder_states = {}

main_card = tk.Frame(root, bg="white")
main_card.place(relx=0.5, rely=0.5, anchor="center",
                relwidth=0.9, relheight=0.92)

title = tk.Label(main_card,
                 text="To-Do Manager",
                 font=("Segoe UI", 18, "bold"),
                 bg="white",
                 fg="#3a4fdd")
title.pack(pady=15)

tk.Button(main_card,
          text="+ Folder",
          command=add_folder,
          bg="#5a78ff",
          fg="white",
          bd=0,
          padx=15,
          pady=6).pack(pady=5)

canvas = tk.Canvas(main_card, bg="white", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_card, orient="vertical",
                          command=canvas.yview)

container = tk.Frame(canvas, bg="white")

container.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=container, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.pack(side="right", fill="y")

render()

root.mainloop()