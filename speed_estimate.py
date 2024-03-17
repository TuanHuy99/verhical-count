import json
import math
import statistics
from datetime import timedelta, datetime
import cv2
import pandas as pd
from sklearn.linear_model import LinearRegression

from process_video import get_video_files

list_vehicle = ["Motor", "Car", "Bus", "LGV", "HGV", "ALL"]

def convert_string_to_datetime(date_string, format):
    '''
    Args:
        date_string:
        format:

    Returns:

    '''
    return datetime.strptime(date_string, format)

def get_start_end_time(video_dir):
    '''
    Args:
        video_dir:

    Returns:

    '''
    try:
        videos = get_video_files(video_dir)
        videos.sort()

        # Mở video và lấy thông tin
        video = cv2.VideoCapture(f"{video_dir}/{videos[0]}")
        fps = video.get(cv2.CAP_PROP_FPS)
        print("FPS của video là:", fps)
        video.release()  # Đóng video sau khi hoàn thành

        start_video_name = videos[0].split(".")[0]
        end_video_name = videos[-1].split(".")[0]
        # print(start_video_name)
        get_day_start, get_time_start, _ = start_video_name.split("_")
        get_day_end, get_time_end, _ = end_video_name.split("_")

        year_start, month_start, day_start = get_day_start[:4], get_day_start[4:6], get_day_start[-2:]
        hour_start, minute_start, sec_start = get_time_start[:2], get_time_start[2:4], get_time_start[-2:]

        year_end, month_end, day_end = get_day_end[:4], get_day_end[4:6], get_day_end[-2:]
        hour_end, minute_end, sec_end = get_time_end[:2], int(get_time_end[2:4]) + 10, get_time_end[-2:]

        str_time_start = f"{year_start}-{month_start}-{day_start}T{hour_start}:{minute_start}:{sec_start}"
        str_time_end = f"{year_end}-{month_end}-{day_end}T{hour_end}:{minute_end}:{sec_end}"

        return str_time_start, str_time_end, fps
    except:
        return '2023-01-01T01:00:00', '2023-01-01T02:00:00', 30

def convert_frame_to_sec(frame, FPS):
    '''
    Args:
        frame:
        FPS:

    Returns:

    '''
    sec = frame / FPS
    return round(sec, 0)

def add_seconds_to_datetime(dt, seconds):
    '''
    Args:
        dt:
        seconds:

    Returns:

    '''
    abc = dt + timedelta(seconds=seconds)
    formatted_datetime = abc.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return formatted_datetime

def find_common_elements(list1, list2):
    '''

    Args:
        list1: List thu nhat
        list2: List thu hai

    Returns:
        common_elements: list chua cac phan tu co trong ca 2 mang

    '''
    set1 = set(list1)
    set2 = set(list2)
    common_elements = list(set1.intersection(set2))
    return common_elements

def calculate_average(lst):

    if len(lst) == 0:
        return 0  # Tránh chia cho 0
    total = sum(lst)
    average = total / len(lst)
    return average

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def train_distance_model(list_D, list_locate):
    reg = LinearRegression().fit(list_locate, list_D)
    return reg


def predict_distance(model, new_locate):
    return abs(model.predict(new_locate)[0])

