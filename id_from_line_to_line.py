import json
import statistics
from new_define_class_method import class_of_id

from utils import check_time_range


def ptduongthang(ix,iy,a,b,c):
    pt=iy-a*ix-b-c
    return pt

def ptduongvuonggoc(x_u,y_u,a,x_x,y_x):
    c=y_u+(1/a)*x_u
    hsvg=-y_x-(1/a)*x_x+c
    return hsvg

def check_oj_in_area(a_pt,b_pt,ix_pt,iy_pt,x_d_pt,y_d_pt,x_u_pt,y_u_pt,d_line, index, id, frame_id):
    if (0 < ptduongthang(ix_pt, iy_pt, a_pt, b_pt, -15)) and (0 > ptduongthang(ix_pt, iy_pt, a_pt, b_pt, 0)) and (
            0 > ptduongvuonggoc(x_u_pt, y_u_pt, a_pt, ix_pt, iy_pt)) and (0 < ptduongvuonggoc(x_d_pt, y_d_pt, a_pt, ix_pt, iy_pt)):
        if id not in d_line:
            d_line[id] = [index, frame_id]
            # print("if 1")

    elif (0 > ptduongthang(ix_pt, iy_pt, a_pt, b_pt, 15)) and (0 < ptduongthang(ix_pt, iy_pt, a_pt, b_pt, 0)) and (
            0 > ptduongvuonggoc(x_u_pt, y_u_pt, a_pt, ix_pt, iy_pt)) and (0 < ptduongvuonggoc(x_d_pt, y_d_pt, a_pt, ix_pt, iy_pt)):
        if id not in d_line:
            d_line[id] = [index, frame_id]
            # print("if 2")

def find_point_up_down(x1, y1, x2, y2):
    if y1>y2:
        return x1, y1, x2, y2
    elif y1<y2:
        return x2, y2, x1, y1
    elif y1==y2:
        if x1<x2:
            return x1, y1, x2, y2
        else:
            return x2, y2, x1, y1
    return x1, y1, x2, y2

def data_from_FE(x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7):
  x,y,x1,y1=find_point_up_down(x,y,x1,y1)
  x2,y2,x3,y3=find_point_up_down(x2,y2,x3,y3)
  x4, y4, x5, y5 = find_point_up_down(x4, y4, x5, y5)
  x6, y6, x7, y7 = find_point_up_down(x6, y6, x7, y7)

  a=(y-y1)/(x-x1)
  b=y-a*x

  a2 = (y2 - y3) / (x2 - x3)
  b2 = y2 - a2 * x2

  a3 = (y4 - y5) / (x4 - x5)
  b3 = y4 - a3 * x4

  a4 = (y6 - y7) / (x6 - x7)
  b4 = y6 - a4 * x6
  return a,b,a2,b2,a3,b3,a4,b4,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7

def data_from_FE_hour(x,y,x1,y1,x2,y2,x3,y3):
  x,y,x1,y1=find_point_up_down(x,y,x1,y1)
  x2,y2,x3,y3=find_point_up_down(x2,y2,x3,y3)

  a=(y-y1)/(x-x1)
  b=y-a*x

  a2 = (y2 - y3) / (x2 - x3)
  b2 = y2 - a2 * x2


  return a,b,a2,b2,x,y,x1,y1,x2,y2,x3,y3

def giaodiem(x, y, x1, y1, x2, y2, x3, y3):
    if (x != x1 and x2 != x3):
        a = (y - y1) / (x - x1)
        b = y - a * x
        a2 = (y2 - y3) / (x2 - x3)
        b2 = y2 - a2 * x2
        if a != a2:
            x_g = (-b + b2) / (a - a2)
            y_g = a * x_g + b
            if (min(x,x1)<=x_g<=max(x,x1) and min(x2,x3)<=x_g<=max(x2,x3) and min(y,y1)<=y_g<=max(y,y1) and min(y2,y3)<=y_g<=max(y2,y3)):
                return 1
            else:
                return 0
        else:
            return 0
    else:
        if x == x1 and x2 != x3:
            a2 = (y2 - y3) / (x2 - x3)
            b2 = y2 - a2 * x2
            if (min(y, y1) <= a2*x+b2 <= max(y, y1) and min(y2, y3) <= a2*x+b2 <= max(y2, y3)):
                return 1
        if x != x1 and x2 == x3:
            a = (y - y1) / (x - x1)
            b = y - a * x
            if (min(y, y1) <= a * x2 + b <= max(y, y1) and min(y2, y3) <= a * x2 + b <= max(y2, y3)):
                return 1
        return 0

