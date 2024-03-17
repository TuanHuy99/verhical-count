import mysql.connector
import datetime
import random
import string
import time
import threading

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password='root',
  database = 'veco',
  consume_results=True,
  autocommit=True,
  connect_timeout=900000,
)

# def ping_connection():
#     while True:
#         time.sleep(60)  # Chờ 60 giây (hoặc thời gian cần thiết)
#         mydb.ping(reconnect=True)
#
# # Tạo một luồng riêng để thực hiện ping kết nối
# ping_thread = threading.Thread(target=ping_connection)
# ping_thread.start()

def updateProject(projectID, day_upload):
    '''

    '''
    mycursor = mydb.cursor()

    text = f"UPDATE projects SET uploadDay = '{day_upload}' WHERE projectId = '{projectID}'"
    print(f'TEXT: {text}')
    mycursor.execute(text)
    mydb.commit()

    return True

def get_all_project_wait_list():

    mycursor = mydb.cursor()
    text = f"SELECT * FROM wait_list"
    mycursor.execute(text)
    result = []
    for x in mycursor:
        result.append(x[0])
    if result:
        return result
    return False
######################################################################
def check_project_numclass(project_id, num_class):
    '''

    Args:
        project_id:
        num_class:

    Returns:    True if project is processing
                False if project is not processing

    '''
    mycursor = mydb.cursor()
    text = f"select * from processing where project_id='{project_id}' and num_class={num_class}"
    mycursor.execute(text)

    result = mycursor.fetchone()  # Lấy kết quả của truy vấn

    if result is not None:
        # print("Phần tử tồn tại trong bảng.")
        return True
    else:
        return False

######################################################################
def check_need_download():
    '''

    Args:
        project_id:
        num_class:

    Returns:    True if project is processing
                False if project is not processing

    '''
    mycursor = mydb.cursor()
    text = f"select * from need_download;"
    mycursor.execute(text)

    result = mycursor.fetchone()  # Lấy kết quả của truy vấn

    if result is not None:
        # print("Phần tử tồn tại trong bảng.")
        return True
    else:
        return False

######################################################################
def add_processing_project(project_id, num_class):
    ''''''
    mycursor = mydb.cursor()

    text = f"insert into processing values('{project_id}', '{num_class}');"
    print(f'TEXT: {text}')
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def remove_processing_project(project_id, num_class):
    mycursor = mydb.cursor()

    text = f"DELETE FROM processing where project_id='{project_id}' and num_class={num_class};"
    print(f'TEXT: {text}')
    mycursor.execute(text)
    mydb.commit()

    return True
######################################################################
def get_projectID(project_name):
    mycursor = mydb.cursor()
    text = f"SELECT projectID FROM projects where name='{project_name}'"
    mycursor.execute(text)

    result = 0
    for x in mycursor:
        result = x
    if result:
        return result[0]
    return None

######################################################################
def get_project_name(projectID):
    mycursor = mydb.cursor()
    text = f"SELECT name FROM projects where projectID='{projectID}'"
    mycursor.execute(text)

    result = 0
    for x in mycursor:
        result = x
    if result:
        return result[0]
    return None

######################################################################
def get_project_name_wait_list(projectID):
    mycursor = mydb.cursor()
    text = f"SELECT name FROM wait_list where project_id='{projectID}'"
    mycursor.execute(text)

    result = 0
    for x in mycursor:
        result = x
    if result:
        return result[0]
    return None

######################################################################
def addProject(randomID, day_upload, num_video, size, owner, name):
    '''

    '''
    mycursor = mydb.cursor()

    text = f"insert into projects values('{randomID}', '{day_upload}', {num_video}, {size}, '{owner}', '{name}');"
    print(f'TEXT: {text}')
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def check_projectID(projectID):
    '''
    Trung ID: True
    Khong trung ID: false
    '''
    mycursor = mydb.cursor()
    text = f"SELECT * FROM projects where projectID='{projectID}'"
    mycursor.execute(text)

    result = 0
    for x in mycursor:
        result = x
    if result:
        return True
    return False

