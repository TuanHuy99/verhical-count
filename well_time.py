import math
import json
import statistics
import pandas as pd
import datetime
import numpy as np

from utils import ccw


def distant_pixel(A, B):
    return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)


def getxyfromframe(id, frame, data):
    for i in data[id]['H20_center']:
        if i[2] == frame:
            return i[0], i[1]


def is_cut(point_check, outside_point, linecheck):
    A=point_check
    B=outside_point
    C=linecheck[0]
    D=linecheck[1]
    # if (point_check[0] != outside_point[0] and linecheck[0][0] != linecheck[1][0]):
    #     a = (point_check[1] - outside_point[1]) / (point_check[0] - outside_point[0])
    #     b = point_check[1] - a * point_check[0]
    #     a2 = (linecheck[0][1] - linecheck[1][1]) / (linecheck[0][0] - linecheck[1][0])
    #     b2 = linecheck[0][1] - a2 * linecheck[0][0]
    #     if a != a2:
    #         x_g = (-b + b2) / (a - a2)
    #         y_g = a * x_g + b
    #         if (min(point_check[0], outside_point[0]) <= x_g <= max(point_check[0], outside_point[0]) and min(
    #                 linecheck[0][0], linecheck[1][0]) <= x_g <= max(linecheck[0][0], linecheck[1][0]) and min(
    #                 point_check[1], outside_point[1]) <= y_g <= max(point_check[1], outside_point[1]) and min(
    #                 linecheck[0][1], linecheck[1][1]) <= y_g <= max(linecheck[0][1], linecheck[1][1])):
    #             return (int(x_g), int(y_g))
    #         else:
    #           return None
    #     else:
    #       return None
    # else:
    #     if point_check[0] == outside_point[0] and linecheck[0][0] != linecheck[1][0]:
    #         a2 = (linecheck[0][1] - linecheck[1][1]) / (linecheck[0][0] - linecheck[1][0])
    #         b2 = linecheck[0][1] - a2 * linecheck[0][0]
    #         if (min(point_check[1], outside_point[1]) <= a2*point_check[0]+b2 <= max(point_check[1], outside_point[1]) and min(linecheck[0][1], linecheck[1][1]) <= a2*point_check[0]+b2 <= max(linecheck[0][1], linecheck[1][1])):
    #             return (int(outside_point[0]), int(a2*point_check[0]+b2))
    #     if point_check[0] != outside_point[0] and linecheck[0][0] == linecheck[1][0]:
    #         a = (point_check[1] - outside_point[1]) / (point_check[0] - outside_point[0])
    #         b = point_check[1] - a * point_check[0]
    #         if (min(point_check[1], outside_point[1]) <= a * linecheck[0][0] + b <= max(point_check[1], outside_point[1]) and min(linecheck[0][1], linecheck[1][1]) <= a * linecheck[0][0] + b <= max(linecheck[0][1], linecheck[1][1])):
    #             return (int(linecheck[0][0]), int(a * linecheck[0][0] + b))
    #     return None
    if A == C or A == D:
        return A
    if B == C or B == D:
        return B
    # AB có cắt CD không.
    ## Xoay khác chiều.
    if ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D):
        # Tính tọa độ giao điểm
        x1, y1 = A
        x2, y2 = B
        x3, y3 = C
        x4, y4 = D
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            # Hai đoạn thẳng song song, không có giao điểm
            return None
        else:
            x_intersect = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
            y_intersect = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
            return x_intersect, y_intersect
    return None


def check_inside(point, vertices):
    x, y = point

    # Tạo một điểm nằm rất xa ngoài hình đa giác
    outside_point = (max(vertices, key=lambda v: v[0])[0] + 1, max(vertices, key=lambda v: v[0])[1])
    edges = []
    for i in range(len(vertices) - 1):
        edge = (vertices[i], vertices[i + 1])
        edges.append(edge)
    edges.append((vertices[-1], vertices[0]))

    point_cut = []

    for edge in edges:
        cut_point = is_cut(point, outside_point, edge)
        if cut_point != None:
            if cut_point not in point_cut:
                point_cut.append(cut_point)

    return len(point_cut) % 2 != 0


