import urllib2
import time
import json
from base64 import b64encode

class Pysumi(object):
	def __init__(self, user, password):
		self.user = user
		self.authToken = b64encode("%s:%s"%(user, password))
		self.devices = []
		self.host = ""
		self.getPartition()
	
	def updateDevices(self):
		data = '{"clientContext":{"appName":"FindMyiPhone","appVersion":"1.1","buildVersion":"99","deviceUDID":"0000000000000000000000000000000000000000","inactiveTime":2147483647,"osVersion":"4.2.1","personID":0,"productType":"iPad1,1"}}'
		deviceString = json.loads(self.makeRequest("initClient",data))['content']
		for device in deviceString:
			deviceDict = {}
			deviceDict['id'] = device['id']
			deviceDict['battery'] = device['b']*100
			deviceDict['name'] = device['name']
			deviceDict['model'] = device['deviceModel']
			deviceDict['displayName'] = device['deviceDisplayName']
			deviceDict['latitude'] = device['location']['latitude']
			deviceDict['longitude'] = device['location']['longitude']
			deviceDict['updateTime'] = device['location']['timeStamp']
			deviceDict['positionType'] = device['location']['positionType']
			deviceDict['accuracy'] = device['location']['horizontalAccuracy']
			self.devices.append(deviceDict)
		
	def sendMessage(self,deviceNum,subject,message,sound=True):
		deviceId = self.devices[deviceNum]['id']
		if sound == True:
			alarm = "true"
		else:
			alarm = "false"
		data = '{"clientContext":{"appName":"FindMyiPhone","appVersion":"1.1","buildVersion":"99","deviceUDID":"0000000000000000000000000000000000000000","inactiveTime":5911,"osVersion":"3.2","productType":"iPad1,1","selectedDevice":"%s","shouldLocate":false},"device":"%s","serverContext":{"callbackIntervalInMS":3000,"clientId":"0000000000000000000000000000000000000000","deviceLoadStatus":"203","hasDevices":true,"lastSessionExtensionTime":null,"maxDeviceLoadTime":60000,"maxLocatingTime":90000,"preferredLanguage":"en","prefsUpdateTime":1276872996660,"sessionLifespan":900000,"timezone":{"currentOffset":-25200000,"previousOffset":-28800000,"previousTransition":1268560799999,"tzCurrentName":"Pacific Daylight Time","tzName":"America/Los_Angeles"},"validRegion":true},"sound":%s,"subject":"%s","text":"%s"}'%(deviceId,deviceId,alarm,subject,message)
		self.makeRequest("sendMessage",data)


	def lockDevice(self,deviceNum,code):
		deviceId = self.devices[deviceNum]['id']
		if type(code) != int or len(str(code)) != 4:
			print "Lock code must be a 4 digit number"
			return
		data = '{"clientContext":{"appName":"FindMyiPhone","appVersion":"1.1","buildVersion":"99","deviceUDID":"0000000000000000000000000000000000000000","inactiveTime":5911,"osVersion":"3.2","productType":"iPad1,1","selectedDevice":"%s","shouldLocate":false},"device":"%s","oldPasscode":"","passcode":"%s","serverContext":{"callbackIntervalInMS":3000,"clientId":"0000000000000000000000000000000000000000","deviceLoadStatus":"203","hasDevices":true,"lastSessionExtensionTime":null,"maxDeviceLoadTime":60000,"maxLocatingTime":90000,"preferredLanguage":"en","prefsUpdateTime":1276872996660,"sessionLifespan":900000,"timezone":{"currentOffset":-25200000,"previousOffset":-28800000,"previousTransition":1268560799999,"tzCurrentName":"Pacific Daylight Time","tzName":"America/Los_Angeles"},"validRegion":true}}'%(deviceId,deviceId,code)
		self.makeRequest("remoteLock",data)
		
	def getPartition(self):
		data = '{"clientContext":{"appName":"FindMyiPhone","appVersion":"1.1","buildVersion":"99","deviceUDID":"0000000000000000000000000000000000000000","inactiveTime":2147483647,"osVersion":"4.2.1","personID":0,"productType":"iPad1,1"}}'
		url = "https://fmipmobile.me.com/fmipservice/device/%s/initClient"%(self.user)
		headers = {
		"Content-Type":"application/json; charset=utf-8",
		"X-Apple-Find-Api-Ver":"2.0",
		"X-Apple-Authscheme":"UserIdGuest",
		"X-Apple-Realm-Support":"1.0",
		 "User-agent":"Find iPhone/1.1 MeKit (iPad: iPhone OS/4.2.1)",
		"X-Client-Name":"iPad",
		"X-Client-Uuid":"0cf3dc501ff812adb0b202baed4f37274b210853",
		"Accept-Language":"en-us",
		"Authorization":"Basic %s"%(self.authToken)
		}
		req = urllib2.Request(url,data,headers)
		try:
			res = urllib2.urlopen(req)
			#host = "%s-fmipmobile.me.com"%res.info().getheader('X-Responding-Partition')
			host = res.info().getheader('X-Apple-MMe-Host')
		except urllib2.HTTPError, e:
			#host = "%s-fmipmobile.me.com"%e.info().getheader('X-Responding-Partition')
			host = e.info().getheader('X-Apple-MMe-Host')
		#self.host = host
		self.host = host
        
	
	def makeRequest(self,method,data):
		url = "https://%s/fmipservice/device/%s/%s"%(self.host,self.user,method)
		headers = {
		"Content-Type":"application/json; charset=utf-8",
		"X-Apple-Find-Api-Ver":"2.0",
		"X-Apple-Authscheme":"UserIdGuest",
		"X-Apple-Realm-Support":"1.0",
		 "User-agent":"Find iPhone/1.1 MeKit (iPad: iPhone OS/4.2.1)",
		"X-Client-Name":"iPad",
		"X-Client-Uuid":"0cf3dc501ff812adb0b202baed4f37274b210853",
		"Accept-Language":"en-us",
		"Authorization":"Basic %s"%self.authToken
		}
		req = urllib2.Request(url,data,headers)
		repsonseString = ""
		while repsonseString == "":
			try:
				res = urllib2.urlopen(req)
				repsonseString = res.read()
			except urllib2.HTTPError, e:
				print e
				time.sleep(30)
		return repsonseString