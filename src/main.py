import getpass
import platform
import tkinter as tk
from tkinter import scrolledtext


class ShellEmulator:
    """Simple GUI shell emulator for Stage 1 (REPL prototype)."""

    def __init__(self, root):
        self.root = root

        username = getpass.getuser()
        hostname = platform.node() or "localhost"

        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("800x500")
        self.root.minsize(600, 350)

        self.output = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Consolas", 11),
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_field = tk.Entry(root, font=("Consolas", 11))
        self.input_field.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.input_field.bind("<Return>", self.execute_command)
        self.input_field.focus_set()

        self.print_output(
            "Эмулятор оболочки запущен.\n"
            "Доступные команды: ls, cd, exit\n\n"
        )

    def print_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    @staticmethod
    def parse_command(command_line):
        parts = command_line.split()
        if not parts:
            return None, []
        return parts[0], parts[1:]

    def execute_command(self, event=None):
        command_line = self.input_field.get()
        self.input_field.delete(0, tk.END)

        if not command_line.strip():
            return

        self.print_output(f"> {command_line}\n")
        command, arguments = self.parse_command(command_line)

        if command == "exit":
            if arguments:
                self.print_output(
                    "Ошибка: команда exit не принимает аргументы.\n\n"
                )
            else:
                self.root.destroy()
            return

        if command in ("ls", "cd"):
            self.execute_stub(command, arguments)
            return

        self.print_output(
            f"Ошибка: неизвестная команда '{command}'.\n\n"
        )

    def execute_stub(self, command, arguments):
        self.print_output(f"Команда: {command}\n")
        self.print_output(f"Аргументы: {arguments}\n\n")


def main():
    root = tk.Tk()
    ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
