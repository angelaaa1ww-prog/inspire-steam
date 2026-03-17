from robodk.robolink import *

# Connect to RoboDK
RDK = Robolink()
robot = RDK.Item('', ITEM_TYPE_ROBOT)

#Your targets
pick_app = RDK.Item('Pick_Approach')
pick = RDK.Item('Pick')
place_app = RDK.Item('Place_Approach')
place = RDK.Item('Place')
home = RDK.Item('Home')

#Move robot — bottle moves automatically because it is attached manually
robot.MoveJ(pick_app)
robot.MoveL(pick)
robot.MoveL(pick_app)
robot.MoveJ(place_app)
robot.MoveL(place)
robot.MoveL(place_app)
robot.MoveJ(home)