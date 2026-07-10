from pysimverse import Drone
import time

drone = Drone()
drone = Drone(speed = 1000)
drone.connect()

drone.take_off(70)

drone.move_forward(230)
drone.move_right(350)

drone.land()