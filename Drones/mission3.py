from pysimverse import Drone 
import time

drone = Drone()
drone = Drone(speed = 1500)
drone.connect()

drone.take_off(30)

drone.move_forward(650)
drone.move_left(300)

drone.move_backward(150)
drone.move_right(1000)


drone.land()