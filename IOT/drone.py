# Name : Angela Amani
# Date : 05/03/2026
# Creation of a drone simulation using pysimverse

# Square Flight Path in PySimVerse

from pysimverse import Drone
import time

def main():
    # Connect to the virtual drone
    drone = Drone()
    drone.connect()

    # Take off
    print("Taking off...")
    drone.take_off()
    time.sleep(2)

    # Fly in a square pattern
    for i in range(4):
        print(f"Flying side {i+1}...")
        drone.move_forward(5)   # move forward 5 units
        time.sleep(2)
        drone.rotate(90)   # rotate 90 degrees
        time.sleep(2)

    # Land
    print("Landing...")
    drone.land()

    print("Square flight complete!")

if __name__ == "__main__":
    main()