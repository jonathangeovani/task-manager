from datetime import datetime, timedelta
import json

def save_config(config: dict) -> bool:
  if type(config) != type({}):
    err = 'Invalid type of config.'
    raise ValueError(err)
  try:
    with open('config.json', 'w') as file:
      json_config = json.dumps(config)
      file.write(json_config)
  except Exception as err:
    print('Error:', err)
    return False
  return True

def load_config() -> dict:
  with open('config.json', 'r') as file:
    json_text = file.read()
    return json.loads(json_text)
  
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

save_config(["olá", "tudo", "bem"])

teste = load_config()

print(teste)