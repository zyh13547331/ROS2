import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory #获取功能包share目录绝对路径
import os

def main():
    #获取真实图片路径
    default_image_path = os.path.join(get_package_share_directory('python_service'), 'resource', 'default.webp')
    print(f"图片路径: {default_image_path}")
    #使用openCV读取图片
    image = cv2.imread(default_image_path)
    #使用face_recognition库进行人脸检测
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1,
    model="cnn") #cnn模型精度高，但速度慢，hog模型速度快，但精度低
    #绘制人脸检测框
    for top,right,bottom,left in face_locations:
        cv2.rectangle(image,(left,top),(right,bottom),(0,255,0),2)
    #显示检测结果
    cv2.imshow("Face Detection Result", image)
    cv2.waitKey(0)