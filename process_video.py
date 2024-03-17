import shutil
import subprocess
import threading

from APIs.get_video_in4 import get_video_information
from ultralytics import YOLO
import cv2
import json
import os
import datetime
import gdown
import dropbox
import urllib.request
import random
import string
import zipfile

from APIs.truy_van import add_processing_project, remove_processing_project, get_first_link_to_download, add_wait_list, \
    get_first_wait_list, addVideos, addProject, check_processing, remove_need_download, add_downloaded, \
    remove_wait_list, add_error_link, removeProject
from APIs.truy_van import check_projectID, get_project_name, updateProject

# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def bytes_to_gb(bytes):
    gb = bytes / (1024.0**3)
    return round(gb, 3)

def check_size(dir_path):
    size = 0

    # get size
    for ele in os.scandir(dir_path):
        size += os.path.getsize(ele)

    size = bytes_to_gb(size)
    return size

def check_size_file(file_path):
    size = os.path.getsize(file_path)
    size = bytes_to_gb(size)

    return size
def find_center(xyxy):
    x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
    cx = (x2 + x1) / 2
    cy = (y2 + y1) / 2
    return int(cx), int(cy)

def find_left_center(xyxy):
    x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
    cy = (y2 + y1) / 2
    return x1, int(cy)

def find_H20_center(xyxy):
    xc,yc = find_center(xyxy)
    xb,yb = find_bottom_center(xyxy)
    return xb, int(yb-((yb-yc)*2)/20)

def find_bottom_center(xyxy):
    x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
    cx = (x2 + x1) / 2
    return int(cx), y2

def find_one_third_center(xyxy):
    x1, y1, x2, y2 = round(xyxy[0], 2), round(xyxy[1], 2), round(xyxy[2], 2), round(xyxy[3], 2)
    cx = x2/3 + 2*x1/ 3
    cy = y2
    return float(round(cx, 2)), float(round(cy, 2))

def most_frequent_element(list1):
    return max(set(list1), key=list1.count)

def get_video_files(directory):
    video_files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            # Kiểm tra phần mở rộng của tệp tin
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in ['.mp4', '.avi', '.mkv', '.mov']:
                video_files.append(filename)
    return video_files

def create_json_file(path_video, project_id, num_class=5):
    print(f"Start_task {path_video} {num_class} class")
    add_processing_project(project_id=project_id, num_class=num_class)
    # print(num_class, type(num_class))
    if int(num_class) == 5:
        weight_path = ''
        # weight_path = 'D:/New folder/veco-v6_2_speed/weights/best_40kdata.pt/'
    elif int(num_class) == 9:
        weight_path = ''
        # weight_path = 'D:/New folder/veco-v6_2_speed/weights/best_9class40k.pt'

    videos = get_video_files(path_video)
    videos.sort()
    print("Hello 123: ", videos)
    dict_data = {}
    num_frame = 0

    model = YOLO(weight_path)
    results = model.track(source=path_video,
                          stream=True, device=0,
                          save=True, project=path_video,
                          name=f'{num_class}_class/track',
                          tracker='bytetrack.yaml', hide_conf=True,
                          verbose=True)

    for rs in results:
        # print(num_frame)
        if not num_frame:
            print('save')
            cv2.imwrite(f'{path_video}/raw_img.jpg', rs.orig_img)

        # print('img: ', rs.visualize())
        boxes = rs.boxes.cpu().numpy()
        for box in boxes:
            # print('img: ', box.data)
            cls = int(box.cls[0])
            # print('class: ', cls)
            cx, cy = find_center(box.xyxy[0])
            c_b_x, c_b_y = find_bottom_center(box.xyxy[0])
            c_l_x, c_l_y = find_H20_center(box.xyxy[0])
            c_13_x, c_13_y = find_one_third_center(box.xyxy[0])
            try:
                id = int(box.id[0])
                # print('id: ', id)

                if id in dict_data:
                    dict_data[id]['cls'].append(cls)
                    dict_data[id]['frame'].append([cx, cy, num_frame])
                    dict_data[id]['bottom_center'].append([c_b_x, c_b_y, num_frame])
                    dict_data[id]['H20_center'].append([c_l_x, c_l_y, num_frame])
                    dict_data[id]['one_third_center'].append([c_13_x, c_13_y, num_frame])
                else:
                    dict_data[id] = {
                        'cls': [],
                        'frame': [],
                        'bottom_center': [],
                        'H20_center': [],
                        'one_third_center': []
                    }

                    dict_data[id]['cls'].append(cls)
                    dict_data[id]['frame'].append([cx, cy, num_frame])
                    dict_data[id]['bottom_center'].append([c_b_x, c_b_y, num_frame])
                    dict_data[id]['H20_center'].append([c_l_x, c_l_y, num_frame])
                    dict_data[id]['one_third_center'].append([c_13_x, c_13_y, num_frame])
            except:
                continue
        num_frame += 1
    with open(f"{path_video}/data_point_{num_class}.json", "w") as outfile:
        json.dump(dict_data, outfile)

    create_line_img(path_video + "/", num_class=num_class)
    remove_processing_project(project_id=project_id, num_class=num_class)
    print("End background Task")


