import json
import statistics

from flask import Flask, redirect, url_for, render_template, request, session, jsonify, Response, send_file
import os, glob
from PIL import Image
import datetime
import threading
from pathlib import Path
import pandas as pd
import random
import string

from app import app
from APIs.login_signup import login, addUser, removeUser
from caculate_quences import caculate_quences, quence_to_excel_form
from gen_video_speed import gen_video_speed, gen_video_2lines, gen_video_speed_test, gen_video_2lines_9class, \
    gen_video_u_turn
from utils import run_gen_json, check_size, find_point_up_down, direct_detector, cat_d, data_from_FE_hour, \
    direct_detector_2short, direct_detector_u_turn, direct_detector_2long
from utils import check_size_file
from APIs.get_video_in4 import get_create_time, get_video_information
from APIs.truy_van import check_projectID, addProject, get_project_name, addVideos, check_project_numclass, \
    add_need_download, add_wait_list, get_first_link_to_download, get_project_name_wait_list, get_all_error_link
from APIs.truy_van import get_project_name, get_first_wait_list, check_processing, get_all_project_wait_list
from process_video import create_json_file, download_video_dropbox, download_video_gg_drive, background_download, \
    process_wait_list
from time_to_frame import check_time_range, convert_time_lap_to_frame
from id_from_line_to_line import run_gen_json_hour, run_gen_json_hour_2, out_from_idlinetoline_with_frame, \
    out_from_idlinetoline_with_frame_2, run_gen_json_u_turn, out_from_idlinetoline_with_frame_u_turn
from view_count_invideo import gen_video_count, gen_video_count_9class
from well_time import check_id_in_area_well_time, xuat_excel_all_dwelltime, write_max_val, getMeanDistance
from xuatexcel_huy import xxuat_xlsx, xxuat_xlsx_9class
from speed_estimate import caculate_speed_v1, calculate_distance, get_start_end_time, caculate_speed_v2, \
    train_distance_model, caculate_speed_v3,caculate_speed_v3_MEDIAN

from threading import Thread


######################################################################
@app.route('/', methods=['GET', 'POST'])
def login_page():
    role = ""
    # session["role"] = ''
    if request.method == "POST":
        user_name = request.form.get("user")
        pass_word = request.form.get("password")
        print(f"USER: {user_name}, PASS: {pass_word}")

        role = login(user=user_name, password=pass_word)
        print(f"ROLE: {role}")
        if role:
            if role == 'Admin':
                print("Toi la Admin")
                return redirect(url_for('home_admin'))

            return redirect(url_for('home_user', user=user_name))

    return render_template('login.html', err_msg=role)


######################################################################
@app.route('/user/<user>')
def home_user(user):
    print('User: ', user)
    projects = os.listdir(f'static/users/{user}')
    print(projects)

    process_project = get_all_project_wait_list()
    if not process_project:
        process_project = []

    error_links = get_all_error_link(user=user)
    if not error_links:
        error_links = []

    project_name = {}
    for project in projects:
        project_name[project] = get_project_name(project)
    for project in process_project:
        project_name[project] = get_project_name_wait_list(project)

    num_video = {}
    for project in projects:
        num_video[project] = len(glob.glob(f'static/users/{user}/{project}/*.mp4'))

    project_size = {}
    for project in projects:
        project_size[project] = check_size(f'static/users/{user}/{project}')

    create_time = {}
    for project in projects:
        create_time[project] = get_create_time(f'static/users/{user}/{project}')

    return render_template('home.html', projects=projects, num_video=num_video, project_name=project_name,
                           project_size=project_size, create_time=create_time, username=user,
                           process_project=process_project, error_links=error_links)


######################################################################
@app.route('/admin')
def home_admin():
    users = os.listdir("static/users")

    return render_template('homeAdmin.html', users=users)


######################################################################
@app.route('/draw_line/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    num_ve_0 = [0] * 5
    num_ve_1 = [0] * 5
    num_ve_2 = [0] * 5
    num_ve_3 = [0] * 5
    max_index = [0] * 5
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        if check_project_numclass(dir_video, num_class):
            return render_template("wait.html")

        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))
        x4 = float(request.form.get("x4"))
        y4 = float(request.form.get("y4"))
        x5 = float(request.form.get("x5"))
        y5 = float(request.form.get("y5"))
        x6 = float(request.form.get("x6"))
        y6 = float(request.form.get("y6"))
        x7 = float(request.form.get("x7"))
        y7 = float(request.form.get("y7"))
        x8 = float(request.form.get("x8"))
        y8 = float(request.form.get("y8"))
        x9 = float(request.form.get("x9"))
        y9 = float(request.form.get("y9"))

        print(x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7)
        print(type(x), type(y))

        x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)
        x4, y4, x5, y5 = find_point_up_down(x4, y4, x5, y5)
        x6, y6, x7, y7 = find_point_up_down(x6, y6, x7, y7)

        link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
        save_json_gen = f'static/users/{name_user}/{dir_video}'
        run_gen_json(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8,
                     y8, x9, y9)
        dir_path = f'static/users/{name_user}/{dir_video}'
        num_ve_0, num_ve_1, num_ve_2, num_ve_3 = direct_detector(dir_path, name_user)

        result = []
        for values in zip(num_ve_0, num_ve_1, num_ve_2, num_ve_3):
            result.append(max(values))

        return render_template('draw_line.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, num_ve_0=num_ve_0, num_ve_1=num_ve_1,
                               num_ve_2=num_ve_2, num_ve_3=num_ve_3, max_index=result, x0=x, y0=y,
                               x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, x5=x5, y5=y5,
                               x6=x6, y6=y6, x7=x7, y7=y7, num_class=num_class)

    return render_template('draw_line.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_ve_0=num_ve_0, num_ve_1=num_ve_1,
                           num_ve_2=num_ve_2, num_ve_3=num_ve_3, max_index=max_index, num_class=num_class)