def caculate_speed_v1(user, projectID, distance_in_pixel, distance_in_meter, time_start_str, time_end_str, FPS, num_class=5):
    f = open(f"static/users/{user}/{projectID}/speed.json", 'r')

    if len(time_start_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_start = convert_string_to_datetime(time_start_str, date_format)
    if len(time_end_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_end = convert_string_to_datetime(time_end_str, date_format)

    data = json.load(f)

    line0 = data['0']
    line1 = data['1']

    common_item = find_common_elements(list(line0.keys()), list(line1.keys()))

    all_speed = {}
    speed_each_class = {}
    speed_each_values = {
        '<40': {},
        '40~60': {},
        '60~80': {},
        '80~120': {},
        '>120': {}
    }
    speed_excel = {
        'Time Range': [],
        'ID': [],
        'Class': [],
        'Time in': [],
        'Time out': [],
        'Travel time (s)': [],
        'Speed (km/h)': [],
        'Distance (m)': []
    }
    for item in common_item:
        # print(line0[item])
        # thoi gian khi cat line 0 (frame) va toa do khi do
        t1 = line0[item][1]     # frame vao
        d1 = line0[item][-1]    # toa do khi do

        # thoi gian khi cat line 1 (frame) va toa do khi do
        t2 = line1[item][1]
        d2 = line1[item][-1]

        # tinh thoi gian di chuyen
        time_frame = abs(t1 - t2) # don vi: frame
        time_sec = round(time_frame / FPS, 3) #don vi: sec

        # tinh khoang cach di chuyen
        distance_frame = calculate_distance(d1[0], d1[1], d2[0], d2[1]) # don vi: pixel
        distance_in_m = distance_frame / distance_in_pixel * distance_in_meter # don vi: m

        # tinh toc do
        if not   time_sec:
            pass
        else:
            speed = round(distance_in_m / time_sec * 3.6, 1) # m/s -> km/h
            all_speed[item] = speed
            cls = str(line0[item][0])

            # tao dict chua thong tin ve speed cua tung class
            if cls in speed_each_class:
                speed_each_class[cls].append(speed)
            else:
                speed_each_class[cls] = []
                speed_each_class[cls].append(speed)

            # Tao dict chua thong tin ve speed theo tung khoang chia
            if speed < 40:
                if cls not in speed_each_values['<40']:
                    speed_each_values['<40'][cls] = 0
                speed_each_values['<40'][cls] += 1
            elif speed>=40 and speed<60 :
                if cls not in speed_each_values['40~60']:
                    speed_each_values['40~60'][cls] = 0
                speed_each_values['40~60'][cls] += 1
            elif speed>=60 and speed<80 :
                if cls not in speed_each_values['60~80']:
                    speed_each_values['60~80'][cls] = 0
                speed_each_values['60~80'][cls] += 1
            elif speed>=80 and speed<=120 :
                if cls not in speed_each_values['80~120']:
                    speed_each_values['80~120'][cls] = 0
                speed_each_values['80~120'][cls] += 1
            elif speed>120 :
                if cls not in speed_each_values['>120']:
                    speed_each_values['>120'][cls] = 0
                speed_each_values['>120'][cls] += 1

        # Tao dict chua thong tin de xuat file excel
        speed_excel['Time range'].append("01:00")
        speed_excel['ID'].append(item)
        speed_excel['Class'].append(list_vehicle[int(cls)])
        if t1 < t2:
            sec_in, sec_out = convert_frame_to_sec(t1, FPS), convert_frame_to_sec(t2, FPS)
            time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                     sec_out)
        else:
            sec_in, sec_out = convert_frame_to_sec(t2, FPS), convert_frame_to_sec(t1, FPS)
            time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                     sec_out)
        speed_excel['Time in'].append(str(time_in))
        speed_excel['Time out'].append(str(time_out))
        speed_excel['Travel time (s)'].append(time_sec)
        speed_excel['Speed (km/h)'].append(speed)
        speed_excel['Distance (m)'].append(round(distance_in_m, 3))

    speed_class_infor = {}
    for i in range (num_class):
        i = str(i)
        if i not in speed_each_class:
            speed_class_infor[i] = {
                'amount': 0,
                'medium': 0,
                'max': 0,
                'min': 0
            }
        else:
            speed_class_infor[i] = {
                'amount': len(speed_each_class[i]),
                'medium': round(calculate_average(speed_each_class[i]), 1),
                'max': max(speed_each_class[i]),
                'min': min(speed_each_class[i])
            }

        for key in speed_each_values:
            if i not in speed_each_values[key]:
                speed_each_values[key][i] = 0
    # print('speed_class_infor: ', speed_class_infor)
    # print('speed_each_class: ', speed_each_class)
    # print('speed_each_values: ', speed_each_values)
    # print('speed_excel: ', speed_excel)

    speed_excel = pd.DataFrame(speed_excel)
    # print(speed_excel)
    speed_excel = speed_excel.sort_values('Time in')
    speed_excel.to_excel(f'static/users/{user}/{projectID}/speed.xlsx', index=False)
    # print(speed_excel)
    return speed_class_infor, speed_each_values


