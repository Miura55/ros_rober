#!/usr/bin/python3
import time
import rospy
from rospy.exceptions import ROSInterruptException
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range


class Contorller:
    def __init__(self):
        rospy.init_node('controller', anonymous=True)
        rospy.on_shutdown(self.shutdown_callback)
        self.distance = 100
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('scan', Range, self.scan_callback)
        rospy.Timer(rospy.Duration(1.0), self.timer_callback)

        # Twistの初期化
        twiet = Twist()
        twiet.linear.x = 0
        twiet.angular.z = 0
        self.pub.publish(twiet)

    def scan_callback(self, data):
        # センサーの値を受け取る
        self.distance = data.range
        rospy.loginfo("distance: %f", self.distance)

    def timer_callback(self, event):
        # Twistの初期化
        twiet = Twist()
        if self.distance < 15:
            twiet.linear.x = 0
            twiet.angular.z = 0.5
        else:
            twiet.linear.x = 0.5
            twiet.angular.z = 0
        rate = rospy.Rate(10)
        for i in range(5):
            self.pub.publish(twiet)
            rate.sleep()

    def shutdown_callback(self):
        rospy.loginfo("Stop")
        rospy.sleep(1)
        twiet = Twist()
        twiet.linear.x = 0
        twiet.angular.z = 0
        self.pub.publish(twiet)


if __name__ == '__main__':
    try:
        Contorller()
        rospy.spin()
    except ROSInterruptException:
        pass
