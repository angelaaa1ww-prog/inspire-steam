from pysimverse import Drone 
import time

drone = Drone()
drone = Drone(speed = 400)
drone.connect()

drone.take_off(30)

drone.move_forward(430)
drone.move_left(200)

drone.move_backward(200)
drone.move_right(500)


drone.land()