def caculate_speed_v2(user, projectID, distance_in_meter, time_start_str, time_end_str, FPS, num_class=5):
    if num_class==9:
        list_vehicle = ["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV", "ALL"]
    f = open(f"static/users/{user}/{projectID}/speed.json", 'r')
    if len(time_start_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_start = convert_string_to_datetime(time_start_str, date_format)
    if len(time_end_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_end = convert_string_to_datetime(time_end_str, date_format)

    data = json.load(f)

    line0 = data['0']
    line1 = data['1']

    common_item = find_common_elements(list(line0.keys()), list(line1.keys()))

    all_speed = {}
    speed_each_class = {}
    speed_each_values = {
        '<40': {},
        '40~60': {},
        '60~80': {},
        '80~120': {},
        '>120': {}
    }
    speed_excel = {
        'Time range': [],
        'ID': [],
        'Class': [],
        'Time in': [],
        'Time out': [],
        'Travel time (s)': [],
        'Speed (km/h)': [],
        'Distance (m)': []
    }
    for item in common_item:
        # print(line0[item])
        # thoi gian khi cat line 0 (frame) va toa do khi do
        t1 = line0[item][1]     # frame vao
        # d1 = line0[item][-1]    # toa do khi do

        # thoi gian khi cat line 1 (frame) va toa do khi do
        t2 = line1[item][1]
        # d2 = line1[item][-1]

        # tinh thoi gian di chuyen
        time_frame = abs(t1 - t2) # don vi: frame
        time_sec = round(time_frame / FPS, 3) #don vi: sec

        # tinh khoang cach di chuyen
        # distance_frame = calculate_distance(d1[0], d1[1], d2[0], d2[1]) # don vi: pixel
        # distance_in_m = distance_frame / distance_in_pixel * distance_in_meter # don vi: m

        # tinh toc do
        if not   time_sec:
            pass
        else:
            speed = round(distance_in_meter / time_sec * 3.6, 1) # m/s -> km/h
            all_speed[item] = speed
            cls = str(line0[item][0])

            # tao dict chua thong tin ve speed cua tung class
            if cls in speed_each_class:
                speed_each_class[cls].append(speed)
            else:
                speed_each_class[cls] = []
                speed_each_class[cls].append(speed)

            # Tao dict chua thong tin ve speed theo tung khoang chia
            if speed < 40:
                if cls not in speed_each_values['<40']:
                    speed_each_values['<40'][cls] = 0
                speed_each_values['<40'][cls] += 1
            elif speed>=40 and speed<60 :
                if cls not in speed_each_values['40~60']:
                    speed_each_values['40~60'][cls] = 0
                speed_each_values['40~60'][cls] += 1
            elif speed>=60 and speed<80 :
                if cls not in speed_each_values['60~80']:
                    speed_each_values['60~80'][cls] = 0
                speed_each_values['60~80'][cls] += 1
            elif speed>=80 and speed<=120 :
                if cls not in speed_each_values['80~120']:
                    speed_each_values['80~120'][cls] = 0
                speed_each_values['80~120'][cls] += 1
            elif speed>120 :
                if cls not in speed_each_values['>120']:
                    speed_each_values['>120'][cls] = 0
                speed_each_values['>120'][cls] += 1

        # Tao dict chua thong tin de xuat file excel
        speed_excel['Time range'].append("01:00")
        speed_excel['ID'].append(item)
        speed_excel['Class'].append(list_vehicle[int(cls)])
        if t1 < t2:
            sec_in, sec_out = convert_frame_to_sec(t1, FPS), convert_frame_to_sec(t2, FPS)
            time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                     sec_out)
        else:
            sec_in, sec_out = convert_frame_to_sec(t2, FPS), convert_frame_to_sec(t1, FPS)
            time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                     sec_out)
        speed_excel['Time in'].append(str(time_in))
        speed_excel['Time out'].append(str(time_out))
        speed_excel['Travel time (s)'].append(time_sec)
        speed_excel['Speed (km/h)'].append(speed)
        speed_excel['Distance (m)'].append(distance_in_meter)

    speed_class_infor = {}
    for i in range (num_class):
        i = str(i)
        if i not in speed_each_class:
            speed_class_infor[i] = {
                'amount': 0,
                'medium': 0,
                'max': 0,
                'min': 0
            }
        else:
            speed_class_infor[i] = {
                'amount': len(speed_each_class[i]),
                'medium': round(calculate_average(speed_each_class[i]), 1),
                'max': max(speed_each_class[i]),
                'min': min(speed_each_class[i])
            }

        for key in speed_each_values:
            if i not in speed_each_values[key]:
                speed_each_values[key][i] = 0
    # print('speed_class_infor: ', speed_class_infor)
    # print('speed_each_class: ', speed_each_class)
    # print('speed_each_values: ', speed_each_values)
    # print('speed_excel: ', speed_excel)

    speed_excel = pd.DataFrame(speed_excel)
    # print(speed_excel)
    speed_excel = speed_excel.sort_values('Time in')
    speed_excel.to_excel(f'static/users/{user}/{projectID}/speed.xlsx', index=False)
    # print(speed_excel)
    return speed_class_infor, speed_each_values


