from datetime import datetime
import math

# kiểm tra thời gian trong khoảng [a,b] có nằm trong khoảng [c,d] không.
def check_time_range(a, b, c, d):
    a = datetime.strptime(a, '%H:%M') # thời gian nhập tay start
    b = datetime.strptime(b, '%H:%M') # thời gian nhập tay end
    c = datetime.strptime(c, '%H:%M:%S') # thời gian bắt đầu của video đầu tiên
    d = datetime.strptime(d, '%H:%M:%S') # thời gian kết thúc của video cuối cùng
    if c <= a <= d and c <= b <= d:
        return True
    else:
        return False

#trả về số giây, frame tính từ video đầu tiên đến thời gian bắt đầu mong muốn
def time_diff_frames(a, c):
    a_time = datetime.strptime(a, '%H:%M') # thời gian nhập tay start
    c_time = datetime.strptime(c, '%H:%M:%S') # thời gian bắt đầu của video đầu tiên

    # Tính khoảng cách giữa a và c
    time_diff = (c_time - a_time)

    # Tính số giây và số frame tương ứng
    seconds = math.fabs(time_diff.total_seconds())
    frames = math.fabs(int(seconds * 30))

    return seconds, frames

def sepheraBlock(start, end, block=0):
    '''
    :param start: time start counting verhical
    :param end: time end counting
    :param block: period time
    :return: list of block time
    '''
    time_lap = []

    starts = start.split(":")
    ends = end.split(":")

    totalMins = (int(ends[0]) - int(starts[0])) *60 - int(starts[1]) + int(ends[1])

    num_block = int(totalMins / block)
    remain = totalMins % block

    for i in range (num_block):
        t1, t2 = addTime(start, block)
        time_lap.append([t1, t2])
        start = t2

    if remain:
        t1, t2 = addTime(start, remain)
        time_lap.append([t1, t2])

    return time_lap

def addTime(time_, addTime):
    '''
    :param time_: time before add mins
    :param mins: minutes added
    :return: time before added, time after added
    '''
    time_ = time_.split(':')
    hours = int(time_[0])
    mins = int(time_[1])

    mins += addTime
    hours += int(mins / 60)
    mins = mins % 60

    return f'{time_[0]}:{time_[1]}', f'{hours}:{mins}'

def frame_start_frame_end(a,b,c):
    '''

    Args:
        a: thời gian nhap tay start a '10:30'
        b: thời gian nhap tay end b  '11:45'
        c: thời gian bắt đầu của video(video đầu tiên)

    Returns: 'bắt đầu tại frame thứ', 'kết thúc tại frame thứ'

    '''
    s_start,frame_start = time_diff_frames(a, c)
    s_end, frame_end = time_diff_frames(a, b+':00')
    return int(frame_start), int(frame_end+frame_start)

def convert_time_lap_to_frame(start_vid, start, end, block):
    '''
    :param start_vid: time of start video
    :param start: time start counting
    :param end: time stop counting
    :param block: time of each block (minutes)
    :return: [start frame, end frame] of each block
    '''
    list_all_frame_block = []

    list_block = sepheraBlock(start, end, block)

    for frame_block in list_block:
        frame_start, frame_end = frame_start_frame_end(frame_block[0], frame_block[1],start_vid)
        list_all_frame_block.append([frame_start, frame_end])

    return list_block, list_all_frame_block

a ='6:57:56'
b = '7:00'
c = '7:05'

abc, abcd = convert_time_lap_to_frame(a, b, c, 2)
print('abc: ', abc)
print('abcd: ', abcd)
# import os

# dir_path = "D:/test_3hour/test"
# videos = os.listdir(dir_path)
#
# print(videos)
#
# videos.sort()
# print(videos)
