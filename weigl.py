#!/usr/bin/env python

# (C) Eric Boxer, 2016
#

# ===============
# Imports
# ===============

import socket 	# Weigl gear is fairly dependant on commpuncating through UDP packets

# ===============
# Start the weigl class
# ===============

class device:
	def __init__(self, ipAddress="0.0.0.0", port=5555, port2=5556, displayTime=2):
		self.ipAddress = ipAddress
		self.port = port
		self.port2 = port2
		self.displayTime = displayTime											# How long does a message on the screen stay on in 1/100 of second incraments

# ===============
# Operational methods.
# ===============
	def makeArgumentLowerString(self,argument):
		"""
		Since most optional arguments will be text based this will convert the argument to a lowercase string.
		"""
		return str(argument).lower()

	def sendCommand(self,command,expectReturn="No",expectedReturnMessages=1):
		"""
		The baase of sending a command and get any information back if provided
		"""
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)					# Open the socket
		s.settimeout(.5)
		s.bind(('',self.port))
		s.sendto(command, (self.ipAddress,self.port))							# Send the Packet
		# q =self.makeArgumentLowerString(expectReturn) 
		try:
			l = []
			while True:
				s.connect((self.ipAddress,self.port))
				t = s.recv(65535)											# 
				if t == "":
					print "No Data"
				l.append(t)
			return l
		except socket.error:
			return socket.error

# ===============
# Setup Methods
# ===============
	def getInfo(self):
		"""
		Devices: All
		Get info from the device. Returns pretty much everythign you'd want to know about it.
		"""
		a="!?#"
		return self.sendCommand(a, expectReturn="Yes")							# Semd the command. Looks like Grawlixes - http://bxhd.me/1WCdaOZ

	def factoryReset(self,areYouSure="No"):										# Basically jsut a doublecheck to make sure REALLY want to reboot the device.
		"""
		Devices: All
		Factory reset the device. Requires positive validation.
		"""
		q = self.makeArgumentLowerString(areYouSure)
		if q == "yes" or q == "true" or q == "1":								# Need someway to catch booleans in here. Not terribly worried at the moment.
			a = "!sfactory#"
			return self.sendCommand(a)
		else:
			return self.displayMessage("Not         Resetting")					# Lots of spaces the get to the new line.

	def reboot(self):
		"""
		Devices: all
		Soft reboots the device, similiar to power cycling.
		"""
		a = "!sreboot#"
		return self.sendCommand(a)


# ===============
# Display functions
# ===============
	def displayMessage(self, message, time=0):									# Why doest time=self.displayTime work??
		"""
		Devices: All
		Sends a message to be displayed on the LCD screen.
		"""
		if time ==0:															# Might be a messy way to set a default time for each object. Will look into this later?
			time=self.displayTime
		if time > 255:															# Setting the dispalyTime to 255 keeps the message on the display indefinatley. 
			time = 255
		a="!mmd%s:\"%s\"#" % (time, message)									# Format the command correctly
		self.sendCommand(a)														# Send the command
		return "%s Displayed"

	def displayReset(self, resetMessage="Display Reset"):
		"""
		Devices: All
		Clears the display.
		"""
		self.displayMessage(resetMessage, 1)												# Using 1 because 0 is already taken. Don't think you'd be able to see it.
		return

	def displayClear(self):
		"""
		Devices: All
		Clears the display. This is just an alias of the displayReset.
		"""

# ===============
# Network Settings Functions
# ===============
	def setIpAddress(self, newIpAddress, confirmation="No"):
		"""
		Devices: All
		Sets the IP address of the device. Will fail of the IP address is not valid.
		"""
		try:																	# Since socket is already imported might as well leverage the the IP checker
			socket.inet_aton(newIpAddress)
			q = self.makeArgumentLowerString(confirmation)
			a = "!sip%s#" % newIpAddress
			return self.sendCommand(a, expectReturn=q)
		except socket.error:
			return "The IP address %s is not valid." % newIpAddress

	def setSubnetMask(self, newSubnetMask="255.255.255.0", confirmation="No"):					# Need to add validation of subnet mask
		"""
		Devices: All
		Sets the subnet mask of the device. Default is 255.255.255.0.
		"""
		q = self.makeArgumentLowerString(confirmation)
		a = "ssm%s#" % newSubnetMask
		return self.sendCommand(a, expectReturn=q)

	def setGateway(self, newGateway, confirmation="No"):
		"""
		Devices: All
		Sets the Gateway address of the device. Will fail of the IP address is not valid.
		"""
		try:																	# Since socket is already imported might as well leverage the the IP checker
			socket.inet_aton(newGateway)
			q = self.makeArgumentLowerString(confirmation)
			a = "!sip%s#" % (newGateway)
			return self.sendCommand(a, expectReturn=q)
		except socket.error:
			return "The IP address %s is not valid." % newGateway

# ===============
# Show Functions
# ===============

	def showStart(self, showNumber):
		"""
		Devices: Procommander Series
		Starts a new show.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rsn%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)

	def showEnd(self, showNumber):
		"""
		Devices: Procommander Series
		Stops the called show.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rse%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)

		def showPause(self, showNumber=0):										# 
		"""
		Devices: Procommander Series
		Pauses the called show. if showNumber == 0 all shows are paused. By default all shows are paused.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rse%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)

	def showStartAdd(self, showNumber):
		"""
		Devices: Procommander Series
		Starts a new show. If a show is already running it will add this show. Maximum of 5 shows can be running at once.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rsa%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)

	def showStartTerminate(self, showNumber):
		"""
		Devices: Procommander Series
		Starts a new show and stops all other shows. If this show is already running it will continue.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rst%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)

	def showStartInterrupt(self, showNumber):
		"""
		Devices: Procommander Series
		Starts a new show and stops all other shows.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rsi%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)

	def ShowRestart(self, showNumber):
		"""
		Devices: Procommander Series
		Starts a new show. If it is alreaedy running it will restart from the begining.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rsr%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)

	def ShowStartPolyphonic(self, showNumber):
		"""
		Devices: Procommander PHX
		Starts or restarts the called show if running in polyphonic mode. All audio is mixed to audio channel 1.
		"""
		q = int(showNumber)														# Convert showNumber to an int
		a = "!rsx%s#" % (q)
		return self.sendCommand(a, expectReturn="No", expectedReturnMessages=1)


# ===============
# EOF
# ===============

# ===============
# Playground
# ===============

# import time

# phx1 = device(ipAddress="10.0.1.151")
# ana1 = device(ipAddress="10.0.1.152")

# phx1.setGateway(newGateway="10.0.1.1", confirmation="No")
