import tkinter as tk
from tkinter import ttk, StringVar


class CreateTaskWindow(tk.Toplevel):
  def __init__(self) -> None:
    super().__init__()
    self.title('Create new Task')
    self.config(padx=10, pady=10)
    self.resizable(False, False)

    self.taskNameValue = StringVar(self, value='Nova Tarefa')
    self.taskNameLabel = ttk.Label(self, text='Nome da Tarefa').grid(row=1, column=0, padx=(10, 5), sticky='w')
    self.taskNameEntry = ttk.Entry(self, textvariable=self.taskNameValue)
    self.taskNameEntry.grid(row=1, column=1, padx=(5, 10), sticky='nsew')
    self.taskNameEntry.focus_set()
    self.taskNameEntry.select_range(0, len(self.taskNameValue.get()))