def caculate_speed_v3(user, projectID, model, time_start_str, time_end_str, FPS, num_class=5):
    f = open(f"static/users/{user}/{projectID}/speed.json", 'r')

    if len(time_start_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_start = convert_string_to_datetime(time_start_str, date_format)
    if len(time_end_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_end = convert_string_to_datetime(time_end_str, date_format)

    data = json.load(f)

    line0 = data['0']
    line1 = data['1']

    common_item = find_common_elements(list(line0.keys()), list(line1.keys()))

    all_speed = {}
    speed_each_class = {}
    speed_each_values = {
        '<40': {},
        '40~60': {},
        '60~80': {},
        '80~120': {},
        '>120': {}
    }
    speed_excel = {
        'Time range': [],
        'ID': [],
        'Class': [],
        'Time in': [],
        'Time out': [],
        'Travel time (s)': [],
        'Speed (km/h)': [],
        'Distance (m)': []
    }
    for item in common_item:
        # print(line0[item])
        # thoi gian khi cat line 0 (frame) va toa do khi do
        t1 = line0[item][1]     # frame vao
        d1 = line0[item][-1]    # toa do khi do

        # thoi gian khi cat line 1 (frame) va toa do khi do
        t2 = line1[item][1]
        d2 = line1[item][-1]

        # tinh thoi gian di chuyen
        time_frame = abs(t1 - t2) # don vi: frame
        time_sec = round(time_frame / FPS, 3) #don vi: sec

        # tinh khoang cach di chuyen
        new_locate = [[d1[0], d1[1], d2[0], d2[1]]]
        distance_in_m = predict_distance(model=model, new_locate=new_locate)
        distance_in_m = abs(distance_in_m)
        # distance_frame = calculate_distance(d1[0], d1[1], d2[0], d2[1]) # don vi: pixel
        # distance_in_m = distance_frame / distance_in_pixel * distance_in_meter # don vi: m

        # tinh toc do
        if not   time_sec:
            pass
        else:
            speed = round(distance_in_m / time_sec * 3.6, 1) # m/s -> km/h
            all_speed[item] = speed
            cls = str(line0[item][0])

            # tao dict chua thong tin ve speed cua tung class
            if cls in speed_each_class:
                speed_each_class[cls].append(speed)
            else:
                speed_each_class[cls] = []
                speed_each_class[cls].append(speed)

            # Tao dict chua thong tin ve speed theo tung khoang chia
            if speed < 40:
                if cls not in speed_each_values['<40']:
                    speed_each_values['<40'][cls] = 0
                speed_each_values['<40'][cls] += 1
            elif speed>=40 and speed<60 :
                if cls not in speed_each_values['40~60']:
                    speed_each_values['40~60'][cls] = 0
                speed_each_values['40~60'][cls] += 1
            elif speed>=60 and speed<80 :
                if cls not in speed_each_values['60~80']:
                    speed_each_values['60~80'][cls] = 0
                speed_each_values['60~80'][cls] += 1
            elif speed>=80 and speed<=120 :
                if cls not in speed_each_values['80~120']:
                    speed_each_values['80~120'][cls] = 0
                speed_each_values['80~120'][cls] += 1
            elif speed>120 :
                if cls not in speed_each_values['>120']:
                    speed_each_values['>120'][cls] = 0
                speed_each_values['>120'][cls] += 1

        # Tao dict chua thong tin de xuat file excel
        speed_excel['Time range'].append("01:00")
        speed_excel['ID'].append(item)
        speed_excel['Class'].append(list_vehicle[int(cls)])
        if t1 < t2:
            sec_in, sec_out = convert_frame_to_sec(t1, FPS), convert_frame_to_sec(t2, FPS)
            time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                     sec_out)
        else:
            sec_in, sec_out = convert_frame_to_sec(t2, FPS), convert_frame_to_sec(t1, FPS)
            time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                     sec_out)
        speed_excel['Time in'].append(str(time_in))
        speed_excel['Time out'].append(str(time_out))
        speed_excel['Travel time (s)'].append(time_sec)
        speed_excel['Speed (km/h)'].append(speed)
        speed_excel['Distance (m)'].append(round(distance_in_m, 3))

    speed_class_infor = {}
    for i in range (num_class):
        i = str(i)
        if i not in speed_each_class:
            speed_class_infor[i] = {
                'amount': 0,
                'medium': 0,
                'max': 0,
                'min': 0
            }
        else:
            speed_class_infor[i] = {
                'amount': len(speed_each_class[i]),
                'medium': round(calculate_average(speed_each_class[i]), 1),
                'max': max(speed_each_class[i]),
                'min': min(speed_each_class[i])
            }

        for key in speed_each_values:
            if i not in speed_each_values[key]:
                speed_each_values[key][i] = 0
    # print('speed_class_infor: ', speed_class_infor)
    # print('speed_each_class: ', speed_each_class)
    # print('speed_each_values: ', speed_each_values)
    # print('speed_excel: ', speed_excel)

    speed_excel = pd.DataFrame(speed_excel)
    # print(speed_excel)
    speed_excel = speed_excel.sort_values('Time in')
    speed_excel.to_excel(f'static/users/{user}/{projectID}/speed.xlsx', index=False)
    # print(speed_excel)
    return speed_class_infor, speed_each_values

