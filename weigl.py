#!/usr/bin/env python

# Add header info here at some point
#

# ===============
# Imports
# ===============

import socket 	# Weigl gear is fairly dependant on commpuncating through UDP packets
import time

# ===============
# Start the weigl class
# ===============

class weigl:
	def __init__(self):
		self.port=5555
		self.port2=5556
		self.ipAddress = "10.1.0.101"
		self.displayTime = 200													# How long does a message on the screen stay on in 1/100 of second incraments

# ===============
# Since most optional arguments will be text based this will convert the argument to a lowercase string
# ===============
	def makeArgumentLowerString(self,argument):
		return str(argument).lower()

# ===============
# The baase of sending a command and get any information back if provided
# ===============
	def sendCommand(self,command,expectReturn="No"):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)					# Open the socket
		s.sendto(command, (self.ipAddress,self.port))							# Send the Packet
		q =self.makeArgumentLowerString(expectReturn) 
		if q != "no":															# If there is rata to return, return it
			try:
				s.connect((self.ipAddress,self.port))
				return s.recv(4096)
			except socket.error:
				return "The connection was refused. Are you sure it's there?"
		else:
			s.close
			return 

# ===============
# Get info from the device. Returns pretty much everythign you'd want to know about it.
# ===============
	def getInfo(self):
		a="!?#"
		return self.sendCommand(a, expectReturn="Yes")												# Semd the command. Looks like Grawlixes - http://bxhd.me/1WCdaOZ

# ===============
# Factory reset the device. 
# ===============
	def factoryReset(self,areYouSure="No"):										# Basically jsut a doublecheck to make sure REALLY want to reboot the device.
		q = self.makeArgumentLowerString(areYouSure)
		if q == "yes" or q == "true" or q == "1":								# Need someway to catch booleans in here. Not terribly worried at the moment.
			a = "!sfactory#"
			return self.sendCommand(a)
		else:
			return self.displayMessage("Not         Resetting")					# Lots of spaces the get to the new line.

# ===============
# Reboot the device.
# ===============
	def reboot(self,areYouSure="No"):											# Basically jsut a doublecheck to make sure REALLY want to reboot the device.
		q = self.makeArgumentLowerString(areYouSure)
		if q == "yes" or q =="true" or q == "1":								# Need someway to catch booleans in here. Not terribly worried at the moment.
			a = "!sreboot#"
			return self.sendCommand(a)
		else:
			self.displayMessage("Not         Rebooting")

# ===============
# Put a message on the screen. Default time is 2 seconds.
# ===============
	def displayMessage(self, message, time=0):									# Why doest time=self.displayTime work??
		if time ==0:															# Might be a messy way to set a default time for each object. Will look into this later?
			time=self.displayTime
		if time > 255:															# Setting the dispalyTime to 255 keeps the message on the display indefinatley. 
			time = 255
		a="!mmd%s:\"%s\"#"%(time, message)										# Format the command correctly
		self.sendCommand(a)														# Send the command
		return "%s Displayed"

# ===============
#  Reset the display. You know, in case you left it on something that it shouldn't be....
# ===============
	def resetDisplay(self):	
		self.displayMessage("",1)												# Using 1 because 0 is already taken. Don't think you'd be able to see it.
		return "Display Reset"

# ===============
# Set the IP of the device. Confirmation is optionally set to no.
# ===============
	def setIpAddress(self,newIpAddress,confirmation="No"):
		try:																	# Since socket is already imported might as well leverage the the IP checker
			socket.inet_aton(newIpAddress)
			q = self.makeArgumentLowerString(confirmation)
			a = "!sip%s#" % newIpAddress 
			return self.sendCommand(a,expectReturn=q)
		except socket.error:
			return "The IP address %s is not valid." % newIpAddress

# ===============
# Set the Subnet Mask of the device. Confirmation is optionally set to no.
# ===============
	def setSubnetMask(self,newSubnetMask,confirmation="No"):					# Need to add validation of subnet mask
		q = self.makeArgumentLowerString(confirmation)
		a = "ssm%s#" % newSubnetMask
		return self.sendCommand(a,expectReturn=q)

# ===============
# Set the Gateway of the device. Confirmationn is optionally set to no.
# ===============
	def setGateway(self,newGateway,confirmation="No"):
		try:																	# Since socket is already imported might as well leverage the the IP checker
			socket.inet_aton(newGateway)
			q = self.makeArgumentLowerString(confirmation)
			a = "!sip%s#" % newGateway
			return self.sendCommand(a,expectReturn=q)
		except socket.error:
			return "The IP address %s is not valid." % newGateway





# ===============
# EOF
# ===============



# ===============
# Playground
# ===============

# phx1 = weigl()
# phx1.ipAddress = "10.0.1.2"

# phx2 = weigl()
# phx2.ipAddress = "10.0.1.4"

# print phx1.setGateway("192.168.7.7")

