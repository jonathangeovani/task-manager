import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from utils import *
from setupwindow import SetupWindow
from createtaskwindow import CreateTaskWindow


def open_setup_window() -> None:
  if not SetupWindow.__name__ in str(root_children()):
    SetupWindow()
  else:
    messagebox.showwarning('Warning!', 'A janela de configurações já está aberta!')


def open_create_task_window() -> None:
  if not CreateTaskWindow.__name__ in str(root_children()):
    CreateTaskWindow()
  else:
    messagebox.showwarning('Warning!', 'Não é possível criar duas tarefas ao mesmo tempo!')


def main() -> None:
  # Checks if config.json already exists and create it case it doesn't
  setup = load_config()

  if not setup:
    alarm_time = simpledialog.askstring('Configuração', 'Entre com um horário para o lembrete:', initialvalue='10:00')
    alarm_advance = simpledialog.askinteger('Configuação', 'Avisar com quantos dias de antecedencia?', initialvalue=1, minvalue=0, maxvalue=7)
    setup = { 'alarm': alarm_time, 'default_advance': alarm_advance, 'tasks': [] }
    save_config(setup)

  # Main window
  root = tk.Tk()
  root.title('Task Manager App')
  root.geometry('480x360')
  root.config(padx=10, pady=10)

  global root_children
  root_children = root.winfo_children

  openSetupWindowButton = ttk.Button(root, text='Open Setup Window', command=open_setup_window).pack(pady=10)
  openCreateTaskWindowButton = ttk.Button(root, text='Create New Task', command=open_create_task_window).pack(pady=10)

  root.mainloop()


if __name__ == '__main__':
  main()