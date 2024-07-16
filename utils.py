from datetime import datetime, timedelta
from os.path import realpath, dirname
import json

def save_config(config: dict) -> bool:
  if type(config) != type({}):
    err = 'Invalid type of config.'
    raise ValueError(err)
  try:
    with open(f'{realpath(dirname(__file__))}/config.json', 'w') as file:
      json_config = json.dumps(config, indent=2)
      file.write(json_config)
      return True
  except:
    return False

def load_config() -> dict:
  try:
    with open(f'{realpath(dirname(__file__))}/config.json', 'r') as file:
      json_text = file.read()
      return json.loads(json_text)
  except FileNotFoundError:
    return None
  
def get_curr_date() -> datetime.date:
  return datetime.now().date()

def get_n_days_after(n: int, from_date: datetime | None = None) -> datetime.date:
  if not from_date:
    return (datetime.now() + timedelta(days=n)).date()
  return (from_date + timedelta(days=n)).date()

def get_n_days_before(n: int, from_date: datetime | None = None) -> datetime.date:
  if not from_date:
    return (datetime.now() - timedelta(days=n)).date()
  return (from_date - timedelta(days=n)).date()

def parse_str_date(str_date: str, date_format: str = '%d-%m-%Y') -> datetime.date:
  return datetime.strptime(str_date, date_format).date()

def stringify_date(date: datetime, date_format: str = '%d-%m-%Y') -> str:
  return datetime.strftime(date, date_format)
