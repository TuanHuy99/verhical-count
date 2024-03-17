import json
import cv2
import os

import pandas as pd

from utils import direct_detector_2short
from view_count_invideo import find_video_path

def gen_video_speed(name_user,dir_video,classes):
    link_json_point= f'static/users/{name_user}/{dir_video}/data_point_5.json'
    f = open(link_json_point)
    data = json.load(f)
    link_video_up = find_video_path(dir_video,name_user,classes)
    print(link_video_up)
    #####
    # link_video_up=f"static/users/{name_user}/{dir_video}/track/1s.mp4"
    vid = cv2.VideoCapture(link_video_up)
    count=0
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    path_vd_speed=f'static/users/{name_user}/{dir_video}/video_speed'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{name_user}/{dir_video}/video_speed/speed.mp4'
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)

    # color=[(255,0,0), (0,255,0), (0,0,255), (255,0,255), (0,255,255)]
    color=[(255,225,0), (255,225,0), (255,225,0), (255,225,0), (255,225,0),(255,225,0),(255,225,0),(255,225,0),(255,225,0)]
    color=[(56, 56, 255), (151, 157, 255), (31,112,255), (29, 178, 255), (49,210,207)]
    classes=['motor','car','bus','lgv','hgv']

    # read xlsx
    df_excel=pd.read_excel(f'static/users/{name_user}/{dir_video}/speed.xlsx')
    speed_by_id = df_excel.set_index("ID")["Speed (km/h)"]

    while (vid.isOpened()):

        ret, frame = vid.read()
        if ret:
            count += 1
        else:
            break

        for id in list(data.keys()):
            for id_vehicle, speed in speed_by_id.items():
                if int(id) == int(id_vehicle):
                    for i in range(len(data[id]["cls"])):
                        x, y, f = data[id]["frame"][i][:3]
                        if f==count:
                            # print(int(data[id]["cls"][i]))
                            font_color = color[int(data[id]["cls"][i])]
                            # font_color = (255,0,0)
                            font_size = 0.8
                            font_thickness = 2
                            # cv2.rectangle(frame, (x-10, y-15), (x + 80, y + 10), (125, 125, 125), -1)
                            cv2.putText(frame, classes[int(data[id]["cls"][i])]+":"+str(speed)+" km/h", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                            # cv2.putText(frame, str(speed)+" km/h", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                            break

                else:
                    for i in range(len(data[id]["cls"])):
                        x, y, f = data[id]["frame"][i][:3]
                        if f==count:
                            # print(int(data[id]["cls"][i]))
                            font_color = color[int(data[id]["cls"][i])]
                            # font_color = (255,0,0)
                            font_size = 0.8
                            font_thickness = 2
                            # cv2.rectangle(frame, (x-10, y-15), (x + 80, y + 10), (125, 125, 125), -1)
                            cv2.putText(frame, classes[int(data[id]["cls"][i])]+"", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                            # cv2.putText(frame, str(speed)+" km/h", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                            break

        print(count)
        out.write(frame)


def gen_video_speed_test(name_user,dir_video,x0,y0,x1,y1,x2,y2,x3,y3,classes):
    link_json_point= f'static/users/{name_user}/{dir_video}/data_point_5.json'
    f = open(link_json_point)
    data = json.load(f)
    link_video_up = find_video_path(dir_video,name_user,classes)
    print(link_video_up)
    #####
    # link_video_up=f"static/users/{name_user}/{dir_video}/track/1s.mp4"
    vid = cv2.VideoCapture(link_video_up)
    total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    count=0
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    path_vd_speed=f'static/users/{name_user}/{dir_video}/video_speed'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{name_user}/{dir_video}/video_speed/speed.mp4'
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)

    # color=[(255,0,0), (0,255,0), (0,0,255), (255,0,255), (0,255,255)]
    color=[(255,225,0), (255,225,0), (255,225,0), (255,225,0), (255,225,0),(255,225,0),(255,225,0),(255,225,0),(255,225,0)]
    color=[(56, 56, 255), (151, 157, 255), (31,112,255), (29, 178, 255), (49,210,207)]
    classes=['motor','car','bus','lgv','hgv']

    # read xlsx
    df_excel=pd.read_excel(f'static/users/{name_user}/{dir_video}/speed.xlsx')
    speed_by_id = df_excel.set_index("ID")["Speed (km/h)"]
    print(speed_by_id.index)
    link_json_speed = f'static/users/{name_user}/{dir_video}/speed.json'
    sp = open(link_json_speed)
    data_speed = json.load(sp)
    while (vid.isOpened()):

        ret, frame = vid.read()
        if ret:
            count += 1
        else:
            break
        font_color = (0, 0, 255)
        font_size = 0.8
        font_thickness = 3
        cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), (255, 253, 0), 4)
        cv2.line(frame, (int(x2), int(y2)), (int(x3), int(y3)), (255, 253, 0), 4)
        cv2.putText(frame, "Line1", (int(x0), int(y0)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, "Line2", (int(x3), int(y3)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        for id in list(data.keys()):
            # for id_vehicle, speed in speed_by_id.items():
            # if int(id) == int(id_vehicle):
            if int(id) in speed_by_id.index:
                for i in range(len(data[id]["cls"])):
                    x, y, f = data[id]["frame"][i][:3]
                    if f==count and min(data_speed["0"][id][1],data_speed["1"][id][1]) <= f <= max(data_speed["0"][id][1],data_speed["1"][id][1]):
                        # print(int(data[id]["cls"][i]))
                        font_color = color[int(data[id]["cls"][i])]
                        # font_color = (255,0,0)
                        font_size = 0.8
                        font_thickness = 2
                        # cv2.rectangle(frame, (x-10, y-15), (x + 80, y + 10), (125, 125, 125), -1)
                        # cv2.putText(frame, classes[int(data[id]["cls"][i])]+":"+str(speed_by_id[int(id)])+" km/h", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                        cv2.putText(frame, str(speed_by_id[int(id)])+" km/h", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                        break
                    elif f>count:
                        break
            # else:
            #     break
                # for i in range(len(data[id]["cls"])):
                #     x, y, f = data[id]["frame"][i][:3]
                #     if f==count:
                #         # print(int(data[id]["cls"][i]))
                #         font_color = color[int(data[id]["cls"][i])]
                #         # font_color = (255,0,0)
                #         font_size = 0.8
                #         font_thickness = 2
                #         # cv2.rectangle(frame, (x-10, y-15), (x + 80, y + 10), (125, 125, 125), -1)
                #         cv2.putText(frame, classes[int(data[id]["cls"][i])]+"", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                #         # cv2.putText(frame, str(speed)+" km/h", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                #         break
                #     elif f>count:
                #         break

        percent_process = count / total_frame * 100
        percent_process = int(round(percent_process))

        yield "data: {}\n\n".format(percent_process)
        out.write(frame)
# gen_video_speed_test('test3','w8y50')

def gen_video_2lines(user,name_dir,x0,y0, x1,y1,x2,y2,x3,y3,classes):

    name_vi_dir = f'static/users/{user}/{name_dir}/{classes}_class/track/'
    name_vi = os.listdir(name_vi_dir)[0]
    link_video_up = name_vi_dir+name_vi
    print(link_video_up)
    vid = cv2.VideoCapture(link_video_up)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    name_vi = name_vi.replace(".", "_")
    path_vd_speed = f'static/users/{user}/{name_dir}/video_speed'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{user}/{name_dir}/video_speed/2short.mp4'
    print(link_out_video)
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)
    count = 0
    list_veco=[0] * 5
    f = open(f'static/users/{user}/{name_dir}/data_idlinetoline_d_hour.json')
    data = json.load(f)

    f_rs = open(f'static/users/{user}/{name_dir}/result.json')
    data_rs = json.load(f_rs)
    def sum_(d):
        sumd = 0
        for a in d:
            sumd += a
        return sumd

    list_veco01=[0]*5
    list_veco10=[0]*5

    while (vid.isOpened()):

        ret, frame = vid.read()
        if ret:
            count += 1
            a = ['0', '1', '2', '3', '4']
            for k in a:
                for i in data_rs['0'][k]:
                    if i in data['0'].keys() and data['0'][i][1] == count:
                        list_veco01[int(k)] += 1
                for i in data_rs['1'][k]:
                    if i in data['1'].keys() and data['1'][i][1] == count:
                        list_veco10[int(k)] += 1
        else:
            break


        cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), (255, 253, 0), 4)
        cv2.line(frame, (int(x2), int(y2)), (int(x3), int(y3)), (255, 253, 0), 4)



        font_color = (0, 0, 255)
        font_size = 0.8
        font_thickness = 2
        cv2.putText(frame, "Cars     LGVs     HGVs     MCs     Buses", (140, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, "Direct1_2", (16, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        cv2.putText(frame, str(list_veco01[1]), (145, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco01[3]), (265, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco01[4]), (385, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco01[0]), (505, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco01[2]), (625, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        cv2.putText(frame, "Total", (760, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        cv2.putText(frame, ""+str(list_veco01[0]+list_veco01[1]+list_veco01[2]+list_veco01[3]+list_veco01[4]), (760, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        # #
        cv2.putText(frame, "Direct2_1", (16, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        cv2.putText(frame, str(list_veco10[1]), (145, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco10[3]), (265, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco10[4]), (385, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco10[0]), (505, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco10[2]), (625, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        cv2.putText(frame, "" + str(list_veco10[0] + list_veco10[1] + list_veco10[2] + list_veco10[3] + list_veco10[4]), (760, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        # print(x0,y0)
        cv2.putText(frame, "Line1", (int(x0), int(y0)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, "Line2", (int(x3), int(y3)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        percent_process = count / total_frame * 100
        percent_process = int(round(percent_process))

        yield "data: {}\n\n".format(percent_process)

        out.write(frame)

def gen_video_u_turn(user,name_dir,x0,y0, x1,y1,classes):

    name_vi_dir = f'static/users/{user}/{name_dir}/{classes}_class/track/'
    name_vi = os.listdir(name_vi_dir)[0]
    link_video_up = name_vi_dir+name_vi
    print(link_video_up)
    vid = cv2.VideoCapture(link_video_up)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    name_vi = name_vi.replace(".", "_")
    path_vd_speed = f'static/users/{user}/{name_dir}/video_speed'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{user}/{name_dir}/video_speed/u_turn.mp4'
    print(link_out_video)
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)
    count = 0
    list_veco=[0] * 5
    f = open(f'static/users/{user}/{name_dir}/data_idlinetoline_u_turn.json')
    data = json.load(f)

    while (vid.isOpened()):

        ret, frame = vid.read()
        if ret:
            count += 1
            for i in data.keys():
                if data[i][1] == count:
                    list_veco[int(data[i][0])] += 1
        else:
            break


        cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), (255, 253, 0), 4)



        font_color = (0, 0, 255)
        font_size = 0.8
        font_thickness = 2
        cv2.putText(frame, "Cars     LGVs     HGVs     MCs     Buses", (140, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, "_U_TURN__", (16, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        cv2.putText(frame, str(list_veco[1]), (145, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[3]), (265, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[4]), (385, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[0]), (505, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco[2]), (625, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        cv2.putText(frame, "Total", (760, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        cv2.putText(frame, ""+str(list_veco[0]+list_veco[1]+list_veco[2]+list_veco[3]+list_veco[4]), (760, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        # #

        # print(x0,y0)
        cv2.putText(frame, "Line", (int(x0), int(y0)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        percent_process = count / total_frame * 100
        percent_process = int(round(percent_process))

        yield "data: {}\n\n".format(percent_process)

        out.write(frame)

def gen_video_2lines_9class(user,name_dir,x0,y0, x1,y1,x2,y2,x3,y3,classes="9"):

    name_vi_dir = f'static/users/{user}/{name_dir}/{classes}_class/track/'
    name_vi = os.listdir(name_vi_dir)[0]
    link_video_up = name_vi_dir+name_vi
    print(link_video_up)
    vid = cv2.VideoCapture(link_video_up)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    name_vi = name_vi.replace(".", "_")
    path_vd_speed = f'static/users/{user}/{name_dir}/video_speed'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{user}/{name_dir}/video_speed/2short_9class.mp4'
    print(link_out_video)
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)
    count = 0
    list_veco=[0] * 9
    f = open(f'static/users/{user}/{name_dir}/data_idlinetoline_d_hour.json')
    data = json.load(f)

    f_rs = open(f'static/users/{user}/{name_dir}/result.json')
    data_rs = json.load(f_rs)
    def sum_(d):
        sumd = 0
        for a in d:
            sumd += a
        return sumd

    list_veco_01=[0]*9
    list_veco_10=[0]*9

    while (vid.isOpened()):

        ret, frame = vid.read()
        if ret:
            count += 1
            a = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
            for k in a:
                for i in data_rs['0'][k]:
                    if i in data['0'].keys() and data['0'][i][1] == count:
                        list_veco_01[int(k)] += 1
                for i in data_rs['1'][k]:
                    if i in data['1'].keys() and data['1'][i][1] == count:
                        list_veco_10[int(k)] += 1
        else:
            break


        cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), (255, 253, 0), 4)
        cv2.line(frame, (int(x2), int(y2)), (int(x3), int(y3)), (255, 253, 0), 4)



        font_color = (0, 0, 255)
        font_size = 0.8
        font_thickness = 2
        cv2.putText(frame, "Motor  Bicycle    Car      Taxi     Coach    Bus      LGV     HGV      VHGV", (140, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, "Direct1_2 ", (16, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, str(list_veco_01[0]), (145, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[1]), (275, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[2]), (385, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[3]), (505, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[4]), (625, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[5]), (745, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[6]), (865, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[7]), (985, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_01[8]), (1105, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        #
        cv2.putText(frame, "Total", (1245, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
        cv2.putText(frame, "" + str(
            list_veco_01[0] + list_veco_01[1] + list_veco_01[2] + list_veco_01[3] + list_veco_01[4] + list_veco_01[5] +
            list_veco_01[6] +
            list_veco_01[7] + list_veco_01[8]), (1245, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0),
                    font_thickness)

        # #
        cv2.putText(frame, "Direct2_1", (16, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        #
        cv2.putText(frame, str(list_veco_10[0]), (145, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[1]), (275, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[2]), (385, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[3]), (505, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[4]), (625, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[5]), (745, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[6]), (865, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[7]), (985, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)
        cv2.putText(frame, str(list_veco_10[8]), (1105, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                    font_thickness)

        cv2.putText(frame, "" + str(
            list_veco_10[0] + list_veco_10[1] + list_veco_10[2] + list_veco_10[3] + list_veco_10[4] + list_veco_10[5] +
            list_veco_10[6] +
            list_veco_10[7] + list_veco_10[8]), (1245, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0),
                    font_thickness)
        # print(x0,y0)
        cv2.putText(frame, "Line1", (int(x0), int(y0)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(frame, "Line2", (int(x3), int(y3)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        percent_process = count / total_frame * 100
        percent_process = int(round(percent_process))

        yield "data: {}\n\n".format(percent_process)

        out.write(frame)