def check_stop(id, frame, data, num_frame, limit_distance):
    # print(data[id]['H20_center'][-1])
    if frame > int(data[id]['H20_center'][-1][2]) - num_frame:
        # print("not pass")
        return False
    if not getxyfromframe(id, frame + num_frame, data):
        return False
    # print('dis:' , distant_pixel(getxyfromframe(id, frame, data), getxyfromframe(id, frame + num_frame, data)))
    if distant_pixel(getxyfromframe(id, frame, data), getxyfromframe(id, frame + num_frame, data)) < limit_distance:
        # print("pass")
        return True
    else:
        # print("dai hon")
        return False

def check_id_in_area_well_time(polygon, data_point_path, num_frame, limit_distance, max_frame):
    #check_id_in_area
    f1 = open(data_point_path)
    data = json.load(f1)
    well_time = {}
    for id_ in list(data.keys()):
        # print(id_)
        isInside = False
        isStop = False
        for locate in data[id_]['H20_center']:
            #         print(locate)
            x, y, frame = locate
            # Neu xe da o trong vung
            if isInside:
                # Kiem tra xem xe con trong vung k
                if check_inside((x, y), polygon):
                    # Neu xe con trong vung va da dung lai thi bo qua
                    if not isStop:
                        # Neu xe chua dung, kiem tra xem xe da dung chua
                        # if True:
                        if check_stop(id_, frame, data, num_frame, limit_distance):
                            # Neu xe dung, them vào dict
                            well_time[id_] = {
                                'stopTime': frame,
                                'outTime': None
                            }
                            isStop = True
                # Neu xe da o trong vung ma gio khong con trong vung
                # thi xe da thoat khoi vung tinh well-time
                else:
                    if id_ in well_time:
                        well_time[id_]['outTime'] = frame
                        isInside = False
                        isStop = False
            # Neu xe chua o trong vung
            else:
                # Kiem tra xem no co vao trong vung k
                if check_inside((x, y), polygon):
                    # Neu xe da vao vung, set isInside = True
                    isInside = True
    # print(well_time['272'])
    a=[]
    if well_time=={}:
        return {'0':[[0,0],0]},{'0':[[0,0],0]}
    for i in well_time.keys():
        if not well_time[i]['outTime']:
            a.append(i)
    for i in a:
        del well_time[i]
    ### end check -> well_time
    id_max = 0
    cls = 0
    all_={}
    max_f=0
    for i in well_time.keys():
        if (well_time[i]['outTime'] - well_time[i]['stopTime']) > max_frame:
            frame_dis = well_time[i]['outTime'] - well_time[i]['stopTime']
            all_[i] = [[well_time[i]['stopTime'], well_time[i]['outTime']],int(statistics.median(data[i]['cls']))]
            if frame_dis > max_f:
                max_f=frame_dis
                id_max=i
    print(all_)
    print(len(well_time))
    if len(all_)==0:
        return {'ERROR: NO STOP': [[0, 0], 0]},{'ERROR: NO STOP': [[0, 0], 0]}
    return all_, {id_max:[[well_time[id_max]['stopTime'], well_time[id_max]['outTime']],int(statistics.median(data[id_max]['cls']))]}

def xuat_excel_all_dwelltime(all,time_start_video,path_ex_allDwellTime,num_class):
    # data_point_path = "E:/cuv1q/data_point_5.json"
    # polygon = [(788,782),(1888,571),(1893,641),(965,1077)]
    # num_frame=30
    # limit_distance=50
    # max_frame=150
    # check_id_in_area(polygon, data_point_path, num_frame, limit_distance)
    # print("ALL : ",all)
    # print("MAX : ",max_f)

    #### excel
    # time_start_video='17:36:36'
    start_time = datetime.datetime.strptime(time_start_video, "%H:%M:%S")
    cls_val=["Motor", "Car", "BUS", "LGV", "HGV"]
    if num_class == 9:
        cls_val = ["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV", "ALL"]
    rows = []
    for ID, values in all.items():
        time1_frame, time2_frame = values[0]
        cls = cls_val[int(values[1])]

        time1 = start_time + datetime.timedelta(seconds=time1_frame/30)
        time2 = start_time + datetime.timedelta(seconds=time2_frame/30)
        time_diff = (time2 - time1).seconds
        rows.append([ID, cls, time1.strftime("%H:%M:%S"), time2.strftime("%H:%M:%S"), str(time_diff)])

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=['ID', 'Vehicle', 'Stop Time', 'Depart Time', 'D_well_time'])

    # Write the DataFrame to Excel
    # excel_filename = path_ex_allDwellTime+'outputDWELL.xlsx'
    # df.to_excel(excel_filename, index=False)
    # print(f'Data has been written to {excel_filename}')
    return df


