import argparse
import getpass
import platform
import tkinter as tk
from tkinter import scrolledtext
import os


class ShellEmulator:
    """GUI shell emulator for Stage 2 (Configuration)."""

    def __init__(self, root, vfs_path, script_path):
        self.root = root
        self.vfs_path = vfs_path
        self.script_path = script_path

        username = getpass.getuser()
        hostname = platform.node() or "localhost"

        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x500")
        self.root.minsize(600, 350)

        self.output = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 11)
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_field = tk.Entry(root, font=("Consolas", 11))
        self.input_field.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.input_field.bind("<Return>", self.execute_ui_command)
        self.input_field.focus_set()

        self.print_output("Эмулятор оболочки запущен.\n\n")

        # Запуск скрипта после инициализации интерфейса
        if self.script_path:
            self.root.after(100, self.run_startup_script)

    def print_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    @staticmethod
    def parse_command(cmd_line):
        parts = cmd_line.split()
        return (parts[0], parts[1:]) if parts else (None, [])

    def run_startup_script(self):
        if not os.path.exists(self.script_path):
            self.print_output(f"Ошибка: '{self.script_path}' не найден.\n\n")
            return
        
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    self.print_output(f"> {line}\n")
                    self.execute_cmd(line)
        except Exception as e:
            self.print_output(f"Ошибка исполнения стартового скрипта: {e}\n\n")

    def execute_ui_command(self, event=None):
        command_line = self.input_field.get()
        self.input_field.delete(0, tk.END)
        if not command_line.strip():
            return

        self.print_output(f"> {command_line}\n")
        self.execute_cmd(command_line)

    def execute_cmd(self, command_line):
        cmd, args = self.parse_command(command_line)
        if not cmd:
            return

        if cmd == "exit":
            if args:
                self.print_output("Ошибка: exit не принимает аргументы.\n\n")
            else:
                self.root.destroy()
        elif cmd in ("ls", "cd"):
            self.print_output(f"Команда: {cmd}\nАргументы: {args}\n\n")
        elif cmd == "conf-dump":
            self.print_output(
                f"vfs_path={self.vfs_path}\nscript_path={self.script_path}\n\n"
            )
        else:
            self.print_output(f"Ошибка: неизвестная команда '{cmd}'.\n\n")


def main():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--vfs", help="Путь к расположению VFS")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    args = parser.parse_args()

    root = tk.Tk()
    ShellEmulator(root, args.vfs, args.script)
    root.mainloop()


if __name__ == "__main__":
    main()
