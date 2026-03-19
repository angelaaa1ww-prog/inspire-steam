from pysimverse import Drone 
import time

drone = Drone()
drone = Drone(speed = 400)
drone.connect()

drone.take_off(50)

drone.move_forward(300)
drone.move_left(250)

drone.move_backward(90)
drone.move_right(500)

drone.land()