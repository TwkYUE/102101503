import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np
import mediapipe as mp
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, LeakyReLU, Dropout, Dense
from keras.optimizers import Adam
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import math

class MyDataset:
    def __init__(self, data_dir,model):
        self.data_dir = data_dir
        self.hand_tracker = mp.solutions.hands.Hands(static_image_mode=True)
        self.hand_features = []
        self.model = model
        self.optimizer = Adam()  

    def extract_image_features(self, image):
        # Preprocess the image if needed
        image =self.preprocess_image(image)
         # Pass the image through your custom CNN model
        image_features = self.model.predict(np.expand_dims(image, axis=0))[0]
        return image_features  
    
    def preprocess_image(self, image):  # 添加用于预处理图像的方法
        # 根据需要对图像进行预处理，例如调整大小、归一化等
        return image
    
    def calculate_hand_feature(self, left_hand_points, right_hand_points,head_points):

        left_hand_points = list(left_hand_points)
        right_hand_points = list(right_hand_points)
        # 标准化手部关键点
        normalized_left_hand = self.normalize_keypoints(left_hand_points)
        normalized_right_hand = self.normalize_keypoints(right_hand_points)
        # 计算头部关键点特征
        normalized_head = self.normalize_keypoints(head_points)
        head_feature = np.array(head_points).flatten()
        
        # 计算相对距离特征
        distances = []
        for i in range(len(left_hand_points)):
            for j in range(i + 1, len(left_hand_points)):
                # 计算欧氏距离
                distance = math.sqrt((left_hand_points[i][0] - left_hand_points[j][0])**2 +
                                     (left_hand_points[i][1] - left_hand_points[j][1])**2)
                distances.append(distance)
        for i in range(len(right_hand_points)):
            for j in range(i + 1, len(right_hand_points)):
                # 计算欧氏距离
                distance = math.sqrt((right_hand_points[i][0] - right_hand_points[j][0])**2 +
                                     (right_hand_points[i][1] - right_hand_points[j][1])**2)
                distances.append(distance)

        # 将标准化的手部关键点和相对距离特征合并
        # 将标准化的手部关键点和相对距离特征合并
        normalized_left_hand = np.array(normalized_left_hand)
        normalized_right_hand = np.array(normalized_right_hand)
        distances = np.array(distances)
        # # 将标准化的手部关键点、头部关键点和相对距离特征合并
        hand_feature = np.concatenate((normalized_left_hand.flatten(), normalized_right_hand.flatten(), distances))
        combined_feature = np.concatenate((hand_feature, head_feature))
        return combined_feature

    def normalize_keypoints(self, keypoints):
        keypoints = np.array(keypoints) # 将列表转换为数组
        max_x, max_y = np.max(keypoints, axis=0)
        min_x, min_y = np.min(keypoints, axis=0)
        normalized_keypoints = (keypoints - [min_x, min_y]) / [max_x - min_x, max_y - min_y]

        return normalized_keypoints.tolist() # 将数组转换回列表

    def preprocess_images(self,batch_size):
        final_features = []
        final_labels = []
        subdirectories = os.listdir(self.data_dir)
        for subdirectory in subdirectories:
            sub_directory_path = os.path.join(self.data_dir, subdirectory)
            if os.path.isdir(sub_directory_path):
                image_dir = os.path.join(sub_directory_path, 'Image')
                label_dir = os.path.join(sub_directory_path, 'Annotations')
                image_files = os.listdir(image_dir)
                
                for i, image_file in enumerate(image_files):
                    # 读取图像
                    features = []
                    labels = []
                    image_path = os.path.join(image_dir, image_file)
                    image = cv2.imread(image_path)
                    if image is None:
                        print("Failed to load image:", image_path)
                        continue  # 跳过此图像
                    # 使用高斯滤波
                   #blurred_image = cv2.GaussianBlur(image, (5, 5), 0)  # 调整滤波器的大小

                    # 或者使用中值滤波
                    #blurred_image = cv2.medianBlur(image, 3)  # 调整核的大小

                    # 将模糊的图像调整为灰度图像
                    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # 调整图像大小
                    # 读取图像并调整为三通道图像
                    image_path = os.path.join(image_dir, image_file)
                    image = cv2.imread(image_path)
                    image_resized = cv2.resize(image, (640, 480))


                    # 可视化处理后的图像和手部关键点
                    #cv2.imshow(image_resized)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()
                    # 读取标签
                    label_file = image_file.replace('.jpg', '.xml')
                    label_path = os.path.join(label_dir, label_file)
                    tree = ET.parse(label_path)
                    label = tree.getroot().find('label').text
                    # Extract image features using the custom CNN model
                    image_features = self.extract_image_features(image_resized)
                    # 执行解析XML文件并提取手部关键点坐标的代码
                    xml_file_path = os.path.join(label_dir, label_file)
                    with open(xml_file_path) as f:
                        xml_content = f.read()
                        tree = ET.ElementTree(ET.fromstring(xml_content))

                    root = tree.getroot()

                    # 执行解析XML文件并提取头部关键点坐标的代码
                    head_points = []
                    head_elements = root.findall('head')
                    if len(head_elements) > 0:
                        for point in head_elements[0]:
                            x = int(point.attrib['x'])
                            y = int(point.attrib['y'])
                            head_points.append((x, y))
                    else:
                        continue        

                    left_hand_points = []
                    left_hand_elements = root.findall('left_hand')
                    if len(left_hand_elements) > 0:
                        for point in left_hand_elements[0]:
                            x = int(point.attrib['x'])
                            y = int(point.attrib['y'])
                            left_hand_points.append((x, y))
                    else:
                        continue


                    right_hand_points = []
                    right_hand_elements = root.findall('right_hand')
                    if len(right_hand_elements) > 0:
                        for point in right_hand_elements[0]:
                            x = int(point.attrib['x'])
                            y = int(point.attrib['y'])
                            right_hand_points.append((x, y))
                    else:
                        continue

                    combined_feature = []  # 将 hand_features 的定义放在此处
                    # 执行计算手部特征的代码
                    
                    combined_feature = self.calculate_hand_feature(left_hand_points, right_hand_points,head_points)

                    # 将特征和标签添加到列表中
                    features.append(combined_feature)
                    labels.append(label)

                    # 检查是否达到了批次大小，如果达到则进行模型预测并清空列表
                    if len(features) == batch_size or i == len(image_files) - 1:
                        # 将特征和标签转换为数组
                        features = np.array(features)
                        labels = np.array(labels)
                    
                     # 合并手部关键点特征和头部关键点特征到特征向量中
                    combined_feature = np.concatenate((image_features, self.hand_features, combined_feature))
                    self.hand_features = np.array(self.hand_features)
                    self.hand_features = self.hand_features.flatten()

                    if len(self.hand_features) != combined_feature.shape[0]:
                        self.hand_features = np.concatenate((([0] * (combined_feature.shape[0] - len(self.hand_features))), self.hand_features))
                    combined_feature = np.concatenate((image_features, combined_feature))

                    features.append(combined_feature)
                    labels.append(label)
                    # 将当前批次得到的特征和标签添加到最终的特征和标签列表中
                    final_features.append(features)
                    final_labels.append(labels)

                    # 清空特征和标签列表
                    features = []
                    labels = []
                      # 显式释放图像和标签变量
                    image = None
                    features = None
                    labels = None


                    cv2.destroyAllWindows()
                # 释放XML文件资源
                tree = None    

        # 合并所有批次得到的特征和标签
        final_features = np.concatenate(final_features, axis=0)
        final_labels = np.concatenate(final_labels, axis=0)

        # 将特征保存到磁盘
        np.save(os.path.join(self.data_dir, 'features.npy'), final_features)
        np.save(os.path.join(self.data_dir, 'labels.npy'), final_labels)

def create_custom_cnn_model():
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=(480, 640, 3)))
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3)))
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(128, (3, 3)))
        model.add(LeakyReLU(alpha=0.1))
        model.add(Conv2D(256, (3, 3)))
        model.add(LeakyReLU(alpha=0.1))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(512, (3, 3)))
        model.add(LeakyReLU(alpha=0.1))
        model.add(GlobalAveragePooling2D())
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(2000, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
        return model


# 使用示例
data_dir = 'dataset'
custom_model = create_custom_cnn_model()
dataset = MyDataset(data_dir, custom_model)
dataset.preprocess_images(batch_size=50)
