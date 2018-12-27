#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image,CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from mask_rcnn_ros.msg import Result
import cv2



class Publishsers():
    def __init__(self):
        # Publisherを作成
        self.publisher = rospy.Publisher('/neko', Image, queue_size = 1)
        # messageの型を作成
	self.image = Image()
        self.image_cropped = Image()

    def make_msg(self, Image, detection_result):
	#opencvに変換
	bridge = CvBridge()
   	try:
   	     self.image = bridge.imgmsg_to_cv2(Image, desired_encoding='bgr8')
             self.rows, self.cols = self.image.shape[:2]
             self.image_cropped = np.zeros((self.rows,self.cols, 3), np.uint8)
        except:     
              pass
        for name, detected_area, mask in zip(detection_result.class_names, detection_result.boxes, detection_result.masks):
                if name == "cat":
                           try:
                               self.image = bridge.imgmsg_to_cv2(Image, desired_encoding='bgr8')
                               self.mask = bridge.imgmsg_to_cv2(mask, desired_encoding='passthrough')
                               self.rows, self.cols = self.image.shape[:2]
                               self.image_cropped = np.zeros((self.rows,self.cols, 3), np.uint8)
                               self.detected_area = self.image[detected_area.y_offset:detected_area.y_offset+detected_area.height, detected_area.x_offset:detected_area.x_offset+detected_area.width]
                               self.detected_area = cv2.bitwise_and(self.detected_area, self.detected_area, mask=self.mask[detected_area.y_offset:detected_area.y_offset+detected_area.height, detected_area.x_offset:detected_area.x_offset+detected_area.width])
                               self.image_cropped[detected_area.y_offset:detected_area.y_offset+detected_area.height, detected_area.x_offset:detected_area.x_offset+detected_area.width] = self.detected_area
                           except Exception as e:
                                   print(e) 
	self.image_cropped = bridge.cv2_to_imgmsg(self.image_cropped, encoding='bgr8')
	#Time stamp付与
	self.image_cropped.header.stamp = rospy.Time.now()

    def send_msg(self):
        # messageを送信
        self.publisher.publish(self.image_cropped)

class Subscribe_publishers():
    def __init__(self, pub):
        self.cat_subscriber = rospy.Subscriber('/resize_img/image', Image, self.cat_callback, queue_size = 1)
        self.detection_subscriber =rospy.Subscriber("/mask_rcnn/result", Result, self.bounding_boxes_callback)
	self.pub = pub
        self.cat_image = Image()

    def cat_callback(self, Image):
        #cat imageを保存
        self.cat_image = Image

    def bounding_boxes_callback(self, detection_result):
        self.pub.make_msg(self.cat_image, detection_result)
        self.pub.send_msg()

def main():
    rospy.init_node('cat_getter')

    pub = Publishsers()
    sub = Subscribe_publishers(pub)

    rospy.spin()

if __name__ == '__main__':
    main()