######################################################################
@app.route('/draw_line_4_long/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy_4_long(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # if check_project_numclass(dir_video, num_class):
        #     return render_template("thanks.html")

        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))
        x4 = float(request.form.get("x4"))
        y4 = float(request.form.get("y4"))
        x5 = float(request.form.get("x5"))
        y5 = float(request.form.get("y5"))
        x6 = float(request.form.get("x6"))
        y6 = float(request.form.get("y6"))
        x7 = float(request.form.get("x7"))
        y7 = float(request.form.get("y7"))
        x8 = float(request.form.get("x8"))
        y8 = float(request.form.get("y8"))
        x9 = float(request.form.get("x9"))
        y9 = float(request.form.get("y9"))

        time1 = str(request.form.get("time1"))
        time2 = str(request.form.get("time2"))
        start = str(request.form.get("start"))
        end = str(request.form.get("end"))
        numM = str(request.form.get("numM"))
        print(x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7)
        print(type(x), type(y))

        x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)
        x4, y4, x5, y5 = find_point_up_down(x4, y4, x5, y5)
        x6, y6, x7, y7 = find_point_up_down(x6, y6, x7, y7)

        if check_time_range(start, end, time1, time2):
            list_time, list_frame = convert_time_lap_to_frame(time1, start, end, int(numM))

            link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
            save_json_gen = f'static/users/{name_user}/{dir_video}'
            # run_gen_json(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7)
            run_gen_json_hour(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7,
                              y7, x8, y8, x9, y9)

            link_json_linetoline = f'static/users/{name_user}/{dir_video}/data_idlinetoline_d_hour.json'

            dict_0, dict_1, dict_2, dict_3 = out_from_idlinetoline_with_frame(list_frame, link_json_linetoline)
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            for j in range(len(dict_0.values())):
                list1.append([int(num.strip()) for num in list(dict_0.values())[j][1:-1].split(',')])
                list2.append([int(num.strip()) for num in list(dict_1.values())[j][1:-1].split(',')])
                list3.append([int(num.strip()) for num in list(dict_2.values())[j][1:-1].split(',')])
                list4.append([int(num.strip()) for num in list(dict_3.values())[j][1:-1].split(',')])
            merged_lists = [[list1[i], list2[i], list3[i], list4[i]] for i in range(len(list1))]
            # print(list1,list2,list3,list4)

            num_ve = []
            for sublist in merged_lists:
                max_sublist = []
                for i in range(len(sublist[0])):
                    max_value = max([sublist[j][i] for j in range(len(sublist))])
                    max_sublist.append(max_value)
                num_ve.append(max_sublist)

        else:
            list_time, list_frame = ['check your input time'], [0, 0]
            num_ve = [['none'] * 9]
        column_names = ["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV"]

        print(list_time)
        thoi_gian = list_time
        thoi_giani = thoi_gian
        # Thay thế các giá trị trong mảng
        for i in range(len(thoi_gian)):
            if len(thoi_gian[i][0]) == 4 and thoi_gian[i][0][-2:] == ':0':
                thoi_gian[i][0] = thoi_gian[i][0] + '0'
            if len(thoi_gian[i][1]) == 4 and thoi_gian[i][1][-2:] == ':0':
                thoi_gian[i][1] = thoi_gian[i][1] + '0'
            if len(thoi_gian[i][0]) == 4:
                thoi_gian[i][0] = '0' + thoi_gian[i][0]

            if len(thoi_gian[i][1]) == 4:
                thoi_gian[i][1] = '0' + thoi_gian[i][1]

            if len(thoi_gian[i][0]) == 3:
                thoi_gian[i][0] = '0' + thoi_gian[i][0] + '0'

            if len(thoi_gian[i][1]) == 3:
                thoi_gian[i][1] = '0' + thoi_gian[i][1] + '0'

            thoi_giani[i] = thoi_gian[i][0].replace(':', '') + ' - ' + thoi_gian[i][1].replace(':', '')
        list_time1 = thoi_giani
        print(num_ve)
        # df = pd.DataFrame(num_ve, columns=column_names)
        # df.insert(0, "Time to time", list_time)
        num_ve_5 = []
        if num_class == 5:
            for i in range(len(num_ve)):
                c = []
                c.append(num_ve[i][0] + num_ve[i][1])
                c.append(num_ve[i][2] + num_ve[i][3])
                c.append(num_ve[i][4] + num_ve[i][5])
                c.append(num_ve[i][6])
                c.append(num_ve[i][7] + num_ve[i][8])
                num_ve_5.append(c)
            xxuat_xlsx(f'static/users/{name_user}/{dir_video}/result_5ex.xlsx', list_time1, num_ve_5, dir_video)
        else:
            xxuat_xlsx_9class(f'static/users/{name_user}/{dir_video}/result_9ex.xlsx', list_time1, num_ve, dir_video)
        print("xuat mau roi")
        # Lưu DataFrame vào file CSV
        # df.to_csv(f'static/users/{name_user}/{dir_video}/data_time_out.csv', index=False)
        if num_class == 9:
            print(1)
            return render_template('draw_line_hour_4_9.html', name_user=name_user, dir_video=dir_video,
                                   size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time,
                                   file_path=dir_video, numM=numM, x0=x, y0=y,
                                   x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, x5=x5, y5=y5,
                                   x6=x6, y6=y6, x7=x7, y7=y7, x8=x8, x9=x9, y9=y9, time1=time1, time2=time2,
                                   start=start, end=end, num_class=num_class)
        else:
            print(2)
            return render_template('draw_line_hour_4_5.html', name_user=name_user, dir_video=dir_video,
                                   size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time,
                                   file_path=dir_video, numM=numM, x0=x, y0=y,
                                   x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, x5=x5, y5=y5,
                                   x6=x6, y6=y6, x7=x7, y7=y7, x8=x8, x9=x9, y9=y9, time1=time1, time2=time2,
                                   start=start, end=end, num_class=num_class)
    list_time, list_frame = ['check your input time'], [0, 0]
    num_ve = [[0] * 9]
    if num_class == 9:
        print(11)
        return render_template('draw_line_hour_4_9.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time,
                               file_path=dir_video, num_class=num_class)
    else:
        print(22)
        return render_template('draw_line_hour_4_5.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time,
                               file_path=dir_video, num_class=num_class)


######################################################################


@app.route('/draw_line_2_long/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy_2_long(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        time1 = str(request.form.get("time1"))
        time2 = str(request.form.get("time2"))
        start = str(request.form.get("start"))
        end = str(request.form.get("end"))
        numM = str(request.form.get("numM"))

        x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)

        if check_time_range(start, end, time1, time2):
            list_time, list_frame = convert_time_lap_to_frame(time1, start, end, int(numM))

            link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
            save_json_gen = f'static/users/{name_user}/{dir_video}'
            # run_gen_json(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7)
            run_gen_json_hour_2(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3)

            link_json_linetoline = f'static/users/{name_user}/{dir_video}/'

            dict_0 = direct_detector_2long(list_frame, link_json_linetoline)
            v = list(dict_0.values())
            num_ve = []
            for i in range(len(v)):
                num_ve.append([int(num.strip()) for num in v[i][1:-1].split(',')])
            print(num_ve)

        else:
            list_time, list_frame = ['check your input time'], [0, 0]
            num_ve = [[0] * 9]
        thoi_gian = list_time
        thoi_giani = thoi_gian
        # Thay thế các giá trị trong mảng
        for i in range(len(thoi_gian)):
            if len(thoi_gian[i][0]) == 4 and thoi_gian[i][0][-2:] == ':0':
                thoi_gian[i][0] = thoi_gian[i][0] + '0'
            if len(thoi_gian[i][1]) == 4 and thoi_gian[i][1][-2:] == ':0':
                thoi_gian[i][1] = thoi_gian[i][1] + '0'
            if len(thoi_gian[i][0]) == 4:
                thoi_gian[i][0] = '0' + thoi_gian[i][0]

            if len(thoi_gian[i][1]) == 4:
                thoi_gian[i][1] = '0' + thoi_gian[i][1]

            if len(thoi_gian[i][0]) == 3:
                thoi_gian[i][0] = '0' + thoi_gian[i][0] + '0'

            if len(thoi_gian[i][1]) == 3:
                thoi_gian[i][1] = '0' + thoi_gian[i][1] + '0'

            thoi_giani[i] = thoi_gian[i][0].replace(':', '') + ' - ' + thoi_gian[i][1].replace(':', '')
        list_time1 = thoi_giani
        print(num_ve)
        # df = pd.DataFrame(num_ve, columns=column_names)
        # df.insert(0, "Time to time", list_time)
        num_ve_5 = []
        if num_class == 5:
            for i in range(len(num_ve)):
                c = []
                c.append(num_ve[i][0] + num_ve[i][1])
                c.append(num_ve[i][2] + num_ve[i][3])
                c.append(num_ve[i][4] + num_ve[i][5])
                c.append(num_ve[i][6])
                c.append(num_ve[i][7] + num_ve[i][8])
                num_ve_5.append(c)
            xxuat_xlsx(f'static/users/{name_user}/{dir_video}/result_5ex_2lines.xlsx', list_time1, num_ve, dir_video)
        else:
            xxuat_xlsx_9class(f'static/users/{name_user}/{dir_video}/result_9ex_2lines.xlsx', list_time1, num_ve, dir_video)
        print("xuat mau roi")

        if num_class == 9:

            return render_template('draw_line_hour_2_9.html', name_user=name_user, dir_video=dir_video,
                                   size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time1,
                                   file_path=dir_video, numM=numM, x0=x, y0=y,
                                   x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, num_ve_0=num_ve[0], num_ve_1=num_ve[1],
                                   time1=time1, time2=time2, start=start, end=end, num_class=num_class)
        else:

            return render_template('draw_line_hour_2_5.html', name_user=name_user, dir_video=dir_video,
                                   size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time,
                                   file_path=dir_video, numM=numM, x0=x, y0=y,
                                   x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, time1=time1, time2=time2,
                                   start=start, end=end, num_class=num_class)
    list_time, list_frame = ['check your input time'], [0, 0]
    num_ve = [[0] * 9]
    if num_class == 9:
        print(11)
        return render_template('draw_line_hour_2_9.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time,
                               file_path=dir_video, num_class=num_class)
    else:
        print(22)
        return render_template('draw_line_hour_2_5.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, data=enumerate(num_ve), list_time=list_time,
                               file_path=dir_video, num_class=num_class)


