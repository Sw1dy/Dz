import tkinter as tk
from tkinter import scrolledtext
import zipfile
import io

virtual_fs = {
    "God": {
        "home": {
            "user": {
                "file1.txt": "user",
                "file2.txt": "user"
            },
            "admin": {
                "file3.txt": "admin"
            }
        },
        "mirea": {
            "Kudzh": {
                "file4.txt": "Kudzh"
            }
        }
    }
}

current_path = ["God", "home"]
current_user = "user"
computer_name = "VirtualOS"

def create_gui():
    root = tk.Tk()
    root.title(f"{computer_name} Emulator")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
    output_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    input_frame = tk.Frame(root)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)

    input_entry = tk.Entry(input_frame)
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def execute_command(event=None):
        command = input_entry.get()
        input_entry.delete(0, tk.END)
        handle_command(command, output_text)

    input_entry.bind("<Return>", execute_command)
    execute_button = tk.Button(input_frame, text="Execute", command=execute_command)
    execute_button.pack(side=tk.RIGHT)

    return root, output_text, input_entry

def ls(path):
    dir_content = virtual_fs
    for p in path:
        dir_content = dir_content.get(p, {})
    return list(dir_content.keys())

def cd(path, new_dir):
    global current_path
    if new_dir == "..":
        if path:
            path.pop()
    else:
        dir_content = virtual_fs
        for p in path:
            dir_content = dir_content.get(p, {})
        if new_dir in dir_content:
            path.append(new_dir)

def chown(path, file, new_owner):
    dir_content = virtual_fs
    for p in path:
        dir_content = dir_content.get(p, {})
    if file in dir_content:
        dir_content[file] = new_owner

def whoami():
    return current_user

def save_to_zip():
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        def add_to_zip(path, zf_path):
            if isinstance(path, dict):
                for key, value in path.items():
                    new_path = f"{zf_path}/{key}"
                    if isinstance(value, dict):
                        add_to_zip(value, new_path)
                    else:
                        zf.writestr(new_path, value)
        add_to_zip(virtual_fs, "")
    memory_file.seek(0)
    with open("vfs.zip", "wb") as f:
        f.write(memory_file.read())
    return "vfs.zip"

def handle_command(command, output_text):
    if command.startswith("ls"):
        result = ls(current_path)
        output_text.insert(tk.END, f"{' '.join(result)}\n")
    elif command.startswith("cd "):
        new_dir = command[3:]
        cd(current_path, new_dir)
        output_text.insert(tk.END, f"Changed directory to {current_path}\n")
    elif command.startswith("chown "):
        _, file, new_owner = command.split()
        chown(current_path, file, new_owner)
        output_text.insert(tk.END, f"Changed owner of {file} to {new_owner}\n")
    elif command == "whoami":
        output_text.insert(tk.END, f"{whoami()}\n")
    elif command == "exit":
        output_text.insert(tk.END, "Exiting...\n")
        root.quit()
    else:
        output_text.insert(tk.END, "Unknown command\n")
    output_text.see(tk.END)

def on_closing():
    zip_file = save_to_zip()
    output_text.insert(tk.END, f"Virtual file system saved to {zip_file}\n")
    root.quit()

if __name__ == "__main__":
    root, output_text, input_entry = create_gui()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
