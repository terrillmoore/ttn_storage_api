#
# Name: fetch.py
#
# Function:
#	Fetch data from TTN, via storage API
#
# Author:
#	Terry Moore, MCCI
#
# Use:
#	import fetch
#	fetch.sensor_pull_storage(...) -- see docs for args
#
#	Or just cut/paste into your script.
#

import subprocess
import json
import pathlib
import re

class Error(Exception):
	"""Base class for errors in this module"""
	pass

class FetchError(Error):
	"""Raised when sensor_pull_storage can't deal with input

	Atrributes:
	   expression -- input expression where error occurred
	   message -- explanation of the error.
	"""
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message

def sensor_pull_storage(appname, accesskey, timestring, *,data_folder = None, ttn_version=3):
	"""
	Pull data from TTN via the storage API.

	appname is the name of the TTN app

	accesskey is the full accesskey from ttn.  For TTN V3, this is is the
		secret output when a kye is created. For TTN V2, this is
		the string from the console, starting with 'ttn-acount-v2.'

	timestring indicates amount of data needed, e.g. '1d'.

	ttn_version should be 2 or 3; 3 is default.

	If data_folder is supplied, it is a string or a Path; the name "
	The data is returned as a string. Use json.loads() to decode into an object.
	"""
	args = [ "curl" ]
	if ttn_version == 2:
		args += [
			"-X", "GET",
			"--header", "Accept: application/json",
			"--header", f"Authorization: key {accesskey}",
			f"https://{appname}.data.thethingsnetwork.org/api/v2/query?last={timestring}"
			]
	elif ttn_version == 3:
		args += [
			"-G", f"https://nam1.cloud.thethings.network/api/v3/as/applications/{appname}/packages/storage/uplink_message",
			"--header", f"Authorization: Bearer {accesskey}",
			"--header", "Accept: text/event-stream",
			"-d", f"last={timestring}",
			"-d", "field_mask=up.uplink_message.decoded_payload",
		]
	else:
		raise FetchError(f"Illegal ttn_version (not 2 or 3)")


	# if the user supplied a data_folder, than tack on the args.
	# list1 += list2 syntax means "append each element of list2 to list 1"
	# pathlib.Path allows 
	if data_folder != None:
		args += [ "-o", pathlib.Path(data_folder, "sensors_lastperiod.json") ]

	result = subprocess.run( 
		args, shell=False, check=True, capture_output=True
		)

	sresult = result.stdout
	if ttn_version == 3:
		return list(map(json.loads, re.sub(r'\n+', '\n', sresult.decode()).splitlines()))
	else:
		return sresult
