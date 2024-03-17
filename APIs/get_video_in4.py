import glob, os
import cv2
import datetime

# create video capture object
def get_video_information(video_path):
    '''

    '''
    data = cv2.VideoCapture(video_path)

    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    data.release()

    return fps, int(frames)

######################################################################
def bytes_to_gb(bytes):
    gb = bytes / (1024.0**3)
    return round(gb, 3)

######################################################################
def get_folder_information(dir_path):
    '''

    '''
    # get number of video in folder
    num_video = len(glob.glob(f'{dir_path}/*.mp4'))

    size = 0
    # get size
    for ele in os.scandir(dir_path):
        size += os.path.getsize(ele)

    size = bytes_to_gb(size)
    return size, num_video

######################################################################
def get_create_time(path):
    '''

    '''
    # file creation
    c_timestamp = os.path.getctime(path)

    # convert creation timestamp into DateTime object
    c_datestamp = datetime.datetime.fromtimestamp(c_timestamp)
    time_obj = datetime.datetime.strptime(str(c_datestamp), "%Y-%m-%d %H:%M:%S.%f")
    rounded_time_str = time_obj.strftime("%Y-%m-%d %H:%M:%S")

    return rounded_time_str

######################################################################