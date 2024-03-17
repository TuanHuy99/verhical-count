# import psutil
# import os
#
# def get_all_drives():
#     drives = []
#     partitions = psutil.disk_partitions(all=True)
#     for partition in partitions:
#         if partition.device and partition.mountpoint:
#             drives.append((partition.device, partition.mountpoint))
#     return drives
#
# # Gọi hàm để lấy danh sách tất cả các ổ đĩa
# all_drives = get_all_drives()
#
# # In danh sách ổ đĩa
# for drive in all_drives:
#     print(f"Device: {drive[0]}, Mountpoint: {drive[1]}")
#     print(os.listdir(drive[0]))
#
import os
import glob

def get_subdirectories_and_videos(directory):
    subdirectories = []
    videos = []

    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            subdirectories.append(os.path.join(root, dir))
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                videos.append(os.path.join(root, file))

    return subdirectories, videos

# Thay đổi đường dẫn của thư mục gốc tại đây
root_directory = 'D:/'

# Gọi hàm để lấy danh sách thư mục con và tập tin video
subdirectories, videos = get_subdirectories_and_videos(root_directory)

# In danh sách thư mục con
print("Subdirectories:")
for subdirectory in subdirectories:
    print(subdirectory)

# In danh sách tập tin video
print("Videos:")
for video in videos:
    print(video)

