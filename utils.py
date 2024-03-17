import json
import statistics
import os
import datetime
import math

def find_common_elements(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    common_elements = list(set1.intersection(set2))
    return common_elements

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def find_center(xyxy):
    x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
    cx = (x2 + x1) / 2
    cy = (y2 + y1) / 2
    return int(cx), int(cy)

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

# Opening JSON file
# f = open('data_point.json')
# toa do 4 diem (2 lines lần lượt)
# x,y,x1,y1,x2,y2,x3,y3=224.5,854,624.5,546,387.5,1079,1047.5,636
# data = json.load(f)

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
            print("if 1")

    elif (0 > ptduongthang(ix_pt, iy_pt, a_pt, b_pt, 15)) and (0 < ptduongthang(ix_pt, iy_pt, a_pt, b_pt, 0)) and (
            0 > ptduongvuonggoc(x_u_pt, y_u_pt, a_pt, ix_pt, iy_pt)) and (0 < ptduongvuonggoc(x_d_pt, y_d_pt, a_pt, ix_pt, iy_pt)):
        if id not in d_line:
            d_line[id] = [index, frame_id]
            print("if 2")

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

def data_from_FE(x, y, x1 ,y1, x2, y2, x3, y3):
  x,y,x1,y1=find_point_up_down(x,y,x1,y1)
  x2,y2,x3,y3=find_point_up_down(x2,y2,x3,y3)

  a=(y-y1)/(x-x1)
  b=y-a*x

  a2 = (y2 - y3) / (x2 - x3)
  b2 = y2 - a2 * x2
  return a,b,a2,b2,x,y,x1,y1,x2,y2,x3,y3

# a,b,a2,b2,x,y,x1,y1,x2,y2,x3,y3=data_from_FE(x,y,x1,y1,x2,y2,x3,y3)
# d1={}
# d2={}
#
# for m in data.keys():
#   for n in data[m]['H20_center']:
#     check_oj_in_area(a , b, n[0], n[1], x, y, x1, y1, d1, int(statistics.median(data[m]['cls'])), m, n[2])
#     check_oj_in_area(a2, b2, n[0], n[1], x2, y2, x3, y3, d2, int(statistics.median(data[m]['cls'])), m, n[2])
#
# d={0:d1,1:d2}
#
# with open("data_idlinetoline_d_line120230330.json", "w") as outfile:
#     json.dump(d, outfile)
def most_frequent_element(list1):
    return max(set(list1), key=list1.count)



def out_from_idlinetoline_with_frame(frames_,link_json_linetoline):
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

def between(A, B, C):
    # C nằm giữa AB.
    return min(A[0], B[0]) <= C[0] and C[0] <= max(A[0], B[0]) and min(A[1], B[1]) <= C[1] and C[1] <= max(A[1], B[1])

def giaodiem(x, y, x1, y1, x2, y2, x3, y3):
  if (x!=x1 and x2!=x3):
    a=(y-y1)/(x-x1)
    b=y-a*x
    # print(a,b)
    a2 = (y2 - y3) / (x2 - x3)
    b2 = y2 - a2 * x2
    # print(a2,b2)
    if a!=a2:
      x_g = (-b+b2)/(a-a2)
      y_g = a*x_g + b
      if (min(x,x1)<=x_g<=max(x,x1) and min(x2,x3)<=x_g<=max(x2,x3) and min(y,y1)<=y_g<=max(y,y1) and min(y2,y3)<=y_g<=max(y2,y3)):
        # print("nam trong doan")
        return 1
      else:
        # print("nam ngoai doan")
        return 0
    else:
      if x == x1 and x2 != x3:
          a2 = (y2 - y3) / (x2 - x3)
          b2 = y2 - a2 * x2
          if (min(y, y1) <= a2 * x + b2 <= max(y, y1) and min(y2, y3) <= a2 * x + b2 <= max(y2, y3)):
              return 1
      if x != x1 and x2 == x3:
          a = (y - y1) / (x - x1)
          b = y - a * x
          if (min(y, y1) <= a * x2 + b <= max(y, y1) and min(y2, y3) <= a * x2 + b <= max(y2, y3)):
              return 1
      return 0
  return 0
def cat_d(x_d,y_d,x1_d,y1_d,random_list,d_line,index,id):
  for t in range(len(random_list)-1):
    # if giaodiem(x_d,y_d,x1_d,y1_d,random_list[t][0],random_list[t][1],random_list[t+1][0],random_list[t+1][1])==1:
    if intersect([x_d,y_d],[x1_d,y1_d],[random_list[t][0],random_list[t][1]],[random_list[t+1][0],random_list[t+1][1]])==1:
        # print("cat")
      # print(random_list[t][2])
      # if id not in d_line and int(random_list[t][2])<=327720 and int(random_list[t][2])>=300720:
      if id not in d_line:
        # d_line[id] = [index, random_list[t][2]]
        d_line[id] = [index, random_list[t][2], [random_list[t][0], random_list[t][1]]]
        # print("dline")
    else:
      continue

def vector_viet(x_start, y_start, x_end, y_end):
    a = x_start - x_end
    b = y_start - y_end

    return [a, b]

def run_gen_json(link_json_point,save_json_gen,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x_start, y_start, x_end, y_end):
    # Opening JSON file
    f = open(link_json_point)
    # toa do 4 diem (2 lines lần lượt)
    data = json.load(f)
    vecto_goc = vector_viet(x_start, y_start, x_end, y_end)
    print(f"veco goc: {vecto_goc}")

    for id in list(data.keys()):
        num_frame_id = len(data[id]["frame"])
        middle_point = int(num_frame_id / 2)
        # Neu diem o giua = 0 thi lay diem dau va diem cuoi
        x_point_start, y_point_start = data[id]["frame"][0][:2]
        if not middle_point:
            x_point_end, y_point_end = data[id]["frame"][-1][:2]
        else:
            x_point_end, y_point_end = data[id]["frame"][middle_point][:2]
        id_vecto = vector_viet(x_point_start, y_point_start, x_point_end, y_point_end)

        # print(f"id: {id} | vecto: {str(id_vecto)}")
        if (vecto_goc[0] * id_vecto[0] + vecto_goc[1] * id_vecto[1]) > 0:
            pass
        else:
            if id in data.keys():
                data.pop(id)
    a,b,a2,b2,a3,b3,a4,b4,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7=data_from_FE(x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7)
    d1={}
    d2={}
    d3={}
    d4={}
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

    with open(f"{save_json_gen}/data_idlinetoline_d.json", "w") as outfile:
        json.dump(d, outfile)

def run_gen_json_hour(link_json_point,save_json_gen,x,y,x1,y1,x2,y2,x3,y3):
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

    with open(f"{save_json_gen}/data_idlinetoline_d_hour.json", "w") as outfile:
        json.dump(d, outfile)

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

def direct_detector(dir_path,name_user):
    f = open(f'{dir_path}/data_idlinetoline_d.json', "r", encoding='utf-8')
    data = json.load(f)
    f.close()

    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0

    for j in data['0'].keys():
        # print(j[])
        if data['0'][j][0] == 0:
            count0 += 1
        elif data['0'][j][0] == 1:
            count1 += 1
        elif data['0'][j][0] == 2:
            count2 += 1
        elif data['0'][j][0] == 3:
            count3 += 1
        elif data['0'][j][0] == 4:
            count4 += 1
        elif data['0'][j][0] == 5:
            count5 += 1
        elif data['0'][j][0] == 6:
            count6 += 1
        elif data['0'][j][0] == 7:
            count7 += 1
        elif data['0'][j][0] == 8:
            count8 += 1

    d1 = [count0, count1, count2, count3, count4, count5, count6, count7, count8]

    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0

    for j in data['1'].keys():
        # print(j[])
        if data['1'][j][0] == 0:
            count0 += 1
        elif data['1'][j][0] == 1:
            count1 += 1
        elif data['1'][j][0] == 2:
            count2 += 1
        elif data['1'][j][0] == 3:
            count3 += 1
        elif data['1'][j][0] == 4:
            count4 += 1
        elif data['1'][j][0] == 5:
            count5 += 1
        elif data['1'][j][0] == 6:
            count6 += 1
        elif data['1'][j][0] == 7:
            count7 += 1
        elif data['1'][j][0] == 8:
            count8 += 1

    d2 = [count0, count1, count2, count3, count4, count5, count6, count7, count8]

    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0

    for j in data['2'].keys():
        # print(j[])
        if data['2'][j][0] == 0:
            count0 += 1
        elif data['2'][j][0] == 1:
            count1 += 1
        elif data['2'][j][0] == 2:
            count2 += 1
        elif data['2'][j][0] == 3:
            count3 += 1
        elif data['2'][j][0] == 4:
            count4 += 1
        elif data['2'][j][0] == 5:
            count5 += 1
        elif data['2'][j][0] == 6:
            count6 += 1
        elif data['2'][j][0] == 7:
            count7 += 1
        elif data['2'][j][0] == 8:
            count8 += 1
    d3 = [count0, count1, count2, count3, count4, count5, count6, count7, count8]

    count0 = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0

    for j in data['3'].keys():
        # print(j[])
        if data['3'][j][0] == 0:
            count0 += 1
        elif data['3'][j][0] == 1:
            count1 += 1
        elif data['3'][j][0] == 2:
            count2 += 1
        elif data['3'][j][0] == 3:
            count3 += 1
        elif data['3'][j][0] == 4:
            count4 += 1
        elif data['3'][j][0] == 5:
            count5 += 1
        elif data['3'][j][0] == 6:
            count6 += 1
        elif data['3'][j][0] == 7:
            count7 += 1
        elif data['3'][j][0] == 8:
            count8 += 1
    d4 = [count0, count1, count2, count3, count4, count5, count6, count7, count8]
    directions={'d1':d1,'d2':d2,'d3':d3,'d4':d4}



    with open(f"{dir_path}/result.json", "w") as outfile:
        json.dump(directions, outfile)

    return d1, d2, d3, d4


def check_time_range(a, b, c, d):
    a = datetime.datetime.strptime(a, '%H:%M') # thời gian nhập tay start
    b = datetime.datetime.strptime(b, '%H:%M') # thời gian nhập tay end
    c = datetime.datetime.strptime(c, '%H:%M:%S') # thời gian bắt đầu của video đầu tiên
    d = datetime.datetime.strptime(d, '%H:%M:%S') # thời gian kết thúc của video cuối cùng
    if c <= a <= d and c <= b <= d:
        return True
    else:
        return False

#trả về số giây, frame tính từ video đầu tiên đến thời gian bắt đầu mong muốn
def time_diff_frames(a, c):
    a_time = datetime.datetime.strptime(a, '%H:%M') # thời gian nhập tay start
    c_time = datetime.datetime.strptime(c, '%H:%M:%S') # thời gian bắt đầu của video đầu tiên

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

def direct_detector_u_turn(dir_path):
    f = open(f'{dir_path}/data_idlinetoline_u_turn.json', "r", encoding='utf-8')
    data = json.load(f)
    f.close()

    ids = list(data.keys())
    u_turn_list = [0]*5
    for id in ids:
        cls = data[id][0]
        u_turn_list[cls] += 1
    return u_turn_list

def run_gen_json_hour(link_json_point,save_json_gen,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7):
    # Opening JSON file
    f = open(link_json_point)
    # toa do 4 diem (2 lines lần lượt)
    data = json.load(f)
    a, b, a2, b2, a3, b3, a4, b4, x, y, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7 = data_from_FE(x, y, x1,
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

def out_from_idlinetoline_with_frame(frames_,link_json_linetoline):
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
    return dict_0,dict_1,dict_2,dict_3


def direct_detector_2short(dir_path):
    f = open(f'{dir_path}/data_idlinetoline_d_hour.json', "r", encoding='utf-8')
    data = json.load(f)
    f.close()

    # lines = list(data.keys())
    # num_line = len(lines)
    #
    # dul = {}
    #
    # # dul = set(data[0]) & set(data[1])
    #
    # count = 0
    # for i in range (0, num_line-1):
    #     for j in range(i+1, num_line):
    #         dul[count] = {
    #             'ids' : list(set(data[str(i)]) & set(data[str(j)])),
    #             # 'name': f'{i} and {j}',
    #             'arr' : [i, j]
    #         }
    #         count += 1
    #
    # num_dul = len(list(dul)) + 1
    #
    # # num_dul = 4
    # directions = {}
    # count = 0
    #
    # classes = ['motor', 'car', 'bus', 'lgv', 'hgv']
    #
    # for i in range (0, num_dul):
    #     for j in range(i+1, num_dul):
    #         for k in range (2):
    #             if count%2 == 0:
    #                 directions[count] = {
    #                     'direc': f'{i} to {j}',
    #                     0: [],
    #                     1: [],
    #                     2: [],
    #                     3: [],
    #                     4: [],
    #                     5: [],
    #                     6: [],
    #                     7: [],
    #                     8: []
    #                 }
    #             else:
    #                 directions[count] = {
    #                     'direc': f'{j} to {i}',
    #                     0: [],
    #                     1: [],
    #                     2: [],
    #                     3: [],
    #                     4: [],
    #                     5: [],
    #                     6: [],
    #                     7: [],
    #                     8: []
    #                 }
    #             count += 1
    # # print(dul)
    # # count = 0
    # for couple in dul:
    #     print(couple)
    #     # for feature in dul[couple]:
    #     #     print(feature)
    #     for point in dul[couple]['ids']:
    #         # print(point)
    #         # print(data[dul[couple]['arr'][0]][point])
    #         # print(data[dul[couple]['arr'][1]][point])
    #         if data[str(dul[couple]['arr'][0])][point][1] < data[str(dul[couple]['arr'][1])][point][1]:
    #             directions[couple * (num_dul-2)][data[str(dul[couple]['arr'][1])][point][0]].append(point)
    #         else:
    #             directions[couple * (num_dul - 2) + 1][data[str(dul[couple]['arr'][1])][point][0]].append(point)
    #
    #
    #
    # with open(f"{dir_path}/result.json", "w") as outfile:
    #     json.dump(directions, outfile)
    #
    # d1 = [0] * 9
    # d2 = [0] * 9
    #
    # for i in range(9):
    #     d1[i] = len(directions[0][i])
    #
    # for i in range(9):
    #     d2[i] = len(directions[1][i])

    ###fix2line
    from_0_to_1 = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [],
                   14: []}
    from_1_to_0 = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [],
                   14: []}
    from_0_1 = {"direc": "0 to 1", 0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [],
                12: [], 13: [], 14: []}
    from_1_0 = {"direc": "1 to 0", 0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [],
                12: [], 13: [], 14: []}
    print("truoc", from_0_to_1,from_1_to_0)
    for id_oj, value in data["0"].items():
        if id_oj in data["1"].keys():
            if value[1] < data["1"][id_oj][1]:
                from_0_to_1[value[0]].append({id_oj: data['0'][id_oj]})
                from_0_1[value[0]].append(id_oj)
            elif value[1] > data["1"][id_oj][1]:
                from_1_to_0[value[0]].append({id_oj: data['0'][id_oj]})
                from_1_0[value[0]].append(id_oj)
    directions = {"0": from_0_1, "1": from_1_0}
    with open(f"{dir_path}/result.json", "w") as outfile:
        json.dump(directions, outfile)
    print("sau", from_0_to_1, from_1_to_0)
    d1 = [0] * 14
    d2 = [0] * 14
    for i in range(len(from_0_to_1) - 1):
        d1[i] = len(from_0_to_1[i])
        d2[i] = len(from_1_to_0[i])

    return d1, d2

