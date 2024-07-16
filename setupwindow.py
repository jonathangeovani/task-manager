import tkinter as tk
from tkinter import ttk, StringVar, IntVar, messagebox
import re
from utils import *

class SetupWindow(tk.Toplevel):
  def __init__(self) -> None:
    super().__init__()
    self.setup = load_config()

    self.title('Setup')
    self.config(padx=10, pady=10)
    self.resizable(False, False)


    self.alarm_checker = self.register(self.validate_alarm_entry)
    self.alarm_advance_checker = self.register(self.validate_alarm_advance_entry)

    self.alarmValue = StringVar(self, self.setup.get('alarm'))
    self.alarmValue.trace_add('write', self.format_alarm_value)
    self.alarmLabel = ttk.Label(self, text='Horário do Lembrete:').grid(row=0, column=0, columnspan=2, padx=(10,0), sticky='w')
    self.alarmLabel2 = ttk.Label(self, text='horas').grid(row=0, column=3, padx=(0,20), sticky='w')
    self.alarmEntry = ttk.Entry(self, textvariable=self.alarmValue, validate="key", validatecommand=(self.alarm_checker, '%P'), width=5, font=('Arial', 13))
    self.alarmEntry.grid(row=0, column=2, padx=(10, 20), sticky='w')
    self.alarmEntry.focus_set()
    self.alarmEntry.select_range(0, len(self.alarmValue.get()))

    self.alarmAdvanceValue = IntVar(self, self.setup.get('default_advance'))
    self.alarmAdvanceValue.trace_add('write', self.format_alarm_advance_value)
    self.alarmAdvanceLabel1 = ttk.Label(self, text='Antecedencia padrão:').grid(row=1, column=0, columnspan=2, padx=(10,0), sticky='w')
    self.alarmAdvanceLabel2 = ttk.Label(self, text='dias').grid(row=1, column=3, padx=(0,20), sticky='w')
    self.alarmAdvanceEntry = ttk.Entry(self, textvariable=self.alarmAdvanceValue, validate='key', validatecommand=(self.alarm_advance_checker, '%P'), font=('Arial', 13), width=5)
    self.alarmAdvanceEntry.grid(row=1, column=2, padx=10, pady=5, sticky='w')

    self.saveConfigButton = ttk.Button(self, text='Salvar', command=self.update_config).grid(row=2, column=0, columnspan=2, padx=(10,4), pady=(5, 0), sticky='nwse')
    self.resetConfigButton = ttk.Button(self, text='Restaurar', command=self.reset_config).grid(row=2, column=2, columnspan=2, padx=(4,0), pady=(5, 0), sticky='nwse')

  
  def validate_alarm_entry(self, text: str) -> bool:
    return (re.search('^[0-9:]+$', text) or len(text) == 0) and len(text) <= 5
  

  def validate_alarm_advance_entry(self, text: str) -> bool:
    return (re.search('^[0-7]+$', text) or len(text) == 0) and len(text) <= 2
  

  def format_alarm_value(self, *args) -> None:
    text = self.alarmValue.get()

    match len(text):
      case 1:
        if ':' in text:
          self.alarmEntry.insert(0, '00')
        elif text.isnumeric() and int(text) > 2:
          self.alarmEntry.insert(0, '0')
      case 2:
        if text.isnumeric() and int(text) > 23:
          self.alarmEntry.insert(0, '00:')
      case 3:
        if ':' not in text:
          self.alarmEntry.insert(2, ':')
          new_char = self.alarmEntry.get()[3]
          if new_char.isnumeric() and int(new_char) > 5:
            self.alarmEntry.insert(3, '0')
      case 4:
        new_char = self.alarmEntry.get()[3]
        if new_char.isnumeric() and int(new_char) > 5:
          self.alarmEntry.insert(3, '0')


  def format_alarm_advance_value(self, *args) -> bool:
    text = self.alarmAdvanceEntry.get()
    
    if len(text) == 2:
      self.alarmAdvanceEntry.delete(0,1)
    elif len(text) == 0:
      self.alarmAdvanceEntry.insert(0, '0')
      self.alarmAdvanceEntry.select_range(0,1)
  

  def update_config(self) -> None:
    alarm_value = self.alarmValue.get()
    alarm_advance_value = self.alarmAdvanceValue.get()

    if not re.match('^([01]\d|2[0-3]):[0-5]\d$', alarm_value):
      self.alarmValue.set('10:00')
      messagebox.showerror('Invalid Time!', 'O horário passado não é válido!\nDigite o horário no padrão 24 horas (HH:MM)')
      self.focus_set()
      return
    
    self.setup['alarm'] = alarm_value
    self.setup['default_advance'] = alarm_advance_value
    save_config(self.setup)
    self.destroy()


  def reset_config(self) -> None:
    self.alarmValue.set('09:30')
    self.alarmAdvanceValue.set('2')
