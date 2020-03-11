import qwiic_vl53l1x
import time
import sys

class Laser:
	def  __init__(self):
		self.distance = 0

	def runExample(self):
		print("\nSparkFun VL53L1X Eample")
		mySensor = qwiic_vl53l1x.QwiicVL53L1X()

#	if mySensor.isConnected() == False:
#		print("The Laser is not connected.")
#		return

		mySensor.sensor_init()

		while True:
			try: 
				mySensor.start_ranging()
				time.sleep(0.005)
				self.distance = mySensor.get_distance()
				time.sleep(00.005)
				mySensor.stop_ranging()

				# print("Distance (mm): %s " % distance)
				print(self.distance)
				return self.distance
			except Exception as e:
				print(e)


print("Testing the VL53L1X Distance Sensor")
test = Laser()
test.runExample()

