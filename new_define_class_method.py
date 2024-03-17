from typing import Dict, List, Tuple
import json
import statistics
import heapq

def caculate_w_h(H20_point:List, one_third_center_point:List) -> Tuple[int]:
    x_h, y_h = H20_point[:2]
    x_3, y_3 = one_third_center_point[:2]
    x_3, y_3 = int(x_3), int(y_3)
    # print(x_h, y_h, x_3, y_3)
    
    w = abs((x_h - x_3) * 6)
    h = abs((y_h - y_3) * 20)
    
    return (w, h)

def caculate_area(w:int, h:int) -> int:
    return w*h


def indexes_of_largest_elements(lst, n=10):
    indexed_elements = [(-value, index) for index, value in enumerate(lst)]
    heapq.heapify(indexed_elements)
    largest_indexes = [heapq.heappop(indexed_elements)[1] for _ in range(n)]
    return largest_indexes

def caculate_area_by_id(id:int, data:dict) -> List:
    h20_positions = data[str(id)]['H20_center']
    one_third_positions = data[str(id)]['one_third_center']
    areas = []
    for i in range(len(one_third_positions)):
        w, h = caculate_w_h(H20_point=h20_positions[i], one_third_center_point=one_third_positions[i])
        areas.append(caculate_area(w, h))
        
    return areas
        

def get_elements_by_indexes(lst, indexes):
    return [lst[i] for i in indexes]


def class_of_id(id:int, data:dict, limit_sample=10) -> int:
    # print(f'id: {id}')
    areas_of_id = caculate_area_by_id(id=id, data=data)
    list_cls = data[str(id)]['cls']
    if len(areas_of_id) >= 10:
        number_sample = limit_sample
    else:
        if len(areas_of_id)==1:
            number_sample = 1
        else:
            number_sample = round(len(areas_of_id) * 0.3)
    indexs = indexes_of_largest_elements(areas_of_id, n=number_sample)
    values = get_elements_by_indexes(lst=list_cls, indexes=indexs)
    # if not values:
    #     print(values)
    cls = int(statistics.median(values))
    return cls