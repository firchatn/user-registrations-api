from passlib.context import CryptContext
import random
from datetime import datetime
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def get_code():
    return str(random.randint(1000,9999))

def get_seconds(d1 : str, d2 : str):
    date_format_str = '%Y-%m-%d %H:%M:%S'
    start = datetime.strptime(d1.split(".")[0], date_format_str)
    end =   datetime.strptime(d2.split(".")[0], date_format_str)
    diff = end - start
    return diff.total_seconds()

def is_email(email):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,email):
      return True
   return False