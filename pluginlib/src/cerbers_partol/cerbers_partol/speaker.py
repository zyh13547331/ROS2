import rclpy
from rclpy.node import Node
from cerbers_speech.srv import SpeechText
import espeakng

class Speeker(Node):
    def __init__(self):
        super().__init__('speeker')
        self.speech_service = self.create_service(SpeechText,'speech_text',
                                                  self.speech_callback)
        self.speaker = espeakng.Speaker()
        self.speaker.voice = 'en-us'

    def speech_callback(self,request,response):
        self.get_logger().info(f"准备朗读{request.text}")
        self.speaker.say(request.text)
        self.speaker.wait()
        response.result = True
        return response

def main():
    rclpy.init()
    node = Speeker()
    rclpy.spin(node)
    rclpy.shutdown()
