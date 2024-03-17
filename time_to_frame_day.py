from datetime import datetime,timedelta
import math

# kiểm tra thời gian trong khoảng [a,b] có nằm trong khoảng [c,d] không.
def check_time_range(a, b, c, d):
    time1 = datetime.fromisoformat(c)# thời gian bắt đầu của video đầu tiên
    time2 = datetime.fromisoformat(d)# thời gian kết thúc của video cuối cùng
    time3 = datetime.fromisoformat(a)# thời gian nhập tay start
    time4 = datetime.fromisoformat(b)# thời gian nhập tay end

    # Kiểm tra điều kiện
    if time1 <= time3 <= time2 and time1 <= time4 <= time2:
        return True
    else:
        return False

#trả về số giây, frame tính từ video đầu tiên đến thời gian bắt đầu mong muốn
def time_diff_frames(a, c):
    # time1 = datetime.fromisoformat(a)
    # time2 = datetime.fromisoformat(c)
    time1=a
    time2=c

    # Tính hiệu của hai đối tượng datetime
    duration = time2 - time1

    # Trả về số giây giữa hai khoảng thời gian
    seconds = duration.total_seconds()
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

    time1 = datetime.fromisoformat(start)
    time2 = datetime.fromisoformat(end)

    # Tính hiệu của hai đối tượng datetime
    duration = time2 - time1

    # Trả về số giây giữa hai khoảng thời gian
    totalMins = duration.total_seconds()//60

    num_block = int(totalMins / block)
    remain = totalMins % block

    for i in range (num_block):
        t1, t2 = addTime(time1, block)
        time_lap.append([t1, t2])
        time1 = t2

    if remain:
        t1, t2 = addTime(time1, remain)
        time_lap.append([t1, t2])

    return time_lap

def addTime(time_, addTime):
    '''
    :param time_: time before add mins
    :param mins: minutes added
    :return: time before added, time after added
    '''
    time_+timedelta(minutes=addTime)
    # hours = int(time_.hour)
    # mins = int(time_.minute)
    #
    # mins += addTime
    # hours += int(mins / 60)
    # mins = mins % 60

    return time_, time_+timedelta(minutes=addTime)

def frame_start_frame_end(a,b,c):
    '''

    Args:
        a: thời gian nhap tay start a '10:30'
        b: thời gian nhap tay end b  '11:45'
        c: thời gian bắt đầu của video(video đầu tiên)

    Returns: 'bắt đầu tại frame thứ', 'kết thúc tại frame thứ'

    '''
    s_start,frame_start = time_diff_frames(a, c)
    s_end, frame_end = time_diff_frames(a, b)
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
    start_vid=datetime.fromisoformat(start_vid)
    list_block = sepheraBlock(start, end, block)

    for frame_block in list_block:
        frame_start, frame_end = frame_start_frame_end(frame_block[0], frame_block[1],start_vid)
        list_all_frame_block.append([frame_start, frame_end])

    return list_block, list_all_frame_block

# a ='6:57:56'
# b = '7:00'
# c = '7:05'
#
# abc, abcd = convert_time_lap_to_frame(a, b, c, 2)
# print('abc: ', abc)
# print('abcd: ', abcd)

time_str1 = "2023-06-23T23:03:15"
time_str2 = "2023-06-26T22:05:51"

# Chuyển chuỗi thời gian thành đối tượng datetime
time1 = datetime.fromisoformat(time_str1)
time2 = datetime.fromisoformat(time_str2)

# Tính khoảng thời gian giữa hai thời điểm
duration = time2 - time1

time_str1 = "2023-06-23T23:03:15"
time_str2 = "2023-06-26T22:05:51"
time_str3 = "2023-06-23T23:30"
time_str4 = "2023-06-26T22:00"

# Chuyển chuỗi thời gian thành đối tượng datetime
time1 = datetime.fromisoformat(time_str1)
time2 = datetime.fromisoformat(time_str2)
time3 = datetime.fromisoformat(time_str3)
time4 = datetime.fromisoformat(time_str4)

# Kiểm tra điều kiện
if time1 <= time3 <= time2 and time1 <= time4 <= time2:
    print("time1 và time2 nằm trong khoảng từ time3 đến time4")
else:
    print("time1 và time2 không nằm trong khoảng từ time3 đến time4")