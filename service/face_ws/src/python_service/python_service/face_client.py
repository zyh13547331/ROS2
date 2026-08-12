import rclpy
from rclpy.node import Node
from face.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory #获取功能包share目录绝对路径
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,ParameterValue,ParameterType

class FaceDetectClient(Node):
    def __init__(self):
        super().__init__('face_client')
        self.bridge_ = CvBridge()
        self.default_image_path_ = os.path.join(get_package_share_directory('python_service'), 'resource', 'default.webp')
        self.image = cv2.imread(self.default_image_path_)
        self.get_logger().info(f"人脸检测已启动")
        self.client = self.create_client(FaceDetector, 'face_detect')

    def call_set_parameters(self,parameters):
        #调用服务修改参数
        #创建客户端
        updata_param = self.create_client(SetParameters,'/face_detect/set_parameters')
        while updata_param.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info(f'等待参数更新服务上线...')
        #创建request
        request = SetParameters.Request()
        request.parameters = parameters
        #调用服务端
        future = updata_param.call_async(request)  # 保存返回的 future
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        return response

    def update_model(self,model='hog'):
        """根据传入的model，构造parameter，然后调用call_set_parameters更新服务端参数"""
        #创建参数对象
        param = Parameter()
        param.name = 'model_'
        #赋值
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value
        #请求更新参数
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f'设置参数结果:{result.successful}{result.reason}')

    def send_request(self):
        while self.client.wait_for_service(timeout_sec=1.0) == False:
            self.get_logger().info('等待服务端启动...')
        #构造request消息
        request = FaceDetector.Request()
        request.image = self.bridge_.cv2_to_imgmsg(self.image)
        #发送请求，通过回调处理响应结果
        future = self.client.call_async(request) # 没有包含响应结果
        future.add_done_callback(self.result_callback) # 添加回调函数，处理响应结果

    def result_callback(self, future):
        response = future.result() # 获取响应结果
        self.get_logger().info(f"接收到响应,结果: {response.number} 个脸部检测到")
        self.show_response(response)
        rclpy.shutdown() # 显示完成后关闭节点，结束 spin

    def show_response(self, response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow("Detected Faces", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    rclpy.init()
    Node = FaceDetectClient()
    Node.update_model('hog')
    Node.send_request()
    Node.update_model('cnn')
    Node.send_request()
    rclpy.spin(Node)
    rclpy.shutdown()
    