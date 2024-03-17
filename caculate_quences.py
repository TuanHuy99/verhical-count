import math
import statistics
from datetime import timedelta, datetime


def distant_pixel(A, B):
    return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)


def getxyfromframe(id, frame, data):
    for i in data[id]['H20_center']:
        if i[2] == frame:
            return i[0], i[1]


def is_cut(point_check, outside_point, linecheck):
    if (point_check[0] != outside_point[0] and linecheck[0][0] != linecheck[1][0]):
        a = (point_check[1] - outside_point[1]) / (point_check[0] - outside_point[0])
        b = point_check[1] - a * point_check[0]
        a2 = (linecheck[0][1] - linecheck[1][1]) / (linecheck[0][0] - linecheck[1][0])
        b2 = linecheck[0][1] - a2 * linecheck[0][0]
        if a != a2:
            x_g = (-b + b2) / (a - a2)
            y_g = a * x_g + b
            if (min(point_check[0], outside_point[0]) <= x_g <= max(point_check[0], outside_point[0]) and min(
                    linecheck[0][0], linecheck[1][0]) <= x_g <= max(linecheck[0][0], linecheck[1][0]) and min(
                    point_check[1], outside_point[1]) <= y_g <= max(point_check[1], outside_point[1]) and min(
                    linecheck[0][1], linecheck[1][1]) <= y_g <= max(linecheck[0][1], linecheck[1][1])):
                return (int(x_g), int(y_g))
            else:
              return None
        else:
          return None
    else:
        if point_check[0] == outside_point[0] and linecheck[0][0] != linecheck[1][0]:
            a2 = (linecheck[0][1] - linecheck[1][1]) / (linecheck[0][0] - linecheck[1][0])
            b2 = linecheck[0][1] - a2 * linecheck[0][0]
            if (min(point_check[1], outside_point[1]) <= a2*point_check[0]+b2 <= max(point_check[1], outside_point[1]) and min(linecheck[0][1], linecheck[1][1]) <= a2*point_check[0]+b2 <= max(linecheck[0][1], linecheck[1][1])):
                return (int(outside_point[0]), int(a2*point_check[0]+b2))
        if point_check[0] != outside_point[0] and linecheck[0][0] == linecheck[1][0]:
            a = (point_check[1] - outside_point[1]) / (point_check[0] - outside_point[0])
            b = point_check[1] - a * point_check[0]
            if (min(point_check[1], outside_point[1]) <= a * linecheck[0][0] + b <= max(point_check[1], outside_point[1]) and min(linecheck[0][1], linecheck[1][1]) <= a * linecheck[0][0] + b <= max(linecheck[0][1], linecheck[1][1])):
                return (int(linecheck[0][0]), int(a * linecheck[0][0] + b))
        return None

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


def get_class_by_id(id_, data):
    if type(id_) != str:
        id_ = str(id_)
    return int(statistics.median(data[id_]['cls']))


def list_id_to_number_of_classes(list_id, data, num_class=5):
    number_of_each_class = [0] * num_class
    for id_ in list_id:
        cls = get_class_by_id(id_, data)
        number_of_each_class[cls] += 1

    return number_of_each_class


def convert_string_to_datetime(date_string, format):
    '''
    Args:
        date_string:
        format:

    Returns:

    '''
    return datetime.strptime(date_string, format)


def convert_frame_to_datetime(frame, start_time, FPS=30):
    sec = frame / FPS
    sec = round(sec, 3)

    # print(start_time, sec)
    abc = start_time + timedelta(seconds=sec)
    #     formatted_datetime = abc.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    formatted_datetime = abc.strftime("%H:%M:%S")
    # print(formatted_datetime)
    return formatted_datetime


