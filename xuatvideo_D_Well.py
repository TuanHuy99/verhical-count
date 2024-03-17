import json
import cv2
import os
import pandas as pd
from view_count_invideo import find_video_path


def gen_video_dwell_test(name_user,dir_video,data_dwell,x0,y0,x1,y1,x2,y2,x3,y3,classes):
    link_json_point= f'static/users/{name_user}/{dir_video}/data_point_{classes}.json'
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
    path_vd_speed=f'static/users/{name_user}/{dir_video}/video_area'
    if not os.path.exists(path_vd_speed):
        os.mkdir(path_vd_speed)
    link_out_video = f'static/users/{name_user}/{dir_video}/video_area/video_D_WELL_TIME.mp4'
    out = cv2.VideoWriter(link_out_video, fourcc, 30.0, size)

    # color=[(255,0,0), (0,255,0), (0,0,255), (255,0,255), (0,255,255)]
    color=[(255,225,0), (255,225,0), (255,225,0), (255,225,0), (255,225,0),(255,225,0),(255,225,0),(255,225,0),(255,225,0)]
    color=[(56, 56, 255), (151, 157, 255), (31,112,255), (29, 178, 255), (49,210,207)]
    color=[(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0)]
    classes=['motor','car','bus','lgv','hgv']

    # read xlsx
    df_excel=pd.read_excel(f'static/users/{name_user}/{dir_video}/excel_file/DWELL_TIME.xlsx')
    d_well_by_id = df_excel.set_index("ID")["D_well_time"]
    print(d_well_by_id.index)
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
        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 253, 0), 4)
        cv2.line(frame, (int(x3), int(y3)), (int(x2), int(y2)), (255, 253, 0), 4)
        cv2.line(frame, (int(x3), int(y3)), (int(x0), int(y0)), (255, 253, 0), 4)
        for id in list(data.keys()):
            # for id_vehicle, speed in d_well_by_id.items():
            # if int(id) == int(id_vehicle):
            if int(id) in d_well_by_id.index:
                for i in range(len(data[id]["cls"])):
                    x, y, f = data[id]["frame"][i][:3]
                    if f==count and data_dwell[id][0][0] <= f <= data_dwell[id][0][1]:
                        # print(int(data[id]["cls"][i]))
                        font_color = color[int(data[id]["cls"][i])]
                        # font_color = (255,0,0)
                        font_size = 0.8
                        font_thickness = 2
                        # cv2.rectangle(frame, (x-10, y-15), (x + 80, y + 10), (125, 125, 125), -1)
                        # cv2.putText(frame, classes[int(data[id]["cls"][i])]+":"+str(d_well_by_id[int(id)])+" km/h", (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                        cv2.putText(frame, str(d_well_by_id[int(id)]), (int(x-10), int(y)), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                        break
                    elif f>count:
                        break
        print(count)

        out.write(frame)

data_dwell={'6': [[80, 697], 2], '8': [[1, 668], 2], '11': [[1, 664], 2], '15': [[391, 759], 2], '82': [[2557, 3774], 2], '100': [[3464, 3853], 2], '103': [[3572, 3790], 6], '164': [[5392, 6513], 2], '168': [[5698, 6518], 2], '177': [[6334, 6550], 2], '307': [[11744, 13092], 2], '314': [[11952, 13080], 2], '318': [[11985, 13170], 2], '363': [[14919, 15368], 6], '364': [[15063, 15350], 2], '365': [[15143, 15313], 3], '415': [[16580, 17019], 2]}

gen_video_dwell_test('test3','0488',data_dwell,int(1258.75), int(446.75), int(1586.75), int(504.75), int(1578.75), int(376.75), int(1430.75), int(366.75),"9")