#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image,CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from darknet_ros_msgs.msg import BoundingBoxes,BoundingBox
import cv2



class Publishsers():
    def __init__(self):
        # Publisherを作成
        self.publisher = rospy.Publisher('/neko', Image, queue_size = 1)
        # messageの型を作成
	self.image = Image()
        self.image_cropped = Image()

    def make_msg(self, Image, detection_data):
	#opencvに変換
	bridge = CvBridge()
   	try:
   	     self.image = bridge.imgmsg_to_cv2(Image, desired_encoding='bgr8')
             self.rows, self.cols = self.image.shape[:2]
             self.image_cropped = np.zeros((self.rows,self.cols, 3), np.uint8)
        except:     
              pass
        for i in detection_data.bounding_boxes:
                if i.Class == "cat":
                           try:
                                   self.detected_area = self.image[i.ymin:i.ymax, i.xmin:i.xmax]
                                   self.image_cropped[i.ymin:i.ymax, i.xmin:i.xmax] = self.detected_area
                           except:
                                   pass 
	self.image_cropped = bridge.cv2_to_imgmsg(self.image_cropped, encoding='bgr8')
	#Time stamp付与
	self.image_cropped.header.stamp = rospy.Time.now()

    def send_msg(self):
        # messageを送信
        self.publisher.publish(self.image_cropped)

class Subscribe_publishers():
    def __init__(self, pub):
        self.cat_subscriber = rospy.Subscriber('/camera/image_raw', Image, self.cat_callback, queue_size = 1)
        self.detection_subscriber =rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, self.bounding_boxes_callback)
	self.pub = pub
        self.cat_image = Image()

    def cat_callback(self, Image):
        #cat imageを保存
        self.cat_image = Image

    def bounding_boxes_callback(self, detection_data):
        self.pub.make_msg(self.cat_image,detection_data)
        self.pub.send_msg()

def main():
    rospy.init_node('cat_getter')

    pub = Publishsers()
    sub = Subscribe_publishers(pub)

    rospy.spin()

if __name__ == '__main__':
    main()
