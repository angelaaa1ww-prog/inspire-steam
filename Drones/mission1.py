from pysimverse import Drone
import time

drone = Drone()
drone = Drone(speed = 400)
drone.connect()

drone.take_off(100)

drone.move_forward(250)
drone.move_right(250)

drone.land()