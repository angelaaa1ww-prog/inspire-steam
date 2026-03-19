from pysimverse import Drone 
import time

drone = Drone()
drone = Drone(speed = 500)
drone.connect()

drone.take_off(30)

drone.move_forward(90)
drone.move_left(250)
drone.move_forward(90)
drone.move_right(250)
drone.move_forward(90)
drone.move_right(250)

drone.land()