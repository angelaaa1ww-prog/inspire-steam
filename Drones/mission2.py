from pysimverse import Drone 
import time

drone = Drone()
drone = Drone(speed = 1100)
drone.connect()

drone.take_off(30)

drone.move_forward(100)
drone.move_left(300)
drone.move_forward(60)
drone.move_right(400)
drone.move_forward(200)
drone.move_right(400)

drone.land()