import rclpy
from rclpy.node import Node
from face.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory #获取功能包share目录绝对路径
import os
from cv_bridge import CvBridge
import time

class FaceDetectService(Node):
    def __init__(self):
        super().__init__('face_detect')
        self.service_ = self.create_service(FaceDetector, 'face_detect', self.detect_callback)
        self.bridge_ = CvBridge()
        self.number_of_times_to_upsample_ = 1
        self.model_ = "cnn"  # 使用CNN模型进行人脸检测
        self.default_image_path_ = os.path.join(get_package_share_directory('python_service'), 'resource', 'default.webp')

    def detect_callback(self, request, response):
        if request.image.data:
            cv_image = self.bridge_.imgmsg_to_cv2(request.image)
        else:
            cv_image = cv2.imread(self.default_image_path_)
            self.get_logger().info(f"Using default image: {self.default_image_path_}")
            #cv_image是opencv格式的图像数据

        start_time = time.time()
        self.get_logger().info(f"Face detection started at {start_time}")
        face_locations = face_recognition.face_locations(cv_image, 
        number_of_times_to_upsample=self.number_of_times_to_upsample_, model=self.model_)
        end_time = time.time()
        self.get_logger().info(f"Face detection completed at {end_time}, Duration: {end_time - start_time}")
        for top, right, bottom, left in face_locations:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)
        response.number = len(face_locations)
        return response

def main():
    rclpy.init()
    node = FaceDetectService()
    rclpy.spin(node)
    rclpy.shutdown()