######################################################################

@app.route("/<username>/upload_videos", methods=['GET', 'POST'])
def upload_video(username):
    if request.method == 'POST':
        link_tf = request.form.get('link_tf')
        num_class = request.form.get('class')
        if not num_class:
            num_class = 5
        else:
            num_class = int(num_class)
        link_db = request.form.get('link_dropbox')
        link_gg = request.form.get('link_drive')
        link_zip = request.form.get('link_zip')
        if link_zip:
            link_zip = link_zip.replace('\\', '/')
        # link_zip.replace('"', '')
        print(link_zip)
        directory_name = request.form.get('directory_name')
        day_upload = datetime.datetime.now()
        key_dropbox = request.form.get('keys_dropbox')

        if link_tf:
            print(2000000)
            if get_first_link_to_download():
                add_need_download(link=link_tf, type='transfer', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
            else:
                add_need_download(link=link_tf, type='transfer', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
                background_thread = threading.Thread(target=background_download)
                background_thread.start()
                print("Thread name:", threading.current_thread().name)

            return render_template('thanks.html', name_user=username)

        if link_db:
            print(2000001)
            print("Keys: ", key_dropbox)
            print(type(key_dropbox))
            if get_first_link_to_download():
                add_need_download(link=link_db, type='dropbox', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
            else:
                add_need_download(link=link_db, type='dropbox', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
                background_thread = threading.Thread(target=background_download, args=(key_dropbox))
                background_thread.start()
                print("Thread name:", threading.current_thread().name)

            return render_template('thanks.html', name_user=username)

        elif link_gg:
            print(3000000)
            if get_first_link_to_download():
                add_need_download(link=link_gg, type='gg-drive', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
            else:
                add_need_download(link=link_gg, type='gg-drive', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
                background_thread = threading.Thread(target=background_download)
                background_thread.start()
                print("Thread name:", threading.current_thread().name)

            return render_template('thanks.html', name_user=username)

        elif link_zip:
            print(4000000)
            if get_first_link_to_download():
                add_need_download(link=link_zip, type='zip', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
            else:
                add_need_download(link=link_zip, type='zip', name=directory_name, num_class=num_class,
                                  day_upload=day_upload, user=username)
                background_thread = threading.Thread(target=background_download)
                background_thread.start()
                print("Thread name:", threading.current_thread().name)

            return render_template('thanks.html', name_user=username)

        elif len(request.files) > 0:
            print(1000000)
            randomID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            # Kiem tra xem ID da xuat hien chua. Neu da xuat hien se sinh ra 1 ID moi
            while (check_projectID(randomID)):
                randomID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

            directory_path = os.path.join(f"../veco-v3/static/users/{username}/", randomID)
            os.makedirs(directory_path, exist_ok=True)
            files = request.files.getlist('files')
            for file in files:
                print(f"Saving {file.filename}")
                file.save(f'{directory_path}/{file.filename}')

            day_upload = datetime.datetime.now()

            if not get_first_wait_list():
                print(100)
                add_wait_list(project_id=randomID, num_class=num_class, time_create=day_upload, user=username,
                              name=directory_name)
                if not check_processing():
                    print(300)
                    process_wait_list()

            else:
                print(200)
                add_wait_list(project_id=randomID, num_class=num_class, time_create=day_upload, user=username,
                              name=directory_name)

            return render_template('thanks.html', name_user=username)
        else:
            return "Vui long kiem tra lai"

        # add thong tin vao database

    return render_template('upload.html', name_user=username)


######################################################################
@app.route("/<username>/<project>/not_process/<num_class>", methods=['GET', 'POST'])
def reprocess_video(username, project, num_class):
    project_name = get_project_name(projectID=project)
    if request.method == 'POST':
        directory_path = os.path.join(f"static/users/{username}/", project)
        time_now = datetime.datetime.now()
        if not get_first_wait_list():
            add_wait_list(project_id=project, num_class=num_class, time_create=time_now, user=username,
                          name=project_name)
            if not check_processing():
                background_thread = threading.Thread(target=process_wait_list)
                background_thread.start()
        else:
            print(200)
            add_wait_list(project_id=project, num_class=num_class, time_create=time_now, user=username,
                          name=project_name)

        return render_template('thanks.html', name_user=username)

    return render_template('choose_create_9_or_5_class.html', name_class=num_class, name_project=project_name,
                           user_name=username, project_id=project)


######################################################################
@app.route('/truncate')
def truncate_table():
    pass


######################################################################
@app.route('/delete/<user>/<projectID>')
def remove_project(user, projectID):
    project_path = os.path.join(f"static/users/{user}/", projectID)
    os.rmdir(project_path)


####download excel
@app.route('/<name_user>/<dir_video>/download-excel_4_5')
def download_excel(name_user, dir_video):
    path_excel = f'static/users/{name_user}/{dir_video}/result_5ex.xlsx'
    if os.path.isfile(path_excel):
        return send_file(path_excel, as_attachment=True)
    else:
        return "Vui long kiem tra lại"

@app.route('/<name_user>/<dir_video>/download-excel_4_9')
def download_excel_4_9(name_user, dir_video):
    path_excel = f'static/users/{name_user}/{dir_video}/result_9ex.xlsx'
    if os.path.isfile(path_excel):
        return send_file(path_excel, as_attachment=True)
    else:
        return "Vui long kiem tra lại"


####download excel
@app.route('/<name_user>/<dir_video>/download-excel_2_5')
def download_excel_2lines(name_user, dir_video):
    path_excel = f'static/users/{name_user}/{dir_video}/result_5ex_2lines.xlsx'
    if os.path.isfile(path_excel):
        return send_file(path_excel, as_attachment=True)
    else:
        return "Vui long kiem tra lại"
####download excel
@app.route('/<name_user>/<dir_video>/download-excel_2_9')
def download_excel_2lines_9(name_user, dir_video):
    path_excel = f'static/users/{name_user}/{dir_video}/result_9ex_2lines.xlsx'
    if os.path.isfile(path_excel):
        return send_file(path_excel, as_attachment=True)
    else:
        return "Vui long kiem tra lại"


@app.route('/draw_line_2_short/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy_2short(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    num_ve_0_1 = [0] * 5
    num_ve_1_0 = [0] * 5
    num_ve_2 = [0] * 5
    num_ve_3 = [0] * 5
    max_index = [0] * 5
    list_frame = [[0, 30000]]
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        if check_project_numclass(dir_video, num_class):
            return render_template("wait.html")

        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        print(x, y, x1, y1, x2, y2, x3, y3)
        print(type(x), type(y))

        x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)
        print(x, y, x1, y1)
        print(x2, y2, x3, y3)

        link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
        save_json_gen = f'static/users/{name_user}/{dir_video}'
        # run_gen_json(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7)
        run_gen_json_hour_2(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3)

        link_json_linetoline = f'static/users/{name_user}/{dir_video}'
        num_ve_0_1, num_ve_1_0 = direct_detector_2short(link_json_linetoline)
        print("0 to 1: ",sum(num_ve_0_1))
        print("1 to 0: ",sum(num_ve_1_0))
        numve01 = [num_ve_0_1[0] + num_ve_0_1[1], num_ve_0_1[2] + num_ve_0_1[3], num_ve_0_1[4] + num_ve_0_1[5], num_ve_0_1[6], num_ve_0_1[7] + num_ve_0_1[8]]

        numve10 = [num_ve_1_0[0] + num_ve_1_0[1], num_ve_1_0[2] + num_ve_1_0[3], num_ve_1_0[4] + num_ve_1_0[5], num_ve_1_0[6], num_ve_1_0[7] + num_ve_1_0[8]]

        return render_template('draw_line_2short.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, num_ve_0_1=numve01, num_ve_1_0=numve10,
                               num_ve_2=num_ve_2, num_ve_3=num_ve_3, x0=x, y0=y,
                               x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, num_class=num_class)

    return render_template('draw_line_2short.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_ve_0_1=num_ve_0_1, num_ve_1_0=num_ve_1_0,
                           num_ve_2=num_ve_2, num_ve_3=num_ve_3, max_index=max_index, num_class=num_class)


    ######################################################################

@app.route('/draw_4lines_9class_short/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy_9classes_4lines_short(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    num_ve_0 = [0] * 9
    num_ve_1 = [0] * 9
    num_ve_2 = [0] * 9
    num_ve_3 = [0] * 9
    max_index = [0] * 9
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        if check_project_numclass(dir_video, num_class):
            return render_template("wait.html")

        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))
        x4 = float(request.form.get("x4"))
        y4 = float(request.form.get("y4"))
        x5 = float(request.form.get("x5"))
        y5 = float(request.form.get("y5"))
        x6 = float(request.form.get("x6"))
        y6 = float(request.form.get("y6"))
        x7 = float(request.form.get("x7"))
        y7 = float(request.form.get("y7"))
        x8 = float(request.form.get("x8"))
        y8 = float(request.form.get("y8"))
        x9 = float(request.form.get("x9"))
        y9 = float(request.form.get("y9"))

        print(x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7)
        print(type(x), type(y))

        x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)
        x4, y4, x5, y5 = find_point_up_down(x4, y4, x5, y5)
        x6, y6, x7, y7 = find_point_up_down(x6, y6, x7, y7)

        link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
        save_json_gen = f'static/users/{name_user}/{dir_video}'
        run_gen_json(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8,
                     y8, x9, y9)
        dir_path = f'static/users/{name_user}/{dir_video}'
        num_ve_0, num_ve_1, num_ve_2, num_ve_3 = direct_detector(dir_path, name_user)

        result = []
        for values in zip(num_ve_0, num_ve_1, num_ve_2, num_ve_3):
            result.append(max(values))

        return render_template('draw_4lines_9short.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, num_ve_0=num_ve_0, num_ve_1=num_ve_1,
                               num_ve_2=num_ve_2, num_ve_3=num_ve_3, max_index=result, x0=x, y0=y,
                               x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, x4=x4, y4=y4, x5=x5, y5=y5,
                               x6=x6, y6=y6, x7=x7, y7=y7, num_class=num_class)

    return render_template('draw_4lines_9short.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_ve_0=num_ve_0, num_ve_1=num_ve_1,
                           num_ve_2=num_ve_2, num_ve_3=num_ve_3, max_index=max_index, num_class=num_class)


######################################################################

@app.route('/draw_2lines_9class_short/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy_9classes_2lines_short(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    num_ve_0 = [0] * 9
    num_ve_1 = [0] * 9
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        if check_project_numclass(dir_video, num_class):
            return render_template("wait.html")

        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        print(type(x), type(y))

        x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)
        link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
        save_json_gen = f'static/users/{name_user}/{dir_video}'
        run_gen_json_hour_2(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3)
        dir_path = f'static/users/{name_user}/{dir_video}'
        num_ve_0, num_ve_1 = direct_detector_2short(dir_path)

        return render_template('draw_2lines_9short.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, num_ve_0=num_ve_0, num_ve_1=num_ve_1, x0=x, y0=y,
                               x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, num_class=num_class)

    return render_template('draw_2lines_9short.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_ve_0=num_ve_0, num_ve_1=num_ve_1,
                           num_class=num_class)


######################################################################

@app.route('/<name_user>/<dir_video>/speed/<num_class>', methods=['GET', 'POST'])
def verhical_speed(name_user, dir_video, num_class):
    project_dir = f'static/users/{name_user}/{dir_video}'
    str_start_time, str_end_time, FPS = get_start_end_time(project_dir)

    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        disss = str(request.form.get("distance"))
        disss = disss.replace(",", ".").replace(" ", ".")
        distance_in_meter = float(disss)

        str_start_time = request.form.get("str_start_time")
        str_end_time = request.form.get("str_end_time")

        dir_path = f'static/users/{name_user}/{dir_video}'
        link_json_point = f'{dir_path}/data_point_{num_class}.json'
        # Opening JSON file
        f = open(link_json_point)
        # toa do 4 diem (2 lines lần lượt)
        data = json.load(f)
        a, b, a2, b2, x, y, x1, y1, x2, y2, x3, y3 = data_from_FE_hour(x, y, x1, y1, x2, y2, x3, y3)
        d1 = {}
        d2 = {}

        # dem theo giao diem
        for m in data.keys():
            cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
            cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)

        d = {0: d1, 1: d2}

        with open(f"{dir_path}/speed.json", "w") as outfile:
            json.dump(d, outfile)

        center_line1 = [int((x + x1) / 2), int((y + y1) / 2)]
        center_line2 = [int((x2 + x3) / 2), int((y2 + y3) / 2)]

        distance_in_pixel = calculate_distance(center_line1[0], center_line1[1], center_line2[0], center_line2[1])

        # speed_class_infor, speed_each_values = caculate_speed_v1(user=name_user, projectID=dir_video, distance_in_pixel=distance_in_pixel,
        #                distance_in_meter=distance_in_meter, num_class=num_class, time_start_str=str_start_time, time_end_str=str_end_time,
        #                                                       FPS=FPS)

        speed_class_infor, speed_each_values = caculate_speed_v2(user=name_user, projectID=dir_video,
                                                                 distance_in_meter=distance_in_meter,
                                                                 num_class=num_class, time_start_str=str_start_time,
                                                                 time_end_str=str_end_time, FPS=FPS)

        list_vehicle = ["Motor", "Car", "Bus", "LGV", "HGV", "ALL"]
        if num_class==9:
            list_vehicle=["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV","ALL"]

        return render_template('draw_line_speed.html', speed_class_infor=speed_class_infor,
                               speed_each_values=speed_each_values,
                               name_user=name_user, dir_video=dir_video, size_w=width, size_h=height,
                               file_path=dir_video, x0=x, y0=y, x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3,
                               num_class=num_class,
                               list_vehicle=list_vehicle, str_start_time=str_start_time, str_end_time=str_end_time)

    return render_template('draw_line_speed.html', name_user=name_user, dir_video=dir_video, num_class=num_class,
                           size_w=width, size_h=height, str_start_time=str_start_time, str_end_time=str_end_time)


######################################################################
@app.route('/<name_user>/<dir_video>/speed_one_third/<num_class>', methods=['GET', 'POST'])
def verhical_speed_one_third(name_user, dir_video, num_class):
    project_dir = f'static/users/{name_user}/{dir_video}'
    str_start_time, str_end_time, FPS = get_start_end_time(project_dir)

    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        disss = str(request.form.get("distance"))
        disss = disss.replace(",", ".").replace(" ", ".")
        distance_in_meter = float(disss)

        str_start_time = request.form.get("str_start_time")
        str_end_time = request.form.get("str_end_time")

        dir_path = f'static/users/{name_user}/{dir_video}'
        link_json_point = f'{dir_path}/data_point_{num_class}.json'
        # Opening JSON file
        f = open(link_json_point)
        # toa do 4 diem (2 lines lần lượt)
        data = json.load(f)
        a, b, a2, b2, x, y, x1, y1, x2, y2, x3, y3 = data_from_FE_hour(x, y, x1, y1, x2, y2, x3, y3)
        d1 = {}
        d2 = {}

        # dem theo giao diem
        for m in data.keys():
            cat_d(x, y, x1, y1, data[m]['one_third_center'], d1, int(statistics.median(data[m]['cls'])), m)
            cat_d(x2, y2, x3, y3, data[m]['one_third_center'], d2, int(statistics.median(data[m]['cls'])), m)

        d = {0: d1, 1: d2}

        with open(f"{dir_path}/speed.json", "w") as outfile:
            json.dump(d, outfile)

        center_line1 = [int((x + x1) / 2), int((y + y1) / 2)]
        center_line2 = [int((x2 + x3) / 2), int((y2 + y3) / 2)]

        distance_in_pixel = calculate_distance(center_line1[0], center_line1[1], center_line2[0], center_line2[1])

        # speed_class_infor, speed_each_values = caculate_speed_v1(user=name_user, projectID=dir_video, distance_in_pixel=distance_in_pixel,
        #                distance_in_meter=distance_in_meter, num_class=num_class, time_start_str=str_start_time, time_end_str=str_end_time,
        #                                                       FPS=FPS)

        speed_class_infor, speed_each_values = caculate_speed_v2(user=name_user, projectID=dir_video,
                                                                 distance_in_meter=distance_in_meter,
                                                                 num_class=num_class, time_start_str=str_start_time,
                                                                 time_end_str=str_end_time, FPS=FPS)

        list_vehicle = ["Motor", "Car", "Bus", "LGV", "HGV", "ALL"]
        if num_class==9:
            list_vehicle=["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV","ALL"]

        return render_template('draw_line_speed.html', speed_class_infor=speed_class_infor,
                               speed_each_values=speed_each_values,
                               name_user=name_user, dir_video=dir_video, size_w=width, size_h=height,
                               file_path=dir_video, x0=x, y0=y, x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3,
                               num_class=num_class,
                               list_vehicle=list_vehicle, str_start_time=str_start_time, str_end_time=str_end_time)

    return render_template('draw_line_speed.html', name_user=name_user, dir_video=dir_video, num_class=num_class,
                           size_w=width, size_h=height, str_start_time=str_start_time, str_end_time=str_end_time)


@app.route('/<name_user>/<dir_video>/speed_left/<num_class>', methods=['GET', 'POST'])
def verhical_speed_left(name_user, dir_video, num_class):
    project_dir = f'static/users/{name_user}/{dir_video}'
    str_start_time, str_end_time, FPS = get_start_end_time(project_dir)

    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        disss = str(request.form.get("distance"))
        disss = disss.replace(",", ".").replace(" ", ".")
        distance_in_meter = float(disss)

        str_start_time = request.form.get("str_start_time")
        str_end_time = request.form.get("str_end_time")

        dir_path = f'static/users/{name_user}/{dir_video}'
        link_json_point = f'{dir_path}/data_point_{num_class}.json'
        # Opening JSON file
        f = open(link_json_point)
        # toa do 4 diem (2 lines lần lượt)
        data = json.load(f)
        a, b, a2, b2, x, y, x1, y1, x2, y2, x3, y3 = data_from_FE_hour(x, y, x1, y1, x2, y2, x3, y3)
        d1 = {}
        d2 = {}

        # dem theo giao diem
        for m in data.keys():
            cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
            cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)

        d = {0: d1, 1: d2}

        with open(f"{dir_path}/speed.json", "w") as outfile:
            json.dump(d, outfile)

        center_line1 = [int((x + x1) / 2), int((y + y1) / 2)]
        center_line2 = [int((x2 + x3) / 2), int((y2 + y3) / 2)]

        distance_in_pixel = calculate_distance(center_line1[0], center_line1[1], center_line2[0], center_line2[1])

        # speed_class_infor, speed_each_values = caculate_speed_v1(user=name_user, projectID=dir_video, distance_in_pixel=distance_in_pixel,
        #                distance_in_meter=distance_in_meter, num_class=num_class, time_start_str=str_start_time, time_end_str=str_end_time,
        #                                                       FPS=FPS)

        speed_class_infor, speed_each_values = caculate_speed_v2(user=name_user, projectID=dir_video,
                                                                 distance_in_meter=distance_in_meter,
                                                                 num_class=num_class, time_start_str=str_start_time,
                                                                 time_end_str=str_end_time, FPS=FPS)

        list_vehicle = ["Motor", "Car", "Bus", "LGV", "HGV", "ALL"]
        if num_class==9:
            list_vehicle=["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV","ALL"]

        return render_template('draw_line_speed.html', speed_class_infor=speed_class_infor,
                               speed_each_values=speed_each_values,
                               name_user=name_user, dir_video=dir_video, size_w=width, size_h=height,
                               file_path=dir_video, x0=x, y0=y, x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3,
                               num_class=num_class,
                               list_vehicle=list_vehicle, str_start_time=str_start_time, str_end_time=str_end_time)

    return render_template('draw_line_speed.html', name_user=name_user, dir_video=dir_video, num_class=num_class,
                           size_w=width, size_h=height, str_start_time=str_start_time, str_end_time=str_end_time)


@app.route('/<name_user>/<dir_video>/speed_bottom/<num_class>', methods=['GET', 'POST'])
def verhical_speed_bottom(name_user, dir_video, num_class):
    project_dir = f'static/users/{name_user}/{dir_video}'
    str_start_time, str_end_time, FPS = get_start_end_time(project_dir)

    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        disss = str(request.form.get("distance"))
        disss = disss.replace(",", ".").replace(" ", ".")
        distance_in_meter = float(disss)

        str_start_time = request.form.get("str_start_time")
        str_end_time = request.form.get("str_end_time")

        dir_path = f'static/users/{name_user}/{dir_video}'
        link_json_point = f'{dir_path}/data_point_{num_class}.json'
        # Opening JSON file
        f = open(link_json_point)

        data = json.load(f)
        a, b, a2, b2, x, y, x1, y1, x2, y2, x3, y3 = data_from_FE_hour(x, y, x1, y1, x2, y2, x3, y3)
        d1 = {}
        d2 = {}


        for m in data.keys():
            cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
            cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)

        d = {0: d1, 1: d2}

        with open(f"{dir_path}/speed.json", "w") as outfile:
            json.dump(d, outfile)

        center_line1 = [int((x + x1) / 2), int((y + y1) / 2)]
        center_line2 = [int((x2 + x3) / 2), int((y2 + y3) / 2)]

        distance_in_pixel = calculate_distance(center_line1[0], center_line1[1], center_line2[0], center_line2[1])

        # speed_class_infor, speed_each_values = caculate_speed_v1(user=name_user, projectID=dir_video, distance_in_pixel=distance_in_pixel,
        #                distance_in_meter=distance_in_meter, num_class=num_class, time_start_str=str_start_time, time_end_str=str_end_time,
        #                                                       FPS=FPS)

        speed_class_infor, speed_each_values = caculate_speed_v2(user=name_user, projectID=dir_video,
                                                                 distance_in_meter=distance_in_meter,
                                                                 num_class=num_class, time_start_str=str_start_time,
                                                                 time_end_str=str_end_time, FPS=FPS)

        list_vehicle = ["Motor", "Car", "Bus", "LGV", "HGV", "ALL"]
        if num_class==9:
            list_vehicle=["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV","ALL"]

        return render_template('draw_line_speed.html', speed_class_infor=speed_class_infor,
                               speed_each_values=speed_each_values,
                               name_user=name_user, dir_video=dir_video, size_w=width, size_h=height,
                               file_path=dir_video, x0=x, y0=y, x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3,
                               num_class=num_class,
                               list_vehicle=list_vehicle, str_start_time=str_start_time, str_end_time=str_end_time)

    return render_template('draw_line_speed.html', name_user=name_user, dir_video=dir_video, num_class=num_class,
                           size_w=width, size_h=height, str_start_time=str_start_time, str_end_time=str_end_time)


@app.route('/<name_user>/<dir_video>/download-speed')
def download_speed(name_user, dir_video):
    path_excel = f'static/users/{name_user}/{dir_video}/speed.xlsx'
    if os.path.isfile(path_excel):
        return send_file(path_excel, as_attachment=True)
    else:
        return "Vui long kiem tra lại"


@app.route('/<name_user>/<dir_video>/process-video-speed', methods=['GET', 'POST'])
def process_video_speed(name_user, dir_video):
    coordinates = session.get('coordinates')

    x = float(coordinates['x'])
    y = float(coordinates['y'])
    x1 = float(coordinates['x1'])
    y1 = float(coordinates['y1'])
    x2 = float(coordinates['x2'])
    y2 = float(coordinates['y2'])
    x3 = float(coordinates['x3'])
    y3 = float(coordinates['y3'])

    return Response(gen_video_speed_test(name_user, dir_video, x, y, x1, y1, x2, y2, x3, y3, classes="5"),
                    mimetype='text/event-stream')
    # gen_video_speed_test(name_user,dir_video)
    # path_video=f'static/users/{name_user}/{dir_video}/video_speed/speed.mp4'
    # if os.path.isfile(path_video):
    #     return send_file(path_video, as_attachment=True)
    # else:
    #     return "Vui long kiem tra lại"


@app.route('/<name_user>/<dir_video>/process-video-2-short', methods=['GET', 'POST'])
def process_video_2short(name_user, dir_video):
    coordinates = session.get('coordinates')

    x = float(coordinates['x'])
    y = float(coordinates['y'])
    x1 = float(coordinates['x1'])
    y1 = float(coordinates['y1'])
    x2 = float(coordinates['x2'])
    y2 = float(coordinates['y2'])
    x3 = float(coordinates['x3'])
    y3 = float(coordinates['y3'])

    print("line1: ", x, y, x1, y1)
    print()

    return Response(gen_video_2lines(name_user, dir_video, x, y, x1, y1, x2, y2, x3, y3, classes="5"),
                    mimetype='text/event-stream')


@app.route('/<name_user>/<dir_video>/process-video-u-turn', methods=['GET', 'POST'])
def process_video_u_turn(name_user, dir_video):
    coordinates = session.get('coordinates')

    x = float(coordinates['x'])
    y = float(coordinates['y'])
    x1 = float(coordinates['x1'])
    y1 = float(coordinates['y1'])

    print("line1: ", x, y, x1, y1)
    print()

    return Response(gen_video_u_turn(name_user, dir_video, x, y, x1, y1, classes="5"), mimetype='text/event-stream')


@app.route('/<name_user>/<dir_video>/process-video-2-short-9class', methods=['GET', 'POST'])
def process_video_2short_9class(name_user, dir_video):
    coordinates = session.get('coordinates')

    x = float(coordinates['x'])
    y = float(coordinates['y'])
    x1 = float(coordinates['x1'])
    y1 = float(coordinates['y1'])
    x2 = float(coordinates['x2'])
    y2 = float(coordinates['y2'])
    x3 = float(coordinates['x3'])
    y3 = float(coordinates['y3'])

    print("line1: ", x, y, x1, y1)
    print()

    return Response(gen_video_2lines_9class(name_user, dir_video, x, y, x1, y1, x2, y2, x3, y3, classes="9"),
                    mimetype='text/event-stream')


@app.route("/<name_user>/<dir_video>/process-video-4-short", methods=['GET', 'POST'])
def process_video_4short(dir_video, name_user):
    # if request.method == "POST":
    print("alo1234")
    coordinates = session.get('coordinates')
    x = float(coordinates['x'])
    y = float(coordinates['y'])
    x1 = float(coordinates['x1'])
    y1 = float(coordinates['y1'])
    x2 = float(coordinates['x2'])
    y2 = float(coordinates['y2'])
    x3 = float(coordinates['x3'])
    y3 = float(coordinates['y3'])
    x4 = float(coordinates['x4'])
    y4 = float(coordinates['y4'])
    x5 = float(coordinates['x5'])
    y5 = float(coordinates['y5'])
    x6 = float(coordinates['x6'])
    y6 = float(coordinates['y6'])
    x7 = float(coordinates['x7'])
    y7 = float(coordinates['y7'])

    print("line 4 : ", x, y, x1, y1)

    name_video = get_project_name(dir_video)

    return Response(gen_video_count(dir_video, name_user, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7,
                                    name_video, classes="5"), mimetype='text/event-stream')


@app.route("/<name_user>/<dir_video>/processing-video-short-9classes", methods=['GET', 'POST'])
def process_video_4short_9classes(dir_video, name_user):
    # if request.method == "POST":
    print("alo1234")
    coordinates = session.get('coordinates')
    x = float(coordinates['x'])
    y = float(coordinates['y'])
    x1 = float(coordinates['x1'])
    y1 = float(coordinates['y1'])
    x2 = float(coordinates['x2'])
    y2 = float(coordinates['y2'])
    x3 = float(coordinates['x3'])
    y3 = float(coordinates['y3'])
    x4 = float(coordinates['x4'])
    y4 = float(coordinates['y4'])
    x5 = float(coordinates['x5'])
    y5 = float(coordinates['y5'])
    x6 = float(coordinates['x6'])
    y6 = float(coordinates['y6'])
    x7 = float(coordinates['x7'])
    y7 = float(coordinates['y7'])

    print("line 4 : ", x, y, x1, y1)

    name_video = get_project_name(dir_video)

    return Response(
        gen_video_count_9class(dir_video, name_user, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7,
                               name_video, classes="9"), mimetype='text/event-stream')


@app.route('/<name_user>/<dir_video>/processing-video', methods=['GET', 'POST'])
def process_video(name_user, dir_video):
    project_name = get_project_name(dir_video)

    x = request.form.get("x")
    y = request.form.get("y")
    x1 = request.form.get("x1")
    y1 = request.form.get("y1")
    x2 = request.form.get("x2")
    y2 = request.form.get("y2")
    x3 = request.form.get("x3")
    y3 = request.form.get("y3")
    x4 = request.form.get("x4")
    y4 = request.form.get("y4")
    x5 = request.form.get("x5")
    y5 = request.form.get("y5")
    x6 = request.form.get("x6")
    y6 = request.form.get("y6")
    x7 = request.form.get("x7")
    y7 = request.form.get("y7")
    task = request.form.get("task")

    print("line1: ", x, y, x1, y1, task)

    session['coordinates'] = {
        'x': x,
        'y': y,
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        'x3': x3,
        'y3': y3,
        'x4': x4,
        'y4': y4,
        'x5': x5,
        'y5': y5,
        'x6': x6,
        'y6': y6,
        'x7': x7,
        'y7': y7
    }

    return render_template('processing.html', name_user=name_user, project_name=project_name, dir_video=dir_video,
                           task=task)


@app.route('/<name_user>/<dir_video>/speed_bottom_v2/<num_class>', methods=['GET', 'POST'])
def verhical_speed_bottom_v2(name_user, dir_video, num_class):
    project_dir = f'static/users/{name_user}/{dir_video}'
    str_start_time, str_end_time, FPS = get_start_end_time(project_dir)

    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))

        i = 1
        mang1 = []
        list_toa_do = []
        list_distance = []

        while (request.form.get(f"A_{i}_1") and request.form.get(f"A_{i}_2")):
            a_1 = float(request.form.get(f"A_{i}_1"))
            b_1 = float(request.form.get(f"B_{i}_1"))
            a_2 = float(request.form.get(f"A_{i}_2"))
            b_2 = float(request.form.get(f"B_{i}_2"))
            distance = float(request.form.get(f"D{i}"))
            list_distance.append(distance)
            mang1.append(a_1)
            mang1.append(b_1)
            mang1.append(a_2)
            mang1.append(b_2)
            if len(mang1) == 4:
                list_toa_do.append(mang1)
                mang1 = []

            i += 1

        str_start_time = request.form.get("str_start_time")
        str_end_time = request.form.get("str_end_time")

        dir_path = f'static/users/{name_user}/{dir_video}'
        link_json_point = f'{dir_path}/data_point_{num_class}.json'
        # Opening JSON file
        f = open(link_json_point)
        # toa do 4 diem (2 lines lần lượt)
        data = json.load(f)
        a, b, a2, b2, x, y, x1, y1, x2, y2, x3, y3 = data_from_FE_hour(x, y, x1, y1, x2, y2, x3, y3)
        d1 = {}
        d2 = {}

        # dem theo giao diem
        for m in data.keys():
            cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
            cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)

        d = {0: d1, 1: d2}

        with open(f"{dir_path}/speed.json", "w") as outfile:
            json.dump(d, outfile)

        model = train_distance_model(list_locate=list_toa_do, list_D=list_distance)
        print(list_toa_do)
        print(list_distance)
        print("Trained model")
        print(type(str_start_time))

        speed_class_infor, speed_each_values = caculate_speed_v3_MEDIAN(user=name_user, projectID=dir_video,
                                                                 model=model,start_range=str_start_time,end_range=str_end_time,
                                                                 num_class=num_class, time_start_str=str_start_time,
                                                                 time_end_str=str_end_time, time_step=15, FPS=FPS)
        print(speed_class_infor, speed_each_values)
        list_vehicle = ["Motor", "Car", "Bus", "LGV", "HGV", "ALL"]
        if num_class==9:
            list_vehicle=["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV","ALL"]

        return render_template('draw_line_speed_v2.html', speed_class_infor=speed_class_infor,
                               speed_each_values=speed_each_values,
                               name_user=name_user, dir_video=dir_video, size_w=width, size_h=height,
                               file_path=dir_video, x0=x, y0=y, x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3,
                               num_class=num_class,
                               list_vehicle=list_vehicle, str_start_time=str_start_time, str_end_time=str_end_time)

    return render_template('draw_line_speed_v2.html', name_user=name_user, dir_video=dir_video, num_class=num_class,
                           size_w=width, size_h=height, str_start_time=str_start_time, str_end_time=str_end_time)