# def giaodiem(x, y, x1, y1, x2, y2, x3, y3):
#     return intersect((x,y),(x1,y1),(x2,y2),(x3,y3))

# def intersect(A,B,C,D):
#     if ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D):
#         return 1
#     else:
#         return 0
#
# def ccw(A,B,C):
#     return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
    # AB cắt CD tại đầu các đoạn.
    if A==C or A==D:
        return 1
    if B==C or B==D:
        return 1
    # AB có cắt CD không.
    ## Xoay khác chiều.
    if ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D):
        return 1
    return 0

def ccw(A, B, C):
    '''
    kiểm tra điều kiện có cắt hay không.
    nếu ccw > 0 (True) thì là quay xuôi chiều
    nếu ccw < 0 (False) thì là quay ngược chiều
    nếu ccw = 0 thì 3 điểm thẳng hàng
    '''
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def vecto(x_start, y_start, x_end, y_end):
    a = 1 if x_end>x_start else 0
    b = 1 if y_end > y_start else 0

    return [a, b]

def vector_viet(x_start, y_start, x_end, y_end):
    a = x_start - x_end
    b = y_start - y_end

    return [a, b]

def cat_d(x_d,y_d,x1_d,y1_d,random_list,d_line,index,id):
  for t in range(len(random_list)-1):
    # if giaodiem(x_d,y_d,x1_d,y1_d,random_list[t][0],random_list[t][1],random_list[t+1][0],random_list[t+1][1])==1:
    if intersect([x_d,y_d],[x1_d,y1_d],[random_list[t][0],random_list[t][1]],[random_list[t+1][0],random_list[t+1][1]])==1:
    #   print(id," : " ,random_list[t][2],[random_list[t][0],random_list[t][1]])
      if id == "117":
          print("cat")
      if id not in d_line:
        d_line[id] = [index, random_list[t][2],[random_list[t][0],random_list[t][1]]]
    else:
      continue

def cat_d_u_turn(x_d,y_d,x1_d,y1_d,u_turn, d_line,random_list,index,id):

    for t in range(len(random_list)-1):
        if giaodiem(x_d,y_d,x1_d,y1_d,random_list[t][0],random_list[t][1],random_list[t+1][0],random_list[t+1][1])==1:
        # if intersect([x_d, y_d], [x1_d, y1_d], [random_list[t][0], random_list[t][1]], [random_list[t + 1][0], random_list[t + 1][1]]) == 1:
            # print("CUT: ",id)
            if id in d_line:
                # print("Hello")
                u_turn[id] = [index, random_list[t][2],[random_list[t][0],random_list[t][1]]]
                # print(u_turn)
            if id not in d_line:
                # print("d_line" ,id)
                d_line[id] = [index, random_list[t][2],[random_list[t][0],random_list[t][1]]]
        else:
          continue

def run_gen_json(link_json_point,save_json_gen,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7, x_start, y_start, x_end, y_end):
    # Opening JSON file
    f = open(link_json_point)
    # toa do 4 diem (2 lines lần lượt)
    data = json.load(f)

    vecto_goc = vector_viet(x_start, y_start, x_end, y_end)
    print(f"veco goc: {vecto_goc}")

    for id in list(data.keys()):
        x_point_start, y_point_start = data[id]["frame"][0][:2]
        x_point_end, y_point_end = data[id]["frame"][-1][:2]
        id_vecto = vector_viet(x_point_start, y_point_start, x_point_end, y_point_end)

        # print(f"id: {id} | vecto: {str(id_vecto)}")
        if (vecto_goc[0]*id_vecto[0]+vecto_goc[1]*id_vecto[1]) > 0:
            pass
        else:
            if id in data.keys():
                data.pop(id)
    a,b,a2,b2,a3,b3,a4,b4,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7=data_from_FE(x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7)
    d1={}
    d2={}
    d3={}
    d4={}

    # dem theo giao diem
    for m in data.keys():
        cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
        cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)
        cat_d(x4, y4, x5, y5, data[m]['H20_center'], d3, int(statistics.median(data[m]['cls'])), m)
        cat_d(x6, y6, x7, y7, data[m]['H20_center'], d4, int(statistics.median(data[m]['cls'])), m)

    d={0:d1,1:d2,2:d3,3:d4}

    with open(f"{save_json_gen}/data_idlinetoline_d.json", "w") as outfile:
        json.dump(d, outfile)

