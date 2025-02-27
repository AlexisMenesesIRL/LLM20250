import os
from flask import Flask, request
import re
from datetime import datetime
import json
from openai import OpenAI
import sys
from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

sys.path.insert(1, os.path.abspath(os.path.join(os.path.join(os.path.abspath(__file__),".."),"..")))
from config import GPT_KEY

client = OpenAI(
    api_key= GPT_KEY,
)

app = Flask(__name__, static_url_path="/", static_folder="resources")


class StatePublisher(Node):

    def __init__(self):
        global joint_pub, broadcaster
        rclpy.init()
        super().__init__('state_publisher')
        
        qos_profile = QoSProfile(depth=10) # queue size of 10 
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))



    def move_to_angle(self,angle):
        degree = pi / 180.0
        # robot state
        tilt = 0.
        tinc = degree
        swivel = 0.
        angle = 0.
        height = 0.
        hinc = 0.005
        # message declarations
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'axis'
        joint_state = JointState()


        # update joint_state
        now = self.get_clock().now()
        joint_state.header.stamp = now.to_msg()
        # Names of joints from the urdf file 
        joint_state.name = ['swivel', 'tilt', 'periscope']
        joint_state.position = [swivel, tilt, height]

        # update transform
        # (moving in a circle with radius=2)
        odom_trans.header.stamp = now.to_msg()
        odom_trans.transform.translation.x = cos(angle)*2
        odom_trans.transform.translation.y = sin(angle)*2
        odom_trans.transform.translation.z = 0.7
        odom_trans.transform.rotation = \
            euler_to_quaternion(0, 0, angle + pi/2) # roll,pitch,yaw

        # send the joint state and transform
        self.joint_pub.publish(joint_state)
        self.broadcaster.sendTransform(odom_trans)

        # Create new robot state
        # tilt += tinc
        # if tilt < -0.5 or tilt > 0.0:
        #     tinc *= -1
        # height += hinc
        # if height > 0.2 or height < 0.0:
        #     hinc *= -1
        # swivel += degree
        # angle += degree/4

node = StatePublisher()

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/send_instruction",methods=['POST'])
def send_instruction():
    text = ""
    if request.method == 'POST':
        instruction = request.get_json()
        print(instruction["instruction"])
        response = client.chat.completions.create(
                            model = "gpt-3.5-turbo",
                            messages = [
                                {"role": "system", "content": "Vas a responder con un archivo json moviendo el robot con el angulo solicitado. Si no hay angulo, muevelo a un angulo random."},
                                {"role": "user", "content": instruction["instruction"] }
                            ],
                            temperature=0
                    )
        text = response.choices[0].message.content.strip()
        data = json.loads(text)
        print(data)
        node.move_to_angle(data["angulo"])
    return json.dumps({"response":text})
    


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content


def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
    qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
    qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
    qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

if __name__ == "__main__":
    app.run(host=os.getenv("APP_ADDRESS", 'localhost'), \
    port=os.getenv("APP_PORT", 80))