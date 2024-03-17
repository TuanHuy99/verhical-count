import mysql.connector
import hashlib

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password='root',
  database = 'veco',
  # consume_results=True
  autocommit=True,
    connect_timeout=900000,
)

def ma_hoa_mk(password):
  """

  """
  return hashlib.md5(password.encode()).hexdigest()

def login(user, password):
  """

  """
  mycursor = mydb.cursor()
  text = f"SELECT role FROM login where login.userName='{user}' and password='{password}'"
  mycursor.execute(text)

  result = 0
  for x in mycursor:
    result = x
  if result:
    return result[0]
  return None

def addUser(user, password, role='user'):
  '''

  '''
  # Check User
  if checkUser(user):
    return False

  password = ma_hoa_mk(password)

  mycursor = mydb.cursor()
  text = f'INSERT INTO login VALUES("{user}", "{password}", "{role}");'
  mycursor.execute(text)
  mydb.commit()

  return True


def checkUser(user):
  '''

  '''
  mycursor = mydb.cursor()
  text = f"SELECT role FROM login where login.userName='{user}';"
  mycursor.execute(text)

  result = 0
  for x in mycursor:
    result = x

  if result:
    return True

  return False

def removeUser(user):
  if checkUser(user):
    return False

  mycursor = mydb.cursor()
  text = f"DELETE FROM login WHERE userName='{user}';"
  mycursor.execute(text)
  mydb.commit()

  return True