#### check time in range
def find_time_block(input_time):
    # Chuyển đổi thời gian đầu vào từ chuỗi "hh:mm:ss" thành số phút
    hours, minutes, seconds = map(int, input_time.split(':'))
    total_minutes = hours * 60 + minutes

    # Xác định khung thời gian 15 phút mà thời điểm nằm trong
    block_start = (total_minutes // 15) * 15
    block_end = block_start + 15

    # Chuyển đổi kết quả thành chuỗi "hh:mm - hh:mm"
    block_start_time = '{:02d}:{:02d}'.format(block_start // 60, block_start % 60)
    block_end_time = '{:02d}:{:02d}'.format(block_end // 60, block_end % 60)

    return f'{block_start_time}-{block_end_time}'

def write_max_val(max_f,time_start_video,path_ex_allDwellTime,num_class):
    hours, minutes, seconds = map(int, time_start_video.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    reference_frame = total_seconds * 30

    result={}
    # Duyệt qua từng ID và dữ liệu tương ứng
    for ID, (interval, value) in max_f.items():
        interval_start, interval_end = interval

        # Chuyển đổi thời gian sang số khung hình
        frame_A = reference_frame + interval_start
        frame_B = reference_frame + interval_end

        # Tìm khoảng thời gian 15 phút chứa frame_A và frame_B
        block_start_time = find_time_block(f'{int((frame_A//30)//3600):02d}:{int((frame_A//30)%3600)//60:02d}:{int((frame_A//30)%60):02d}')
        block_end_time = find_time_block(f'{int((frame_B//30)//3600):02d}:{int((frame_B//30)%3600)//60:02d}:{int((frame_B//30)%60):02d}')

        # Tính B - A
        difference = interval[1] - interval[0]

        # Kiểm tra xem có cần cập nhật kết quả hay không
        if block_start_time not in result or difference > result[block_start_time][0]:
            result[block_start_time] = (difference, ID, value)

    # In ra ID có giá trị của B - A lớn nhất trong mỗi khung thời gian
    for block_time, (max_difference, max_difference_ID, value) in result.items():
        print(f"Khung thời gian {block_time}: ID {max_difference_ID} {value} có B - A lớn nhất là {max_difference//30}s")

    cls_val = ["Motor", "Car", "BUS", "LGV", "HGV"]
    if num_class == 9:
        cls_val = ["Motor", "Bicycle", "Car", "Taxi", "Coach", "Bus", "LGV", "HGV", "VHGV", "ALL"]
    rows = []
    for block_time, (max_difference, max_difference_ID, value) in result.items():
        rows.append([block_time,max_difference_ID, cls_val[value], str(max_difference//30)])

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=['Time', 'ID', 'Vehicle', 'D_well_time_MAX'])

    # Write the DataFrame to Excel
    # excel_filename = path_ex_allDwellTime + 'outputDWELLMAX.xlsx'
    # df.to_excel(excel_filename, index=False)
    # print(f'Data has been written to {excel_filename}')
    return df

def getMeanDistance(list_toa_do, distance):
  arr_m = np.mean(np.array([distant_pixel([list_toa_do[0][0], list_toa_do[0][1]], [list_toa_do[0][2], list_toa_do[0][3]]), distant_pixel([list_toa_do[1][0], list_toa_do[1][1]], [list_toa_do[1][2], list_toa_do[1][3]]), distant_pixel([list_toa_do[2][0], list_toa_do[2][1]], [list_toa_do[2][2], list_toa_do[2][3]])]))/distance
  return arr_m

# data_point_path = "E:/cuv1q/data_point_5.json"
# polygon = [(788,782),(1888,571),(1893,641),(965,1077)]#
# num_frame=30#
# limit_distance=50#
# max_frame=150#
# all_,max_f=check_id_in_area_well_time(polygon, data_point_path, num_frame, limit_distance, max_frame)
#
# time_start_video='17:36:36'#
# path_ex_allDwellTime=''
# xuat_excel_all_dwelltime(all_,time_start_video,path_ex_allDwellTime)
# write_max_val(max_f,time_start_video,path_ex_allDwellTime)
