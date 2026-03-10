from pysimverse import Drone
import time
import cv2

# Initialize OpenCV window (needed to capture keys)
cv2.namedWindow("Drone Control")

# Connect to drone
drone = Drone()
drone.connect()
time.sleep(1)  # wait for connection

# Take off to 5 meters
drone.take_off(5)
rc_speed = 250

print("Controls:")
print("W/S: forward/backward")
print("A/D: left/right")
print("C/R: down/up")
print("Q/E: yaw left/right")
print("1 or ESC: land and exit")

while True:
    key = cv2.waitKey(1) & 0xFF  # capture key press

    # Reset all movement values
    left_right = 0
    forward_backward = 0
    up_down = 0
    yaw = 0

    # Movement controls
    if key == ord("w"):
        forward_backward = rc_speed
    elif key == ord("s"):
        forward_backward = -rc_speed
    elif key == ord("a"):
        left_right = -rc_speed
    elif key == ord("d"):
        left_right = rc_speed
    elif key == ord("c"):
        up_down = -rc_speed
    elif key == ord("r"):
        up_down = rc_speed
    elif key == ord("q"):
        yaw = -rc_speed
    elif key == ord("e"):
        yaw = rc_speed
    elif key == ord("1") or key == 27:  # land on '1' or ESC
        drone.land()
        time.sleep(2)
        break

    # Send the RC commands to the drone
    drone.send_rc_control(left_right, forward_backward, up_down, yaw)

# Clean up OpenCV window
cv2.destroyAllWindows()



    
