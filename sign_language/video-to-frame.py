import zipfile
import cv2
import os
import tempfile
import hashlib
from scipy import signal
from scipy import misc
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim


# 包含多个压缩包的文件夹路径
folder_path = "E:\\D\\手语识别系统\\DEVISIGN_D\\P03_1"

output_folder="DEVISIGN_D/D_P03_1"
# 创建一个临时文件夹用于保存解压缩后的视频文件
temp_folder = tempfile.mkdtemp()

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    # 如果是压缩包文件
    if file_name.endswith(".zip"):
        # 打开压缩包
        with zipfile.ZipFile(file_path, 'r') as archive:
            # 获取压缩包中的文件列表
            file_list = archive.namelist()

            for file_name in file_list:
                # 如果是视频文件
                if file_name.endswith(".avi"):
                    # 打开视频文件
                    with archive.open(file_name) as video_file:
                        # 将视频数据写入临时文件
                        temp_file = tempfile.NamedTemporaryFile(delete=False)
                        temp_file.write(video_file.read())
                        temp_file.close()

                        # 创建一个视频文件对象
                        video_stream = cv2.VideoCapture(temp_file.name)

                        # 获取视频文件名（不包含扩展名）
                        video_name = os.path.splitext(file_name)[0]

                        # 创建一个文件夹来保存当前视频的图像帧
                        video_folder = os.path.join(output_folder, video_name)
                        os.makedirs(video_folder, exist_ok=True)

                        previous_frame = None

                        frame_count = 0

                        while True:
                            # 读取视频帧
                            ret, frame = video_stream.read()

                            if not ret:
                                break

                            # 将帧转换为灰度图像
                            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                          

                            # 图像标准化处理（例如，调整亮度和对比度）
                            normalized_frame = cv2.normalize(gray_frame, None, 0, 255, cv2.NORM_MINMAX)

                            # 保存图像
                            output_path = os.path.join(video_folder, f"frame_{frame_count}.jpg")
                            cv2.imwrite(output_path, normalized_frame)

                            frame_count += 1

                            # 显示处理后的视频帧
                            cv2.imshow('Processed Frame', normalized_frame)
                            cv2.waitKey(1)

                        # 释放资源
                        video_stream.release()
                        cv2.destroyAllWindows()

                    # 删除临时文件
                    os.remove(temp_file.name)

# 删除临时文件夹
os.rmdir(temp_folder)