def create_line_img(dir_path, num_class=5):
    f = open(f"{dir_path}/data_point_{num_class}.json", 'r')
    data = json.load(f)
    ids = list(data.keys())

    colors = [(255, 128, 0), (255, 153, 51), (255, 178, 102), (230, 230, 0), (255, 153, 255),
              (153, 204, 255), (255, 102, 255), (255, 51, 255), (102, 178, 255), (51, 153, 255),
              (255, 153, 153), (255, 102, 102), (255, 51, 51), (153, 255, 153), (102, 255, 102),
              (51, 255, 51), (0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 255)]
    img = cv2.imread(f"{dir_path}/raw_img.jpg")

    for id_ in ids:
        cls = most_frequent_element(data[id_]['cls'])
        #         print(f'{id_} co class la {cls}')
        for i in range(len(data[id_]['H20_center']) - 1):
            x1 = data[id_]['H20_center'][i][0]
            y1 = data[id_]['H20_center'][i][1]

            x2 = data[id_]['H20_center'][i + 1][0]
            y2 = data[id_]['H20_center'][i + 1][1]
            cv2.line(img, (x1, y1), (x2, y2), colors[cls], 1)

    cv2.imwrite(f'{dir_path}/line_road_{num_class}.jpg', img)

def download_video_gg_drive(directory_path, link_gg_drive):
    gdown.download_folder(url=link_gg_drive, output=directory_path)

######################################################################
def download_video_dropbox(directory_path, link_dropbox, key_dropbox=''):
    # Replace 'ACCESS_TOKEN' with your actual access token
    ACCESS_TOKEN = key_dropbox

    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    shared_link = dropbox.files.SharedLink(url=link_dropbox)

    listing = dbx.files_list_folder(path="", shared_link=shared_link)
    # todo: add implementation for files_list_folder_continue
    print("Dowloading...")

    for entry in listing.entries:
        if entry.name.endswith((".mp4", ".MP4", '.avi')):
            print(entry.name)
            with open(directory_path + '/' +entry.name, "wb") as f:
                # note: this simple implementation only works for files in the root of the folder
                metadata, res = dbx.sharing_get_shared_link_file(url=shared_link.url, path="/" + entry.name)
                # print(res.content)
                f.write(res.content)

def download_video_transfer(directory_path, link_transfer):
    command = ["./dropboxtransfer", "-d", "./"+directory_path, link_transfer]
    subprocess.run(command)

