from robodk.robolink import *  # RoboDK API
from robodk.robomath import *
import time

# Connect to RoboDK
RDK = Robolink()

# Get your programs (use EXACT names from your tree)
pick_prog = RDK.Item('Pick_simulation', ITEM_TYPE_PROGRAM)
drop_prog = RDK.Item('Drop_simulation', ITEM_TYPE_PROGRAM)

# Safety check
if not pick_prog.Valid() or not drop_prog.Valid():
    raise Exception("Programs not found. Check names!")

# Infinite loop
while True:
    print("Picking bottle...")
    pick_prog.RunProgram()
    pick_prog.WaitFinished()

    time.sleep(1)  # small delay

    print("Returning bottle...")
    drop_prog.RunProgram()
    drop_prog.WaitFinished()

    time.sleep(1)  # delay before repeating