def run_gen_json_hour(link_json_point,save_json_gen,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x_start, y_start, x_end, y_end):
    f = open(link_json_point)
    # toa do 4 diem (2 lines lần lượt)
    data = json.load(f)

    vecto_goc = vector_viet(x_start, y_start, x_end, y_end)
    print(f"veco goc: {vecto_goc}")

    for id in list(data.keys()):
        x_point_start, y_point_start = data[id]["frame"][0][:2]
        x_point_end, y_point_end = data[id]["frame"][-1][:2]
        id_vecto = vector_viet(x_point_start, y_point_start, x_point_end, y_point_end)

        # print(f"id: {id} | vecto: {str(id_vecto)}")
        if (vecto_goc[0] * id_vecto[0] + vecto_goc[1] * id_vecto[1]) > 0:
            pass
        else:
            if id in data.keys():
                data.pop(id)
    a, b, a2, b2, a3, b3, a4, b4, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7=data_from_FE(x, y, x1,
                                                                                                              y1, x2,
                                                                                                              y2, x3,
                                                                                                              y3, x4,
                                                                                                              y4, x5,
                                                                                                              y5, x6,
                                                                                                              y6, x7,
                                                                                                              y7)
    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}
    # dem theo mang
    # for m in data.keys():
    #   for n in data[m]['H20_center']:
    #
    #     check_oj_in_area(a , b, n[0], n[1], x, y, x1, y1, d1, int(statistics.median(data[m]['cls'])), m, n[2])
    #     check_oj_in_area(a2, b2, n[0], n[1], x2, y2, x3, y3, d2, int(statistics.median(data[m]['cls'])), m, n[2])

    # dem theo giao diem
    for m in data.keys():
        cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
        cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)
        cat_d(x4, y4, x5, y5, data[m]['H20_center'], d3, int(statistics.median(data[m]['cls'])), m)
        cat_d(x6, y6, x7, y7, data[m]['H20_center'], d4, int(statistics.median(data[m]['cls'])), m)

    d={0:d1,1:d2,2:d3,3:d4}

    with open(f"{save_json_gen}/data_idlinetoline_d_hour.json", "w") as outfile:
        json.dump(d, outfile)

def run_gen_json_hour_2(link_json_point,save_json_gen,x,y,x1,y1,x2,y2,x3,y3):
    # Opening JSON file
    f = open(link_json_point)
    # toa do 4 diem (2 lines lần lượt)
    data = json.load(f)
    a,b,a2,b2,x,y,x1,y1,x2,y2,x3,y3=data_from_FE_hour(x,y,x1,y1,x2,y2,x3,y3)
    d1={}
    d2={}
    # dem theo mang
    # for m in data.keys():
    #   for n in data[m]['H20_center']:
    #
    #     check_oj_in_area(a , b, n[0], n[1], x, y, x1, y1, d1, int(statistics.median(data[m]['cls'])), m, n[2])
    #     check_oj_in_area(a2, b2, n[0], n[1], x2, y2, x3, y3, d2, int(statistics.median(data[m]['cls'])), m, n[2])

    # dem theo giao diem
    for m in data.keys():
        # cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
        # cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)
        cat_d(x, y, x1, y1, data[m]['H20_center'], d1, class_of_id(id=m, data=data), m)
        cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, class_of_id(id=m, data=data), m)

    d={0:d1,1:d2}

    with open(f"{save_json_gen}/data_idlinetoline_d_hour.json", "w") as outfile:
        json.dump(d, outfile)

def run_gen_json_u_turn(link_json_point,save_json_gen,x,y,x1,y1):
    # Opening JSON file
    f = open(link_json_point)
    # toa do 4 diem (2 lines lần lượt)
    data = json.load(f)
    a,b,_,_,x,y,x1,y1,_,_,_,_=data_from_FE_hour(x,y,x1,y1,1,2,3,4)
    # dem theo mang
    # for m in data.keys():
    #   for n in data[m]['H20_center']:
    #
    #     check_oj_in_area(a , b, n[0], n[1], x, y, x1, y1, d1, int(statistics.median(data[m]['cls'])), m, n[2])
    #     check_oj_in_area(a2, b2, n[0], n[1], x2, y2, x3, y3, d2, int(statistics.median(data[m]['cls'])), m, n[2])

    # dem theo giao diem
    d_line = {}
    u_turn = {}
    for m in data.keys():
        cat_d_u_turn(x, y, x1, y1,u_turn, d_line, data[m]['H20_center'], int(statistics.median(data[m]['cls'])), m)
    print(u_turn)
    with open(f"{save_json_gen}/data_idlinetoline_u_turn.json", "w") as outfile:
        json.dump(u_turn, outfile)