def download_from_links(link, type, save_dir, user, key_dropbox=''):
    save_path = os.path.join(f"static/users/{user}/", save_dir)
    os.makedirs(save_path, exist_ok=True)

    time_now = datetime.datetime.now()
    if type == 'dropbox':
        download_video_dropbox(link_dropbox=link, directory_path=save_path, key_dropbox=key_dropbox)
        remove_need_download(link=link, type='dropbox')
        add_downloaded(link=link, type='dropbox', save_dir=save_dir, time_done=time_now)
    elif type == 'gg-drive':
        download_video_gg_drive(link_gg_drive=link, directory_path=save_path)
        remove_need_download(link=link, type='gg-drive')
        add_downloaded(link=link, type='gg-drive', save_dir=save_dir, time_done=time_now)
    elif type == 'transfer':
        download_video_transfer(link_transfer=link, directory_path=save_path)
        remove_need_download(link=link, type='transfer')
        add_downloaded(link=link, type='transfer', save_dir=save_dir, time_done=time_now)
    elif type == 'zip':
        print(1.1)
        with zipfile.ZipFile(link, 'r') as zip_ref:
            zip_ref.extractall(save_path)
        print(1.2)
        remove_need_download(link=link, type='zip')
        add_downloaded(link=link, type='zip', save_dir=save_dir, time_done=time_now)

def background_download(key_dropbox=''):
    print("Downloading...")
    print("Thread name:", threading.current_thread().name)
    while get_first_link_to_download():
        randomID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        # Kiem tra xem ID da xuat hien chua. Neu da xuat hien se sinh ra 1 ID moi
        while (check_projectID(randomID)):
            randomID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


        link, type, name, num_class,day_upload, username = get_first_link_to_download()
        print(f'Downloading {name}')
        try:
            download_from_links(link=link, type=type, save_dir=randomID, user=username, key_dropbox=key_dropbox)
            print(f'Downloaded {name}')

            time_now = datetime.datetime.now()
            # Neu trong wait list khong co gi thi chay luon
            if not get_first_wait_list():
                print(100)
                add_wait_list(project_id=randomID, num_class=num_class, time_create=time_now, user=username, name=name)
                if not check_processing():
                    print(300)
                    process_wait_list()
                    # background_thread = threading.Thread(target=process_wait_list)
                    # background_thread.start()
                    # print("Thread name:", threading.current_thread().name)
                    # process_wait_list()
            else:
                print(200)
                add_wait_list(project_id=randomID, num_class=num_class, time_create=time_now, user=username, name=name)
        except:
            save_path = os.path.join(f"static/users/{username}/", randomID)
            remove_need_download(link=link)
            remove_wait_list(project_id=randomID, num_class=num_class, user=username)
            remove_processing_project(project_id=randomID, num_class=num_class)
            removeProject(project_id=randomID)
            add_error_link(link=link, name=name, id=randomID, user=username, time_upload=day_upload)

            shutil.rmtree(save_path)

            print(f'Error Link {name} !!!')


def process_wait_list():
    print("Dang chay wait list...")
    print(get_first_wait_list())
    while get_first_wait_list():
        print(10)
        project_id, num_class, time_create, username, project_name = get_first_wait_list()
        print(f"Dang xu ly {project_name}")
        directory_path = os.path.join(f"static/users/{username}/", project_id)
        videos = get_video_files(directory_path)
        print("Videos: ", videos)

        for video in videos:
            file_path = os.path.join(directory_path, video)
            f_size = check_size_file(file_path)
            f_fps, f_frames = get_video_information(file_path)

            addVideos(projectID=project_id, size=f_size, video_name=video, num_frame=f_frames, fps=f_fps)

            print(f_size, f_fps, f_frames)

        num_video = len(videos)
        size = check_size(directory_path)
        day_upload = datetime.datetime.now()

        create_json_file(directory_path, num_class=num_class,project_id=project_id)
        print(100)
        create_line_img(directory_path , num_class=num_class)
        print(200)
        remove_wait_list(project_id=project_id, num_class=num_class, user=username)
        if get_project_name(projectID=project_id):
            updateProject(projectID=project_id, day_upload=day_upload)
        else:
            addProject(randomID=project_id, day_upload=day_upload, num_video=num_video, owner=username, size=size,
                    name=project_name)
        print(f"Da xu ly xong het project {project_name}")
    print(20)