def check_median(D,dis_fall):
  mda=statistics.median(D)
  if mda <= 0:
      mda = 4
  if mda > 0:
      lower_m = mda/2
      higher_m = mda*1.5
      if dis_fall < lower_m:
          dis_fall = lower_m
      if dis_fall > higher_m:
          dis_fall = higher_m
  return dis_fall

def caculate_speed_v3_MEDIAN(user, projectID, model, time_start_str, time_end_str, FPS, start_range, end_range,time_step, num_class=5):


    f = open(f"static/users/{user}/{projectID}/speed.json", 'r')

    if len(time_start_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_start = convert_string_to_datetime(time_start_str, date_format)
    if len(time_end_str)<17:
        date_format="%Y-%m-%dT%H:%M"
    else:
        date_format = "%Y-%m-%dT%H:%M:%S"
    time_end = convert_string_to_datetime(time_end_str, date_format)

    if not start_range:
        start_range = time_start_str
    if not end_range:
        end_range = time_end_str
    time_space_start = (convert_string_to_datetime(start_range, date_format) - time_start)
    print("time_space_start FRAME: ",int(time_space_start.total_seconds() * FPS))
    time_space_end = (convert_string_to_datetime(end_range, date_format) - time_start)
    print("time_space_end FRAME", int(time_space_end.total_seconds() * FPS))

    total_frames = int(time_space_end.total_seconds() * FPS) - int(time_space_start.total_seconds() * FPS) + 1

    # Calculate the number of blocks
    num_blocks = total_frames // (int(time_step) * FPS * 60)
    frame_blocks = []

    # Calculate frame ranges for each block
    for block_index in range(num_blocks):
        block_start_frame = int(time_space_start.total_seconds() * FPS) + block_index * int(time_step) * FPS * 60
        block_end_frame = block_start_frame + int(time_step) * FPS * 60 - 1
        frame_blocks.append((block_start_frame, block_end_frame))

    data = json.load(f)

    line0 = data['0']
    line1 = data['1']

    common_item = find_common_elements(list(line0.keys()), list(line1.keys()))

    all_speed = {}
    speed_each_class = {}

    speed_each_values = {
        '<40': {},
        '40~60': {},
        '60~80': {},
        '80~120': {},
        '>120': {}
    }
    speed_excel = {
        'Time range': [],
        'ID': [],
        'Class': [],
        'Time in': [],
        'Time out': [],
        'Travel time (s)': [],
        'Speed (km/h)': [],
        'Distance (m)': []
    }
    all_Distance = []
    for item in common_item:
        # toa do khi cat line 0 (frame)
        d1 = line0[item][-1]    # toa do khi do

        # toa do khi cat line 1 (frame)
        d2 = line1[item][-1]

        new_locate = [[d1[0], d1[1], d2[0], d2[1]]]
        distance_in_m = predict_distance(model=model, new_locate=new_locate)
        all_Distance.append(distance_in_m)

    check_time_have = 0
    for item in common_item:
        # print(line0[item])
        # thoi gian khi cat line 0 (frame) va toa do khi do
        t1 = line0[item][1]  # frame vao
        d1 = line0[item][-1]  # toa do khi do

        # thoi gian khi cat line 1 (frame) va toa do khi do
        t2 = line1[item][1]
        d2 = line1[item][-1]

        # tinh thoi gian di chuyen
        time_frame = abs(t1 - t2)  # don vi: frame
        time_sec = round(time_frame / FPS, 3)  # don vi: sec

        # tinh khoang cach di chuyen
        new_locate = [[d1[0], d1[1], d2[0], d2[1]]]
        distance_in_m = predict_distance(model=model, new_locate=new_locate)
        distance_in_m = check_median(all_Distance,distance_in_m)
        # distance_frame = calculate_distance(d1[0], d1[1], d2[0], d2[1]) # don vi: pixel
        # distance_in_m = distance_frame / distance_in_pixel * distance_in_meter # don vi: m
        for block in frame_blocks:
            if block[0] <= t1 <= block[1]:
        # tinh toc do
                if not time_sec:
                    pass
                else:
                    speed = round(distance_in_m / time_sec * 3.6, 1)  # m/s -> km/h
                    all_speed[item] = speed
                    cls = str(line0[item][0])

                    # tao dict chua thong tin ve speed cua tung class
                    if cls in speed_each_class:
                        speed_each_class[cls].append(speed)
                    else:
                        speed_each_class[cls] = []
                        speed_each_class[cls].append(speed)

                    # Tao dict chua thong tin ve speed theo tung khoang chia
                    if speed < 40:
                        if cls not in speed_each_values['<40']:
                            speed_each_values['<40'][cls] = 0
                        speed_each_values['<40'][cls] += 1
                    elif speed >= 40 and speed < 60:
                        if cls not in speed_each_values['40~60']:
                            speed_each_values['40~60'][cls] = 0
                        speed_each_values['40~60'][cls] += 1
                    elif speed >= 60 and speed < 80:
                        if cls not in speed_each_values['60~80']:
                            speed_each_values['60~80'][cls] = 0
                        speed_each_values['60~80'][cls] += 1
                    elif speed >= 80 and speed <= 120:
                        if cls not in speed_each_values['80~120']:
                            speed_each_values['80~120'][cls] = 0
                        speed_each_values['80~120'][cls] += 1
                    elif speed > 120:
                        if cls not in speed_each_values['>120']:
                            speed_each_values['>120'][cls] = 0
                        speed_each_values['>120'][cls] += 1

                # Tao dict chua thong tin de xuat file excel

                speed_excel['Time range'].append(f'{add_seconds_to_datetime(time_start,convert_frame_to_sec(block[0], FPS))[:-4]} - {add_seconds_to_datetime(time_start,convert_frame_to_sec(block[1], FPS))[:-4]}')
                speed_excel['ID'].append(item)
                speed_excel['Class'].append(list_vehicle[int(cls)])
                if t1 < t2:
                    sec_in, sec_out = convert_frame_to_sec(t1, FPS), convert_frame_to_sec(t2, FPS)
                    time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                             sec_out)
                else:
                    sec_in, sec_out = convert_frame_to_sec(t2, FPS), convert_frame_to_sec(t1, FPS)
                    time_in, time_out = add_seconds_to_datetime(time_start, sec_in), add_seconds_to_datetime(time_start,
                                                                                                             sec_out)
                speed_excel['Time in'].append(str(time_in[:-4]))
                speed_excel['Time out'].append(str(time_out[:-4]))
                speed_excel['Travel time (s)'].append(time_sec)
                speed_excel['Speed (km/h)'].append(speed)
                speed_excel['Distance (m)'].append(round(distance_in_m, 3))
    # check_time_have = 0
    speed_class_infor = {}
    for i in range (num_class):
        i = str(i)
        if i not in speed_each_class:
            speed_class_infor[i] = {
                'amount': 0,
                'medium': 0,
                'max': 0,
                'min': 0
            }
        else:
            speed_class_infor[i] = {
                'amount': len(speed_each_class[i]),
                'medium': round(calculate_average(speed_each_class[i]), 1),
                'max': max(speed_each_class[i]),
                'min': min(speed_each_class[i])
            }

        for key in speed_each_values:
            if i not in speed_each_values[key]:
                speed_each_values[key][i] = 0
    # print('speed_class_infor: ', speed_class_infor)
    # print('speed_each_class: ', speed_each_class)
    # print('speed_each_values: ', speed_each_values)
    # print('speed_excel: ', speed_excel)

    speed_excel = pd.DataFrame(speed_excel)
    # print(speed_excel)
    speed_excel = speed_excel.sort_values('Time in')
    speed_excel['Time range']= speed_excel['Time range'].mask(speed_excel['Time range'].eq(speed_excel['Time range'].shift(1)))


    speed_excel.to_excel(f'static/users/{user}/{projectID}/speed.xlsx', index=False)
    # print(speed_excel)
    return speed_class_infor, speed_each_values

# caculate_speed(user='test2', projectID='cv8zg', distance_in_meter=100, distance_in_pixel=100)
# now = datetime.now()
# sec = 5.637
# print(add_seconds_to_datetime(now, sec))
