from djitellopy import Tello

me = Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()