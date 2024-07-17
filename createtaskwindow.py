import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, BooleanVar
from utils import *
import re


class CreateTaskWindow(tk.Toplevel):
  def __init__(self) -> None:
    super().__init__()
    today_date = stringify_date(get_curr_date())

    self.title('Create new Task')
    self.config(padx=10, pady=10)
    self.columnconfigure(2, weight=3)
    self.resizable(False, False)

    self.setup = load_config()
    self.date_checker = self.register(validate_date)
    self.alarm_checker = self.register(validate_alarm)
    self.alarm_advance_checker = self.register(validate_alarm_advance)

    self.headerLabel = ttk.Label(self, text='Criar Nova Tarefa', font=('Arial', 13)).grid(row=0, column=0, columnspan=3, sticky='n', pady=(5, 11))

    self.taskNameValue = StringVar(self, value='Nova Tarefa')
    self.taskNameLabel = ttk.Label(self, text='Nome:').grid(row=1, column=0, padx=(10, 5), pady=(5, 0), sticky='w')
    self.taskNameEntry = ttk.Entry(self, textvariable=self.taskNameValue, font=('Arial', 13))
    self.taskNameEntry.grid(row=1, column=1, columnspan=2, padx=(5, 10), pady=(5, 0), sticky='nsew')
    self.taskNameEntry.focus_set()
    self.taskNameEntry.select_range(0, len(self.taskNameValue.get()))

    self.taskDescriptionValue = StringVar(self)
    self.taskDescriptionLabel = ttk.Label(self, text='Descrição:').grid(row=2, column=0, padx=(10, 5), pady=(5, 0), sticky='w')
    self.taskDescriptionEntry = ttk.Entry(self, textvariable=self.taskDescriptionValue, font=('Arial', 13)).grid(row=2, column=1, columnspan=2, padx=(5, 10), pady=(5, 0), sticky='nsew')

    self.taskDateValue = StringVar(self, value=today_date)
    self.taskDateValue.trace_add('write', self.format_date_value)
    self.taskDateLabel = ttk.Label(self, text='Dia:').grid(row=3, column=0, padx=(10, 5), pady=(5, 0), sticky='w')
    self.taskDateEntry = ttk.Entry(self, textvariable=self.taskDateValue, validate='key', validatecommand=(self.date_checker, '%P'), font=('Arial', 13), width=10)
    self.taskDateEntry.grid(row=3, column=1, columnspan=2, padx=(5, 10), pady=(5, 0), sticky='w')

    self.taskAlarmValue = StringVar(self, value='09:00')
    self.taskAlarmValue.trace_add('write', self.format_alarm_value)
    self.taskAlarmLabel = ttk.Label(self, text='Horário:').grid(row=4, column=0, padx=(10, 5), pady=(5, 0), sticky='w')
    self.taskAlarmEntry = ttk.Entry(self, textvariable=self.taskAlarmValue, validate='key', validatecommand=(self.alarm_checker, '%P'), font=('Arial', 13), width=5, justify='center')
    self.taskAlarmEntry.grid(row=4, column=1, columnspan=2, padx=(5, 10), pady=(5, 0), sticky='w')

    self.useCustomTaskAlarmAdvanceValue = BooleanVar(self, value=False)
    self.taskAlarmAdvanceCheckbox = ttk.Checkbutton(self, text='Personalizar antecedência', variable=self.useCustomTaskAlarmAdvanceValue, command=self.toggle_task_alarm_advance_state)
    self.taskAlarmAdvanceCheckbox.grid(row=5, column=0, columnspan=3, padx=(10, 5), pady=(20, 0), sticky='w')

    self.taskAlarmAdvanceValue = IntVar(self, value=self.setup.get('default_advance'))
    self.taskAlarmAdvanceValue.trace_add('write', self.format_alarm_advance_value)
    self.taskAlarmAdvanceLabel1 = ttk.Label(self, text='Avisar', state='disabled')
    self.taskAlarmAdvanceLabel1.grid(row=6, column=0, padx=(10, 0), pady=(5, 0), sticky='e')
    self.taskAlarmAdvanceEntry = ttk.Entry(self, textvariable=self.taskAlarmAdvanceValue, validate='key', validatecommand=(self.alarm_advance_checker, '%P'), font=('Arial', 13), width=2, justify='center', state='disabled')
    self.taskAlarmAdvanceEntry.grid(row=6, column=1, padx=5, pady=(5, 0), sticky='w')
    self.taskAlarmAdvanceLabel2 = ttk.Label(self, text='dias antes', state='disabled')
    self.taskAlarmAdvanceLabel2.grid(row=6, column=2, padx=(0, 5), pady=(5, 0), sticky='w')

    self.createTaskButton = ttk.Button(self, text='Criar Tarefa', command=self.save_new_task).grid(row=7, column=0, padx=(10, 5), pady=(15, 10), sticky='w')
    self.cancelButton = ttk.Button(self, text='Cancelar', command=self.destroy).grid(row=7, column=1, columnspan=2, padx=(0, 10), pady=(15, 10), sticky='w')


  def toggle_task_alarm_advance_state(self) -> None:
    is_using = self.useCustomTaskAlarmAdvanceValue.get()
    self.taskAlarmAdvanceEntry['state'], self.taskAlarmAdvanceLabel1['state'], self.taskAlarmAdvanceLabel2['state'] = ['enabled'] * 3 if is_using else ['disabled'] * 3

    if is_using:
      self.taskAlarmAdvanceEntry.focus_set()
      self.taskAlarmAdvanceEntry.select_range(0,1)


  def format_alarm_value(self, *args) -> None:
    text = self.taskAlarmValue.get()

    match len(text):
      case 1:
        if ':' in text:
          self.taskAlarmEntry.insert(0, '00')
        elif text.isnumeric() and int(text) > 2:
          self.taskAlarmEntry.insert(0, '0')
      case 2:
        if text.isnumeric() and int(text) > 23:
          self.taskAlarmEntry.insert(0, '00:')
      case 3:
        if ':' not in text:
          self.taskAlarmEntry.insert(2, ':')
          new_char = self.taskAlarmEntry.get()[3]
          if new_char.isnumeric() and int(new_char) > 5:
            self.taskAlarmEntry.insert(3, '0')
      case 4:
        new_char = self.taskAlarmEntry.get()[3]
        if new_char.isnumeric() and int(new_char) > 5:
          self.taskAlarmEntry.insert(3, '0')


  def format_alarm_advance_value(self, *args) -> None:
    text = self.taskAlarmAdvanceEntry.get()
    
    if len(text) == 2:
      self.taskAlarmAdvanceEntry.delete(0,1)
    elif len(text) == 0:
      self.taskAlarmAdvanceEntry.insert(0, '0')
      self.taskAlarmAdvanceEntry.select_range(0,1)

  
  def format_date_value(self, *args) -> None:
    ...


  def save_new_task(self) -> None:
    task_name = self.taskNameValue.get()
    task_description = self.taskDescriptionValue.get()
    task_time = self.taskAlarmValue.get()
    task_alarm_advance = self.taskAlarmAdvanceValue.get()

    if not re.match('^([01]\\d|2[0-3]):[0-5]\\d$', task_time):
      self.taskAlarmValue.set('10:00')
      messagebox.showerror('Invalid Time!', 'O horário passado não é válido!\nDigite o horário no padrão 24 horas (HH:MM)')
      self.focus_set()
      return
    
    new_task = {
      'name': task_name,
      'description': task_description,
      'time': task_time,
      'alarm_advance': task_alarm_advance if self.useCustomTaskAlarmAdvanceValue.get() else 'default'
    }

    curr_tasks: list[dict] = self.setup['tasks']
    for idx, task in enumerate(curr_tasks):
      if task_name in task.get('name'):
        overwrite_permission = True if messagebox.askyesno('Task already exists!', 'Já existe uma tarefa com esse nome!\nDeseja sobrescrever a tarefa?') else False
        if overwrite_permission:
          self.setup['tasks'][idx] = new_task
          save_config(self.setup)
          self.destroy()

        return
        
    self.setup['tasks'].append(new_task)
    save_config(self.setup)
    self.destroy()


# CreateTaskWindow().mainloop()