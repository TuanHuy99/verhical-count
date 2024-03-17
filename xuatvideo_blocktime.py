import cv2
import json
from utils import direct_detector
video_paths = ["F:/viet/video2.mp4", "F:/viet/video3.mp4", "F:/viet/video4.mp4", "F:/viet/video5.mp4"]
output_path = "output_video_block.mp4"


def sum_(d):
    sumd = 0
    for a in d:
        sumd += a
    return sumd
def gen_video_from_numframe(video_paths, output_path,start_frame,end_frame,nameuservideo,x,y,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7):
    vid = cv2.VideoCapture(video_paths[0])
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter(output_path, fourcc, 30.0, size)

    start_frame = int(start_frame)  # Nhân 30 để chuyển từ giây sang frame
    end_frame = int(end_frame)
    frame_count = 0
    list_veco = [0] * 9

    f = open(f'static/video_upload/user/{nameuservideo}/data_idlinetoline_d.json')
    data = json.load(f)
    d1, d2, d3, d4 = direct_detector(f'static/video_upload/user/{nameuservideo}')
    idline = [sum_(d1), sum_(d2), sum_(d3), sum_(d4)]
    count=0
    for video_path in video_paths:
        video = cv2.VideoCapture(video_path)

        while frame_count <= end_frame:
            ret, frame = video.read()
            if not ret:
                break
            count+=1
            for i in data[str(idline.index(max(idline)))].keys():
                if data[str(idline.index(max(idline)))][i][1] == count:
                    list_veco[data[str(idline.index(max(idline)))][i][0]] += 1
            if start_frame <= frame_count <= end_frame:
                toadoxy = [[x, y, x1, y1], [x2, y2, x3, y3], [x4, y4, x5, y5], [x6, y6, x7, y7]]
                cv2.line(frame,
                         (int(toadoxy[idline.index(max(idline))][0]), int(toadoxy[idline.index(max(idline))][1])),
                         (int(toadoxy[idline.index(max(idline))][2]), int(toadoxy[idline.index(max(idline))][3])),
                         (255, 253, 0), 4)

                font_color = (0, 0, 255)
                font_size = 0.8
                font_thickness = 2
                cv2.putText(frame, "Motor  Bicycle    Car      Taxi     Coach    Bus      LGV     HGV      VHGV",
                            (110, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                cv2.putText(frame, "Line ", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

                cv2.putText(frame, str(list_veco[0]), (115, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[1]), (235, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[2]), (355, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[3]), (475, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[4]), (595, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[5]), (715, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[6]), (835, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[7]), (955, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)
                cv2.putText(frame, str(list_veco[8]), (1075, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                            font_thickness)

                # cv2.putText(frame, "Cars     LGVs     HGVs     MCs     Buses", (110, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                #             font_color, font_thickness)
                # cv2.putText(frame, "Line ", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                #
                # cv2.putText(frame, str(list_veco[2]+list_veco[3]), (115, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                #             font_thickness)
                # cv2.putText(frame, str(list_veco[6]), (235, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                #             font_thickness)
                # cv2.putText(frame, str(list_veco[7]+list_veco[8]), (355, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                #             font_thickness)
                # cv2.putText(frame, str(list_veco[0]+list_veco[1]), (475, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                #             font_thickness)
                # cv2.putText(frame, str(list_veco[4]+list_veco[5]), (595, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                #             font_thickness)
                #
                # cv2.putText(frame, "Total", (730, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)

                cv2.putText(frame, "Total", (1215, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0),
                            font_thickness)
                cv2.putText(frame, "" + str(
                    list_veco[0] + list_veco[1] + list_veco[2] + list_veco[3] + list_veco[4] + list_veco[5] + list_veco[
                        6] + list_veco[7] + list_veco[8]), (1215, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0),
                            font_thickness)
                # #
                # cv2.putText(frame, "Line2", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                #
                # cv2.putText(frame, str(list_veco[1]), (115, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                # cv2.putText(frame, str(list_veco[3]), (235, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                # cv2.putText(frame, str(list_veco[4]), (355, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                # cv2.putText(frame, str(list_veco[0]), (475, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                # cv2.putText(frame, str(list_veco[2]), (595, 90), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
                #
                # cv2.putText(frame, "" + str(list_veco[0] + list_veco[1] + list_veco[2] + list_veco[3] + list_veco[4]), (730, 90),
                #             cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)
                cv2.putText(frame, "Line ",
                            (int(toadoxy[idline.index(max(idline))][0]), int(toadoxy[idline.index(max(idline))][1])),
                            cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

                output_video.write(frame)

            frame_count += 1
        video.release()
    output_video.release()

start_frame=0
end_frame=180
gen_video_from_numframe(video_paths, output_path,start_frame,end_frame)