def quence_to_excel_form(quence, id_, start_time, data, num_class=5):
    if num_class == 5:
        classes = ['motor', 'car', 'bus', 'lgv', 'hgv']
    elif num_class == 9:
        classes = ['motor', 'bicycle', 'car', 'taxi', 'coach', 'bus', 'lgv', 'hgv', 'vhgv']
    elif num_class == 15:
        classes = ['xe_con', 'buyt', 'khach_nho', 'khach_vua', 'khach_lon',
                   'tai_nho', 'tai_trung_1', 'tai_trung_2', 'tai_nang', 'tai_sieu_nang',
                   'container20ft', 'container40ft', 'xe_may', 'xe_dap', 'xe_khac']
    else:
        return "Check lai so class"

    start_time = convert_string_to_datetime(start_time, ("%H:%M:%S"))
    excel_form = {
        'start_time': convert_frame_to_datetime(frame=quence['inTime'], start_time=start_time),
        'first_id': int(id_),
        'first_class': classes[get_class_by_id(quence['ids'][0], data)],
        'last_id': quence['ids'][-1],
        'last_class': classes[get_class_by_id(quence['ids'][-1], data)]
    }

    for i in range(num_class):
        excel_form[classes[i]] = list_id_to_number_of_classes(quence['ids'], data=data)[i]

    excel_form['number_of_cars'] = convert_list_class_to_car(list_id_to_number_of_classes(quence['ids'], data=data))[0]
    excel_form['quence_length'] = convert_list_class_to_car(list_id_to_number_of_classes(quence['ids'], data=data))[1]
    excel_form['ids'] = quence['ids']

    return excel_form


def convert_list_class_to_car(list_class):
    #     ['motor', 'car', 'bus', 'lgv', 'hgv'] = [0.3, 1, 2, 1, 2]
    if len(list_class) == 5:
        convert_list = [0.3, 1, 2, 1, 2]
    if len(list_class) == 15:
        convert_list = [1]*15

    convert_to_car = 0
    for i in range(len(list_class)):
        convert_to_car += list_class[i] * convert_list[i]

    convert_to_meter = convert_to_car * 7

    return convert_to_car, int(round(convert_to_meter, -1))


def check_stop(id, frame, data, num_frame=30, limit_distance=150):
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


def caculate_quences(small_zone, big_zone, limit_sec, list_verhicle, data, FPS=30):
    quences = {}
    limit_frame = limit_sec * FPS

    # Tìm các Quences trong zone đã xác định
    for id_ in list_verhicle:
        isInside = False
        for locate in data[id_]['H20_center']:
            x, y, frame = locate
            # Neu xe da o trong vung
            if isInside:
                # Kiem tra xem xe con trong vung k
                if check_inside((x, y), small_zone):
                    pass
                # Neu xe da o trong vung ma gio khong con trong vung
                # thi xe da thoat khoi vung tinh well-time
                else:
                    if id_ in quences:
                        if (frame - quences[id_]['inTime']) > limit_frame:
                            quences[id_]['outTime'] = frame
                            isInside = False
                        else:
                            del quences[id_]
            # Neu xe chua o trong vung    
            else:
                # Kiem tra xem no co vao trong vung k
                if check_inside((x, y), small_zone):
                    isInside = True
                    # Neu xe da vao vung, set isInside = True
                    quences[id_] = {
                        'inTime': frame,
                        'outTime': None,
                        'ids': []
                    }

    frame_info = {}
    # Tìm các id xuất hiện trong bigzone tại từng frame
    for id_ in list_verhicle:
        for locate in data[id_]['H20_center']:
            x, y, frame = locate
            if check_inside((x, y), big_zone):
                if frame in frame_info:
                    frame_info[frame].append(id_)
                else:
                    frame_info[frame] = []
                    frame_info[frame].append(id_)

    # Tìm list các xe trong từng Quences
    # print(frame_info)
    print(quences)
    rm_list = []
    for id_ in quences.keys():
        if quences[id_]['outTime']:
            last_frame = quences[id_]['outTime']
            # in_frame = quences[id_]['inTime']
            quences[id_]['ids'] = []
            for id_car in frame_info[last_frame - 1]:
                # if check_stop(id=id_car, frame=last_frame-1, data=data):
                if True:
                    quences[id_]['ids'].append(id_car)
        else:
            rm_list.append(id_)

    for i in rm_list:
        del quences[i]
    print('quences: ', quences)
    return quences