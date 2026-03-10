from pysimverse import Drone 
import time

drone = Drone()


drone.take_off(200)

left_right = 0
forward_backwards = 0
up_down = 0
yaw = 0

while True:
    drone.send_rc_control(
        left_right=left_right,
        forward_backward=forward_backwards,
        up_down=up_down,
        yaw=yaw
    )
