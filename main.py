import tkinter as tk
from tkinter import simpledialog
from utils import *

def main() -> None:
  # Checks if config.json already exists and create it case it doesn't
  setup = load_config()

  if not setup:
    alarm_time = simpledialog.askstring('Configuração', 'Entre com um horário para o lembrete:', initialvalue='10:00')
    alarm_advance = simpledialog.askinteger('Configuação', 'Avisar com quantos dias de antecedencia?', initialvalue=1, minvalue=0, maxvalue=7)
    setup = {'alarm': alarm_time, 'default_advance': alarm_advance}
    save_config(setup)

  # Main window
  root = tk.Tk()
  root.title('Task Manager App')
  root.geometry('480x360')
  root.config(padx=10, pady=10)

  root.mainloop()


if __name__ == '__main__':
  main()