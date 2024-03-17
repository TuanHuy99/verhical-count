import os
from flask import send_file
import cv2
import json
from utils import *
from APIs.truy_van import get_project_name
def find_video_path(video_name,user,classes):
    # starting directory
    root_dir = "static/users/"+user+"/"+video_name+"/"+classes+"_class"+"/"
    print("root_dir: ",root_dir)

    # loop through all subdirectories, starting from the bottom
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        print(dirpath, dirnames, filenames)
        # loop through all files in the current directory
        if dirpath[-5:]=='track':
            for filename in filenames:
                # check if the filename matches the given video name
                if filename[-4:] == ".mp4" and dirnames==[]:
                    # print("vo day nay")
                    # return the full path to the video file
                    # print(os.path.join(dirpath, filename).replace("\\","/"))
                    return os.path.join(dirpath, filename).replace("\\","/")
                if filename[-4:] == ".avi" and dirnames==[]:
                    # print("vo day nay")
                    # return the full path to the video file
                    # print(os.path.join(dirpath, filename).replace("\\","/"))
                    return os.path.join(dirpath, filename).replace("\\","/")

    # if the video is not found, return None
    return None
def gen_video_count(project,user,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,name_video,classes):

    link_video_up=find_video_path(project,user,classes)
    namevideo=get_project_name(project)

    vid = cv2.VideoCapture(link_video_up)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    path_vd_speed = f'static/users/{user}/{project}/video_count_4lines'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{user}/{project}/video_count_4lines/count5classes.mp4'
    print(link_out_video)
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)
    count = 0
    list_veco=[0] * 9

    f = open(f'static/users/{user}/{project}/data_idlinetoline_d.json')
    data = json.load(f)


    d1, d2, d3, d4 = direct_detector(f'static/users/{user}/{project}',user)

    def sum_(d):
        sumd = 0
        for a in d:
            sumd += a
        return sumd

    idline = [sum_(d1), sum_(d2), sum_(d3), sum_(d4)]
    while (vid.isOpened()):

        ret, frame = vid.read()
        if ret:
            count += 1
            for i in data[str(idline.index(max(idline)))].keys():
                if data[str(idline.index(max(idline)))][i][1] == count:
                    list_veco[data[str(idline.index(max(idline)))][i][0]] += 1
        else:
            break

        toadoxy=[[x,y,x1,y1],[x2,y2,x3,y3],[x4,y4,x5,y5],[x6,y6,x7,y7]]
        cv2.line(frame, (int(toadoxy[idline.index(max(idline))][0]), int(toadoxy[idline.index(max(idline))][1])), (int(toadoxy[idline.index(max(idline))][2]), int(toadoxy[idline.index(max(idline))][3])), (255, 253, 0), 4)



        font_color = (0, 0, 255)
        font_size = 0.8
        font_thickness = 2
        # cv2.putText(frame, "Motor  Bicycle    Car      Taxi     Coach    Bus      LGV     HGV      VHGV", (110, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, "Line ", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        # cv2.putText(frame, str(list_veco[0]), (115, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[1]), (235, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[2]), (355, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[3]), (475, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[4]), (595, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[5]), (715, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[6]), (835, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[7]), (955, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[8]), (1075, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        cv2.putText(frame, "Cars     LGVs     HGVs     MCs     Buses", (140, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                    font_color, font_thickness)
        cv2.putText(frame, "Direction", (16, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        cv2.putText(frame, str(list_veco[2]+list_veco[3]), (145, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco[6]), (265, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco[7]+list_veco[8]), (385, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco[0]+list_veco[1]), (505, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco[4]+list_veco[5]), (625, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)

        cv2.putText(frame, "Total", (760, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)

        # cv2.putText(frame, "Total", (1215, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        # cv2.putText(frame, ""+str(list_veco[0]+list_veco[1]+list_veco[2]+list_veco[3]+list_veco[4]+list_veco[5]+list_veco[6]+list_veco[7]+list_veco[8]), (1215, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        # #
        # cv2.putText(frame, "Line2", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        # cv2.putText(frame, str(list_veco[1]), (115, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[3]), (235, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[4]), (355, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[0]), (475, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[2]), (595, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        cv2.putText(frame, "" + str(list_veco[0] + list_veco[1] + list_veco[2] + list_veco[3] + list_veco[4]), (760, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        cv2.putText(frame, "Line", (int(toadoxy[idline.index(max(idline))][0]), int(toadoxy[idline.index(max(idline))][1])), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        percent_process = count / total_frame * 100
        percent_process = int(round(percent_process))

        yield "data: {}\n\n".format(percent_process)
        out.write(frame)
    # file_path = f"static/users/{user}/{project}/out_" + name_video + ".mp4"
    # return send_file(file_path, as_attachment=True)

# gen_video_count('20230330_110000_054_r.mp4',x=595.888888835907,y=457.66668701171875,x1=995.888888835907,y1=558.6666870117188,x2=481.888888835907,y2=502.66668701171875,x3=971.888888835907,y3=641.6666870117188,x4=393.888888835907,y4=528.6666870117188,x5=959.888888835907,y5=739.6666870117188,x6=349.888888835907,y6=549.6666870117188,x7=930.888888835907,y7=834.6666870117188)

def gen_video_count_9class(project,user,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,name_video,classes):

    link_video_up=find_video_path(project,user,classes)
    namevideo=get_project_name(project)

    vid = cv2.VideoCapture(link_video_up)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    path_vd_speed = f'static/users/{user}/{project}/video_count_4lines'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{user}/{project}/video_count_4lines/count9classes.mp4'
    print(link_out_video)
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)
    count = 0
    list_veco=[0] * 9

    f = open(f'static/users/{user}/{project}/data_idlinetoline_d.json')
    data = json.load(f)


    d1, d2, d3, d4 = direct_detector(f'static/users/{user}/{project}',user)

    def sum_(d):
        sumd = 0
        for a in d:
            sumd += a
        return sumd

    idline = [sum_(d1), sum_(d2), sum_(d3), sum_(d4)]
    while (vid.isOpened()):

        ret, frame = vid.read()
        if ret:
            count += 1
            for i in data[str(idline.index(max(idline)))].keys():
                if data[str(idline.index(max(idline)))][i][1] == count:
                    list_veco[data[str(idline.index(max(idline)))][i][0]] += 1
        else:
            break

        toadoxy=[[x,y,x1,y1],[x2,y2,x3,y3],[x4,y4,x5,y5],[x6,y6,x7,y7]]
        cv2.line(frame, (int(toadoxy[idline.index(max(idline))][0]), int(toadoxy[idline.index(max(idline))][1])), (int(toadoxy[idline.index(max(idline))][2]), int(toadoxy[idline.index(max(idline))][3])), (255, 253, 0), 4)



        font_color = (0, 0, 255)
        font_size = 0.8
        font_thickness = 2
        cv2.putText(frame, "Motor  Bicycle    Car      Taxi     Coach    Bus      LGV     HGV      VHGV", (140, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, "Line ", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        cv2.putText(frame, str(list_veco[0]), (145, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[1]), (275, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[2]), (385, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[3]), (505, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[4]), (625, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[5]), (745, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[6]), (865, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[7]), (985, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[8]), (1105, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        # cv2.putText(frame, "Cars     LGVs     HGVs     MCs     Buses", (140, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size,
        #             font_color, font_thickness)
        cv2.putText(frame, "Direction", (16, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        # cv2.putText(frame, str(list_veco[2]+list_veco[3]), (145, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
        #             font_thickness)
        # cv2.putText(frame, str(list_veco[6]), (265, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
        #             font_thickness)
        # cv2.putText(frame, str(list_veco[7]+list_veco[8]), (385, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
        #             font_thickness)
        # cv2.putText(frame, str(list_veco[0]+list_veco[1]), (505, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
        #             font_thickness)
        # cv2.putText(frame, str(list_veco[4]+list_veco[5]), (625, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
        #             font_thickness)
        #
        # cv2.putText(frame, "Total", (760, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)

        cv2.putText(frame, "Total", (1245, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        cv2.putText(frame, ""+str(list_veco[0]+list_veco[1]+list_veco[2]+list_veco[3]+list_veco[4]+list_veco[5]+list_veco[6]+list_veco[7]+list_veco[8]), (1245, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        # #
        # cv2.putText(frame, "Line2", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        # cv2.putText(frame, str(list_veco[1]), (115, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[3]), (235, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[4]), (355, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[0]), (475, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        # cv2.putText(frame, str(list_veco[2]), (595, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        # cv2.putText(frame, "" + str(list_veco[0] + list_veco[1] + list_veco[2] + list_veco[3] + list_veco[4]), (760, 60),
        #             cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        cv2.putText(frame, "Line", (int(toadoxy[idline.index(max(idline))][0]), int(toadoxy[idline.index(max(idline))][1])), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        percent_process = count / total_frame * 100
        percent_process = int(round(percent_process))

        yield "data: {}\n\n".format(percent_process)
        out.write(frame)