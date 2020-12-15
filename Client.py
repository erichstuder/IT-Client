"""
IT - Internal Tracer
Copyright (C) 2019 Erich Studer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from helpers.ComportHandler import ComportHandler
import threading
import time
import os
import sys


class Client:
	def __init__(self):
		self.__running = True
		self.__comPortHandler = ComportHandler(self.__printAnswer)
		self.__keyboardReaderThread = threading.Thread(target=self.__keyboardReaderWorker)
		self.__keyboardReaderThread.daemon = True
		self.__keyboardReaderThread.start()

	def __keyboardReaderWorker(self):
		while self.__running:
			self.__keyboardInputParser(input().strip())

	def run(self, initFile=None):
		if initFile != None:
			self.__keyboardInputParser("run " + initFile)
		with open("mySession.session", "a+b") as sessionFile:
			while True:
				data = self.__comPortHandler.read()
				if data is not None:
					sessionFile.write(data)
					sessionFile.flush()
				if not self.__running:
					break

	def __keyboardInputParser(self, keyboardInput):
		""" list comports may be activated in future
		if keyboardInput == "list comports":
			self.__comPortHandler.getFriendlyNames()
		el
		"""
		if keyboardInput.startswith("set connectionType "):
			connectionType = keyboardInput.split(" ")[2]
			self.__comPortHandler.setConnectionType(connectionType)
			self.__printAnswer("connectionType set to: " + connectionType)
		elif keyboardInput.startswith("set VID "):
			vid = keyboardInput.split(" ")[2]
			self.__comPortHandler.setVID(vid)
			self.__printAnswer("VID set to: " + vid)
		elif keyboardInput.startswith("set PID "):
			pid = keyboardInput.split(" ")[2]
			self.__comPortHandler.setPID(pid)
			self.__printAnswer("PID set to: " + pid)
		#elif keyboardInput.startswith("set deviceId "):
		#	deviceId = keyboardInput.split(" ")[2]
		#	self.__comPortHandler.setDeviceId(deviceId)
		#	self.__printAnswer("deviceId set to: " + deviceId)
		elif keyboardInput.startswith("set comport "):
			comPort = keyboardInput.split(" ")[2]
			self.__comPortHandler.setPort(comPort)
			self.__printAnswer("comport set to: " + comPort)
		elif keyboardInput.startswith("set baudrate "):
			baudrate = keyboardInput.split(" ")[2]
			self.__comPortHandler.setBaudrate(baudrate)
			self.__printAnswer("baudrate set to: " + baudrate)
		elif keyboardInput.startswith("run "):
			scriptFileName = keyboardInput.split(" ")[1]
			if os.path.isfile(scriptFileName):
				self.__printAnswer("running: " + scriptFileName)
				with open(scriptFileName, "r") as scriptFile:
					for line in scriptFile:
						self.__keyboardInputParser(line.strip())
			else:
				self.__printAnswer("error: file not found")
		elif keyboardInput == "exit":
			self.__printAnswer("goodbye...")
			self.__running = False
			time.sleep(0.5)
		else:
			self.__comPortHandler.write(keyboardInput + "\r")

	@staticmethod
	def __printAnswer(answer):
		print(">>  " + answer)


if __name__ == "__main__":
	print("client started")
	if sys.platform.startswith("win"):
		os.system("mode 70,15")
		os.system("title IT client")
	if len(sys.argv) >= 2:
		Client().run(str(sys.argv[1]))
	else:
		Client().run()
