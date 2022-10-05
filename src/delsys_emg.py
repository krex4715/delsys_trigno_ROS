#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32MultiArray
import struct 
import time # To run the streaming loop for 5s
import socket
import numpy as np




class delsys:
    def __init__(self):
        self.pub = rospy.Publisher('EMG_datas', Float32MultiArray, queue_size=10)
        self.EMG_IP = "192.168.50.226"
        self.EMG_COMMAND_PORT = 50040
        self.EMG_STREAM_PORT = 50043
        
        # Open a socket to both the command and streaming ports
        self.emgCommandSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.emgCommandSocket.connect((self.EMG_IP, self.EMG_COMMAND_PORT))
        self.emgStreamSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.emgStreamSocket.connect((self.EMG_IP, self.EMG_STREAM_PORT))
        
        # Tell the Trigno server to start broadcasting data packets 
        self.emgCommandSocket.sendall(b'START')
        self.emgCommandSocket.sendall(b'TRIGGER START\r\n\r\n')
        self.startTime = time.time()
        
    def emg_pub(self):
        pub_data = Float32MultiArray()
        
        emgData = self.emgStreamSocket.recv(64)
        emgArray = np.array(struct.unpack("<16f", emgData))
        
        pub_data.data = emgArray.tolist()
        rospy.loginfo(emgArray.tolist())
        self.pub.publish(pub_data)
        
def main():
    rospy.init_node('talker')
    rate = rospy.Rate(2148)
    
    emgs = delsys()
    while not rospy.is_shutdown():
        emgs.emg_pub()
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass