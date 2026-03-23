from pysimverse import Drone
import time
import cv2
import numpy as np

cv2.namedWindow("Drone Control")

# Initialize drone
drone = Drone()
response = drone.connect()
print("Response:", response)
time.sleep(1)

# --- STATE ---
flying = False
frame = np.zeros((300, 400, 3), dtype=np.uint8)

# speed modes
speed_modes = {1: 200, 2: 400, 3: 600}  # faster base speeds
current_mode = 2
target_speed = speed_modes[current_mode]

# movement variables (direct, no smoothing)
lr = fb = ud = yaw = 0

# last input timestamp for deadman stop
last_input_time = time.time()

print("T: takeoff | L: land")
print("WASD: move | R/C: up/down | Q/E: yaw")
print("1/2/3: speed modes")
print("X: emergency kill | ESC: exit")

while True:
    frame[:] = 0  # clear frame
    cv2.imshow("Drone Control", frame)
    key = cv2.waitKey(1) & 0xFF

    now = time.time()

    # --- DEADMAN STOP ---
    if key != 255:
        last_input_time = now

    if now - last_input_time > 0.2:
        target_lr = target_fb = target_ud = target_yaw = 0
    else:
        target_lr = target_fb = target_ud = target_yaw = 0

        if key == ord("w"):
            target_fb = target_speed
        elif key == ord("s"):
            target_fb = -target_speed
        elif key == ord("a"):
            target_lr = -target_speed
        elif key == ord("d"):
            target_lr = target_speed
        elif key == ord("r"):
            target_ud = target_speed
        elif key == ord("c"):
            target_ud = -target_speed
        elif key == ord("q"):
            target_yaw = -target_speed
        elif key == ord("e"):
            target_yaw = target_speed

    # --- DIRECT MOVEMENT (instant, no smoothing) ---
    lr = target_lr
    fb = target_fb
    ud = target_ud
    yaw = target_yaw

    # --- CONTROLS ---
    if key == ord("t") and not flying:
        drone.take_off(5)
        flying = True
        print("Takeoff")
    elif key == ord("l") and flying:
        drone.land()
        flying = False
        print("Landing")
    elif key == ord("x"):
        drone.send_rc_control(0, 0, 0, 0)
        if flying:
            drone.land()
            flying = False
        print("EMERGENCY STOP")
    elif key == ord("1"):
        current_mode = 1
        target_speed = speed_modes[current_mode]
        print("Speed: SLOW")
    elif key == ord("2"):
        current_mode = 2
        target_speed = speed_modes[current_mode]
        print("Speed: MEDIUM")
    elif key == ord("3"):
        current_mode = 3
        target_speed = speed_modes[current_mode]
        print("Speed: FAST")
    elif key == 27:  # ESC
        if flying:
            drone.land()
        break

    # --- SEND COMMANDS ---
    drone.send_rc_control(int(lr), int(fb), int(ud), int(yaw))

    # --- HUD ---
    cv2.putText(frame, f"Speed Mode: {current_mode}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.putText(frame, f"LR:{int(lr)} FB:{int(fb)}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 2)
    cv2.putText(frame, f"UD:{int(ud)} YAW:{int(yaw)}", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 2)
    status = "FLYING" if flying else "LANDED"
    cv2.putText(frame, status, (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

cv2.destroyAllWindows()