

# Move above bottle
robot.MoveJ(pick_app)
robot.MoveL(pick)

# PICK the bottle
bottle.setParent(vacuum)

# Lift the bottle
robot.MoveL(pick_app)

# Move above box
robot.MoveJ(place_app)
robot.MoveL(place)

# RELEASE the bottle
bottle.setParent(RDK.Item('Station'))  # Replace 'Station' with your drop frame

# Move away to Home
robot.MoveL(place_app)
robot.MoveJ(home)