def run_gen_json_speed(link_json_point,save_json_gen,x,y,x1,y1,x2,y2,x3,y3):
    # Opening JSON file
    f = open(link_json_point)
    # toa do 4 diem (2 lines lần lượt)
    data = json.load(f)
    a,b,a2,b2,x,y,x1,y1,x2,y2,x3,y3=data_from_FE_hour(x,y,x1,y1,x2,y2,x3,y3)
    d1={}
    d2={}
    # dem theo mang
    # for m in data.keys():
    #   for n in data[m]['H20_center']:
    #
    #     check_oj_in_area(a , b, n[0], n[1], x, y, x1, y1, d1, int(statistics.median(data[m]['cls'])), m, n[2])
    #     check_oj_in_area(a2, b2, n[0], n[1], x2, y2, x3, y3, d2, int(statistics.median(data[m]['cls'])), m, n[2])

    # dem theo giao diem
    for m in data.keys():
        cat_d(x, y, x1, y1, data[m]['H20_center'], d1, int(statistics.median(data[m]['cls'])), m)
        cat_d(x2, y2, x3, y3, data[m]['H20_center'], d2, int(statistics.median(data[m]['cls'])), m)

    d={0:d1,1:d2}

    with open(f"{save_json_gen}/speed.json", "w") as outfile:
        json.dump(d, outfile)

def out_from_idlinetoline_with_frame(frames_,link_json_linetoline):
    f = open(link_json_linetoline)
    data = json.load(f)
    dict_0 = {}
    for j in frames_:
        list_veco = [0] * 9
        for i in data['0'].keys():
            if j[0] <= data['0'][i][1] <= j[1]:
                list_veco[data['0'][i][0]] += 1
        dict_0[str(j)] = str(list_veco)

    dict_1 = {}
    for j in frames_:
        list_veco = [0] * 9
        for i in data['1'].keys():
            if j[0] <= data['1'][i][1] <= j[1]:
                list_veco[data['1'][i][0]] += 1
        dict_1[str(j)] = str(list_veco)

    dict_2 = {}
    for j in frames_:
        list_veco = [0] * 9
        for i in data['2'].keys():
            if j[0] <= data['2'][i][1] <= j[1]:
                list_veco[data['2'][i][0]] += 1
        dict_2[str(j)] = str(list_veco)

    dict_3 = {}
    for j in frames_:
        list_veco = [0] * 9
        for i in data['3'].keys():
            if j[0] <= data['3'][i][1] <= j[1]:
                list_veco[data['3'][i][0]] += 1
        dict_3[str(j)] = str(list_veco)
    return dict_0, dict_1, dict_2, dict_3

def out_from_idlinetoline_with_frame_u_turn(frames_,link_json_linetoline):
    f = open(link_json_linetoline)
    data = json.load(f)
    dict_0 = {}
    for j in frames_:
        list_veco = [0] * 9
        for i in data.keys():
            if j[0] <= data[i][1] <= j[1]:
                list_veco[data[i][0]] += 1
        dict_0[str(j)] = str(list_veco)
    return dict_0

def out_from_idlinetoline_with_frame_2(frames_,link_json_linetoline):
    f = open(link_json_linetoline)
    data = json.load(f)
    dict_0={}
    for j in frames_:
        list_veco = [0] * 9
        for i in data['0'].keys():
            if j[0]<=data['0'][i][1]<=j[1]:
                list_veco[data['0'][i][0]] += 1
        dict_0[str(j)]=str(list_veco)

    dict_1={}
    for j in frames_:
        list_veco = [0] * 9
        for i in data['1'].keys():
            if j[0]<=data['1'][i][1]<=j[1]:
                list_veco[data['1'][i][0]] += 1
        dict_1[str(j)]=str(list_veco)

    return dict_0,dict_1

def json_speed(x,y, x1, y1, x2, y2, x3, y3, name_user, dir_video, num_class):
    x, y, x1, y1 = find_point_up_down(x, y, x1, y1)
    x2, y2, x3, y3 = find_point_up_down(x2, y2, x3, y3)

    link_json_point = f'static/users/{name_user}/{dir_video}/data_point_{num_class}.json'
    save_json_gen = f'static/users/{name_user}/{dir_video}'
    run_gen_json_speed(link_json_point, save_json_gen, x, y, x1, y1, x2, y2, x3, y3)

    link_json_linetoline = f'static/users/{name_user}/{dir_video}/speed.json'