######################################################################
def addVideos(projectID, video_name, num_frame, fps, size):
    '''

    '''
    mycursor = mydb.cursor()
    text = f"insert into videos values('{projectID}', '{video_name}', {size} , {str(num_frame)}, {str(fps)});"
    print("TEXT: ", text)
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def removeProject(projectID):
    '''

    '''
    mycursor = mydb.cursor()
    text = f"DELETE FROM projects WHERE projectID='{projectID}';"
    mycursor.execute(text)
    mydb.commit()

    text = f"DELETE FROM videos WHERE projectID='{projectID}';"
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def addResult(user, projectID, dateUload, result):
    '''

    '''
    mycursor = mydb.cursor()
    text = f'insert into processed values ("{user}", "{projectID}", "{dateUload}", "{result}");'
    print("TEXT: ", text)
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################

def get_first_link_to_download():
    '''

    Returns:

    '''
    mycursor = mydb.cursor()
    text = f"SELECT * FROM need_download ORDER BY day_upload ASC LIMIT 1;"
    mycursor.execute(text)

    result = mycursor.fetchone()  # Lấy kết quả của truy vấn

    return result

######################################################################
def add_need_download(link, type, name, num_class, day_upload, user):
    '''

    Args:
        link:
        type:
        name:
        num_class:
        day_upload:

    Returns:

    '''
    mycursor = mydb.cursor()
    text = f'insert into need_download values ("{link}", "{type}", "{name}", "{num_class}", "{day_upload}", "{user}");'
    print("TEXT: ", text)
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def remove_need_download(link, type=''):
    '''

    Args:
        link:
        type:
        name:

    Returns:

    '''
    mycursor = mydb.cursor()
    text = f"DELETE FROM need_download WHERE link='{link}';"
    print(text)
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def add_downloaded(link, type, save_dir, time_done):
    '''

    Args:
        link:
        type:
        save_dir:
        time_done:

    Returns:

    '''
    mycursor = mydb.cursor()
    text = f'insert into downloaded values ("{link}", "{type}", "{save_dir}", "{time_done}");'
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def add_wait_list(project_id, num_class, time_create, user, name):
    '''

    Args:
        project_id:
        num_class:
        time_create:
        user:
        name:

    Returns:

    '''
    mycursor = mydb.cursor()
    text = f'insert into wait_list values ("{project_id}", "{num_class}", "{time_create}", "{user}", "{name}");'
    print(text)
    mycursor.execute(text)
    mydb.commit()

    return True

######################################################################
def remove_wait_list(project_id, num_class, user):
    '''

    Args:
        dir_path:
        num_class:
        user:

    Returns:

    '''
    mycursor = mydb.cursor()
    text = f'DELETE FROM wait_list WHERE project_id="{project_id}" AND num_class={num_class};'
    print(text)
    mycursor.execute(text)
    mydb.commit()

    return True

def get_first_wait_list():
    '''

    Returns:

    '''
    mycursor = mydb.cursor()
    text = f"SELECT * FROM wait_list ORDER BY time_create ASC LIMIT 1;"
    mycursor.execute(text)

    result = mycursor.fetchone()  # Lấy kết quả của truy vấn

    return result

######################################################################
def check_processing():
    '''

    Returns: True if processing
            False if not processing

    '''
    mycursor = mydb.cursor()
    text = f"SELECT * FROM processing LIMIT 1;"
    mycursor.execute(text)

    result = mycursor.fetchone()  # Lấy kết quả của truy vấn

    if result:
        return True

    return False

######################################################################
def get_all_error_link(user):

    mycursor = mydb.cursor()
    text = f"SELECT * FROM error_link WHERE user='{user}' ORDER BY upload_time DESC;"
    mycursor.execute(text)
    result = []
    for x in mycursor:
        result.append([x[0], x[1], x[-1]])
    if result:
        return result
    return False

######################################################################
def add_error_link(link, name, id, user, time_upload):
    '''

    '''
    mycursor = mydb.cursor()
    text = f'insert into error_link values ("{link}", "{name}", "{id}", "{user}", "{time_upload}");'
    print(text)
    mycursor.execute(text)
    mydb.commit()

    return True
