import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font
import re
import subprocess

class TextTab:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill='both')

        # Default to dark mode
        self.text_area = tk.Text(self.frame, undo=True, wrap='word', font=('consolas', 10), bg='black', fg='white')
        self.text_area.pack(expand=True, fill='both')

        self.scroll = ttk.Scrollbar(self.frame, command=self.text_area.yview)
        self.scroll.pack(side=tk.RIGHT, fill='y')
        self.text_area.config(yscrollcommand=self.scroll.set)

        self.text_area.bind('<KeyRelease>', self.highlight)

    def highlight(self, event=None):
        self.text_area.tag_configure('keyword', foreground='blue')
        self.text_area.tag_configure('comment', foreground='green')

        keywords = r'\b(False|def|if|raise|None|del|import|return|True|elif|in|try|and|else|is|while|as|except|lambda|with|assert|finally|nonlocal|yield|break|for|not|class|from|or|continue|global|pass|self)\b'
        comments = r'#.*'

        self.apply_highlighting(keywords, 'keyword')
        self.apply_highlighting(comments, 'comment')

    def apply_highlighting(self, pattern, tag):
        self.text_area.tag_remove(tag, '1.0', tk.END)
        for match in re.finditer(pattern, self.text_area.get('1.0', tk.END)):
            start = f"{match.start()}c"
            end = f"{match.end()}c"
            self.text_area.tag_add(tag, '1.0+' + start, '1.0+' + end)

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("DogeCode")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()  # For light/dark mode switching
        self.create_tools_menu()  # For dictation feature

        self.create_tab()

        self.terminal_frame = ttk.Frame(self.root)
        self.terminal_frame.pack(expand=True, fill='both', side='bottom')

        self.terminal_text_area = tk.Text(self.terminal_frame, undo=True, wrap='word', font=('consolas', 10), bg='black', fg='white')
        self.terminal_text_area.pack(expand=True, fill='both')

        self.terminal_scroll = ttk.Scrollbar(self.terminal_frame, command=self.terminal_text_area.yview)
        self.terminal_scroll.pack(side=tk.RIGHT, fill='y')
        self.terminal_text_area.config(yscrollcommand=self.terminal_scroll.set)

        self.terminal_text_area.insert('1.0', 'Terminal > ')

        self.terminal_text_area.bind('<KeyRelease>', self.handle_terminal_input)

    def handle_terminal_input(self, event=None):
        if event.keysym == 'Return':
            command = self.terminal_text_area.get("1.0", tk.END)
            output = run_command(command)