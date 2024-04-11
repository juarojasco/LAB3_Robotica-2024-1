import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios
import sys
import os

TERMIOS = termios

class TurtleController:
    def __init__(self):
        rospy.init_node('turtle_controller', anonymous=True)
        self.vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.teleport_abs = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        self.teleport_rel = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        self.linear_speed = 1.0  # Velocidad lineal para movimiento hacia adelante y hacia atrás
        self.angular_speed = 1.0  # Velocidad angular para rotaciones

    def move_forward(self):
        vel_msg = Twist()
        vel_msg.linear.x = self.linear_speed
        self.vel_pub.publish(vel_msg)

    def move_backward(self):
        vel_msg = Twist()
        vel_msg.linear.x = -self.linear_speed
        self.vel_pub.publish(vel_msg)

    def rotate_clockwise(self):
        vel_msg = Twist()
        vel_msg.angular.z = -self.angular_speed
        self.vel_pub.publish(vel_msg)

    def rotate_counterclockwise(self):
        vel_msg = Twist()
        vel_msg.angular.z = self.angular_speed
        self.vel_pub.publish(vel_msg)

    def reset_pose(self):
        self.teleport_abs(5.5, 5.5, 0.0)  # Teletransportar a la posición central con orientación 0

    def rotate_180_degrees(self):
        self.teleport_rel(0.0, 3.14159)  # Rotar 180 grados (pi radianes)


def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c

if __name__ == '__main__':
    try:
        controller = TurtleController()
        print("Presiona las teclas para controlar la tortuga:")
        print("W: Mover hacia adelante")
        print("S: Mover hacia atrás")
        print("A: Rotar en sentido antihorario")
        print("D: Rotar en sentido horario")
        print("R: Retornar a la posición y orientación centrales")
        print("ESPACIO: Girar 180 grados")
        print("<------------------------------------------------>")
        while not rospy.is_shutdown():
            key = getkey()
            if key == b'w':
                controller.move_forward()
                print("W: Mover hacia adelante")
            elif key == b's':
                controller.move_backward()
                print("S: Mover hacia atrás")
            elif key == b'a':
                controller.rotate_counterclockwise()
                print("A: Rotar en sentido antihorario")
            elif key == b'd':
                controller.rotate_clockwise()
                print("D: Rotar en sentido horario")
            elif key == b'r':
                controller.reset_pose()
                print("R: Retornar a la posición y orientación centrales")
            elif key == b' ':
                controller.rotate_180_degrees()
                print("ESPACIO: Girar 180 grados")

    except rospy.ROSInterruptException:
        pass