@app.route('/draw_line_u_turn/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy_u_turn(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))

        # time1 = str(request.form.get("time1"))
        # time2 = str(request.form.get("time2"))
        # start = str(request.form.get("start"))
        # end = str(request.form.get("end"))
        # numM = str(request.form.get("numM"))

        x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
        save_json_gen = f'static/users/{name_user}/{dir_video}'
        run_gen_json_u_turn(link_json_point, save_json_gen, x, y, x1, y1)

        link_json_linetoline = f'static/users/{name_user}/{dir_video}'
        u_turn_list = direct_detector_u_turn(link_json_linetoline)
        return render_template('draw_line_u_turn.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, num_class=num_class, u_turn_list=u_turn_list,
                               x0=x, y0=y, x1=x1, y1=y1)

    return render_template('draw_line_u_turn.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_class=num_class)


@app.route('/draw_line_u_turn_hour/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def getxy_u_turn_hour(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if check_project_numclass(dir_video, num_class):
        print(dir_video, num_class)
        return render_template("thanks.html", name_user=name_user)
    elif not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))

        time1 = str(request.form.get("time1"))
        time2 = str(request.form.get("time2"))
        start = str(request.form.get("start"))
        end = str(request.form.get("end"))
        numM = str(request.form.get("numM"))

        if check_time_range(start, end, time1, time2):
            list_time, list_frame = convert_time_lap_to_frame(time1, start, end, int(numM))

            x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
            link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
            save_json_gen = f'static/users/{name_user}/{dir_video}'
            run_gen_json_u_turn(link_json_point, save_json_gen, x, y, x1, y1)

            link_json_linetoline = f'static/users/{name_user}/{dir_video}/data_idlinetoline_u_turn.json'

            u_turn_list_ = out_from_idlinetoline_with_frame_u_turn(list_frame, link_json_linetoline)
            u_turn_lists = []
            for j in range(len(u_turn_list_.values())):
                u_turn_lists.append([int(num.strip()) for num in list(u_turn_list_.values())[j][1:-1].split(',')])
        else:
            list_time = ['check your input time'], [0, 0]
            u_turn_lists = [[0] * 9]

        if num_class == 5:
            return render_template('draw_line_hour_u_turn_time.html', name_user=name_user, dir_video=dir_video,
                                   size_w=width, size_h=height, num_class=num_class,
                                   u_turn_lists=enumerate(u_turn_lists), list_time=list_time,
                                   x0=x, y0=y, x1=x1, y1=y1, time1=time1, time2=time2, start=start, end=end, numM=numM)
        else:
            return render_template('draw_line_hour_u_turn_time_9.html', name_user=name_user, dir_video=dir_video,
                                   size_w=width, size_h=height, num_class=num_class,
                                   u_turn_lists=enumerate(u_turn_lists), list_time=list_time,
                                   x0=x, y0=y, x1=x1, y1=y1, time1=time1, time2=time2, start=start, end=end, numM=numM)
    return render_template('draw_line_hour_u_turn_time.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_class=num_class)


@app.route("/<name_user>/<dir_video>/download-video-4-short", methods=['GET', 'POST'])
def download_video_4short(dir_video, name_user):
    name_video = get_project_name(dir_video)
    file_path = f"static/users/{name_user}/{dir_video}/video_count_4lines/count5classes.mp4"
    return send_file(file_path, as_attachment=True)


@app.route("/<name_user>/<dir_video>/download-video-4-short-9classes", methods=['GET', 'POST'])
def download_video_4short_9classes(dir_video, name_user):
    name_video = get_project_name(dir_video)
    file_path = f"static/users/{name_user}/{dir_video}/video_count_4lines/count9classes.mp4"
    return send_file(file_path, as_attachment=True)


@app.route('/<name_user>/<dir_video>/download-video-2-short', methods=['GET', 'POST'])
def download_video_2short(name_user, dir_video):
    path_video = f'static/users/{name_user}/{dir_video}/video_speed/2short.mp4'
    if os.path.isfile(path_video):
        return send_file(path_video, as_attachment=True)
    else:
        return "Vui long kiem tra lại"


@app.route('/<name_user>/<dir_video>/download-video-u-turn', methods=['GET', 'POST'])
def download_video_u_turn(name_user, dir_video):
    path_video = f'static/users/{name_user}/{dir_video}/video_speed/u_turn.mp4'
    if os.path.isfile(path_video):
        return send_file(path_video, as_attachment=True)
    else:
        return "Vui long kiem tra lại"


@app.route('/<name_user>/<dir_video>/download-video-2-short-9class', methods=['GET', 'POST'])
def download_video_2short_9class(name_user, dir_video):
    path_video = f'static/users/{name_user}/{dir_video}/video_speed/2short_9class.mp4'
    if os.path.isfile(path_video):
        return send_file(path_video, as_attachment=True)
    else:
        return "Vui long kiem tra lại"


@app.route('/<name_user>/<dir_video>/download-video-speed')
def download_video_speed(name_user, dir_video):
    path_video = f'static/users/{name_user}/{dir_video}/video_speed/speed.mp4'
    if os.path.isfile(path_video):
        return send_file(path_video, as_attachment=True)
    else:
        return "Vui long kiem tra lại"


@app.route('/draw_area/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def draw_area_short(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height
    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        if check_project_numclass(dir_video, num_class):
            return render_template("wait.html")

        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))
        time_start = request.form.get("time1")
        dx = float(request.form.get("dx"))
        dy = float(request.form.get("dy"))
        dx1 = float(request.form.get("dx1"))
        dy1 = float(request.form.get("dy1"))
        dx2 = float(request.form.get("dx2"))
        dy2 = float(request.form.get("dy2"))
        dx3 = float(request.form.get("dx3"))
        dy3 = float(request.form.get("dy3"))
        dx4 = float(request.form.get("dx4"))
        dy4 = float(request.form.get("dy4"))
        dx5 = float(request.form.get("dx5"))
        dy5 = float(request.form.get("dy5"))


        #distance of 3 doan (m)
        distance_u = int(request.form.get("limit_distance"))
        list_toa_do = [[dx,dy,dx1,dy1],[dx2,dy2,dx3,dy3],[dx4,dy4,dx5,dy5]]
        print(list_toa_do)
        numFrame=int(request.form.get("numFrame"))
        limit_distance = getMeanDistance(list_toa_do, distance_u)/numFrame
        # max_frame = int(request.form.get("max_frame"))*30
        max_frame = 5*30

        print(time_start, 1, limit_distance, max_frame)
        print(x, y, x1, y1, x2, y2, x3, y3)
        print(type(x), type(y))

        # x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
        # x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)

        link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
        path_ex_allDwellTime = f'static/users/{name_user}/{dir_video}/excel_file/'
        if not os.path.exists(path_ex_allDwellTime):
            os.mkdir(path_ex_allDwellTime)

        polygon = [(int(x), int(y)), (int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3))]  #
        #time check stop (frame)
        num_frame = int(30)
        print(f"input: {polygon} {link_json_point} {num_frame} {limit_distance} {max_frame}")
        all_, max_f = check_id_in_area_well_time(polygon, link_json_point, num_frame, limit_distance, max_frame)

        time_start_video = time_start  #
        df_all = xuat_excel_all_dwelltime(all_, time_start_video, path_ex_allDwellTime,num_class)
        df_max = write_max_val(max_f, time_start_video, path_ex_allDwellTime,num_class)
        output_file_path = path_ex_allDwellTime + 'DWELL_TIME.xlsx'

        with pd.ExcelWriter(output_file_path) as writer:
            df_all.to_excel(writer, sheet_name='Sheet_ALL', index=False)
            df_max.to_excel(writer, sheet_name='Sheet_MAX', index=False)

        return render_template('draw_area_5.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, x0=x, y0=y,
                               x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, num_class=num_class, numFrame=numFrame,
                               time1=time_start, distance_u=distance_u, max_frame=int(max_frame/30))
    return render_template('draw_area_5.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_class=num_class)


######################################################################

@app.route('/<name_user>/<dir_video>/download-dwell-time')
def download_DWELL_TIME(name_user, dir_video):

    path_excel = f'static/users/{name_user}/{dir_video}/excel_file/DWELL_TIME.xlsx'
    print(path_excel)
    if os.path.isfile(path_excel):
        return send_file(path_excel, as_attachment=True)
    else:
        return "Vui long kiem tra lại"

#####################################################################

@app.route('/draw_area_q_lenght/<name_user>/<dir_video>/<num_class>', methods=['GET', 'POST'])
def draw_area_q_lenght_short(dir_video, name_user, num_class):
    num_class = int(num_class)
    draw_img_path = f'static/users/{name_user}/{dir_video}/line_road_{num_class}.jpg'
    if not Path(draw_img_path).exists():
        print("Khong co File")
        return redirect(url_for("reprocess_video", username=name_user, project=dir_video, num_class=num_class))
    img = Image.open(draw_img_path)
    width = img.width
    height = img.height

    print("Day la GET")
    if request.method == "POST":
        # Neu project dang xu li thi -> sang page waiting
        if check_project_numclass(dir_video, num_class):
            return render_template("wait.html")

        # Chuyen sang page dem line
        print("Day la POST")
        x = float(request.form.get("x"))
        y = float(request.form.get("y"))
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        x3 = float(request.form.get("x3"))
        y3 = float(request.form.get("y3"))
        x4 = float(request.form.get("x4"))
        y4 = float(request.form.get("y4"))
        x5 = float(request.form.get("x5"))
        y5 = float(request.form.get("y5"))
        x6 = float(request.form.get("x6"))
        y6 = float(request.form.get("y6"))
        x7 = float(request.form.get("x7"))
        y7 = float(request.form.get("y7"))
        time_start = request.form.get("time1")
        print(time_start, type(time_start))
        numFrame = int(request.form.get("numFrame"))
        limit_distance = int(request.form.get("limit_distance"))

        print(time_start, numFrame, limit_distance)
        print(x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7)
        print(type(x), type(y))

        link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
        f1 = open(link_json_point)
        data = json.load(f1)
        list_verhicle = list(data.keys())

        # path_ex_allDwellTime = f'static/users/{name_user}/{dir_video}/'

        big_zone = [(int(x), int(y)), (int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3))]
        small_zone = [(int(x4), int(y4)), (int(x5), int(y5)), (int(x6), int(y6)), (int(x7), int(y7))]
        # big_zone = [(788, 782), (1888, 571), (1893, 641), (956, 1077)]
        # small_zone = [(965, 1077), (788, 782), (1200, 700), (1270, 938)]
        limit_sec = 5
        FPS = 30

        quences = caculate_quences(big_zone=big_zone, small_zone=small_zone, limit_sec=limit_sec, FPS=FPS, data=data,
                                   list_verhicle=list_verhicle)

        excel_quence = []

        start_time = str(time_start)
        for key in quences:
            abc = quence_to_excel_form(quences[key], id_=key, start_time=start_time, data=data, num_class=num_class)
            excel_quence.append(abc)
            print(abc)

        # Save result to excel file
        df = pd.DataFrame(excel_quence)
        path_ex = f'static/users/{name_user}/{dir_video}/excel_file/'
        if not os.path.exists(path_ex):
            os.mkdir(path_ex)
        excel_filename = path_ex+'quence-length.xlsx'
        sheet_name = 'quence-length'
        excel_writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
        df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
        excel_writer.save()
        print(f"Data saved to {excel_filename} with multiple sheets.")

        return render_template('draw_area_q_lenght_5.html', name_user=name_user, dir_video=dir_video,
                               size_w=width, size_h=height, x0=x, y0=y,
                               x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, num_class=num_class, numFrame=numFrame,
                               time1=time_start, limit_distance=limit_distance)

    return render_template('draw_area_q_lenght_5.html', name_user=name_user, dir_video=dir_video,
                           size_w=width, size_h=height, num_class=num_class)

######################################################################
@app.route('/<name_user>/<dir_video>/download-excel-q-lenght')
def download_excel_q_lenght(name_user, dir_video):
    path_excel = f'static/users/{name_user}/{dir_video}/excel_file/quence-length.xlsx'
    if os.path.isfile(path_excel):
        return send_file(path_excel, as_attachment=True)
    else:
        return "Vui long kiem tra lại"
######################################################################

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)