def direct_detector_2long(frame_,dir_path):
    f = open(f'{dir_path}/data_idlinetoline_d_hour.json', "r", encoding='utf-8')
    data = json.load(f)
    f.close()

    lines = list(data.keys())
    num_line = len(lines)

    dul = {}

    # dul = set(data[0]) & set(data[1])

    count = 0
    for i in range (0, num_line-1):
        for j in range(i+1, num_line):
            dul[count] = {
                'ids' : list(set(data[str(i)]) & set(data[str(j)])),
                # 'name': f'{i} and {j}',
                'arr' : [i, j]
            }
            count += 1

    num_dul = len(list(dul)) +1

    # num_dul = 4
    directions = {}
    count = 0

    classes = ['motor', 'car', 'bus', 'lgv', 'hgv']

    for i in range (0, num_dul):
        for j in range(i+1, num_dul):
            for k in range (2):
                if count%2 == 0:
                    directions[count] = {
                        'direc': f'{i} to {j}',
                        0: [],
                        1: [],
                        2: [],
                        3: [],
                        4: [],
                        5: [],
                        6: [],
                        7: [],
                        8: []
                    }
                else:
                    directions[count] = {
                        'direc': f'{j} to {i}',
                        0: [],
                        1: [],
                        2: [],
                        3: [],
                        4: [],
                        5: [],
                        6: [],
                        7: [],
                        8: []
                    }
                count += 1
    # print(dul)
    # count = 0
    for couple in dul:
        print(couple)
        # for feature in dul[couple]:
        #     print(feature)
        for point in dul[couple]['ids']:
            # print(point)
            # print(data[dul[couple]['arr'][0]][point])
            # print(data[dul[couple]['arr'][1]][point])
            if data[str(dul[couple]['arr'][0])][point][1] < data[str(dul[couple]['arr'][1])][point][1]:
                directions[couple * (num_dul-2)][data[str(dul[couple]['arr'][1])][point][0]].append(point)
            else:
                directions[couple * (num_dul - 2) + 1][data[str(dul[couple]['arr'][1])][point][0]].append(point)



    with open(f"{dir_path}/result.json", "w") as outfile:
        json.dump(directions, outfile)

    dict_0 = {}
    for l in frame_:
        list_veco = [0] * 9
        for i in range(0, 9):
            for j in directions[0][i]:
                if l[0] <= data['0'][j][1] <= l[1] and l[0] <= data['1'][j][1] <= l[1]:
                    list_veco[data['0'][j][0]] += 1
            dict_0[str(l)] = str(list_veco)

    return dict_0
