#
# Name: ttn_storage_api.py
#
# Function:
#	Fetch data from TTN, via storage API
#
# Author:
#	Terry Moore, MCCI
#
# Use:
#	import ttn_storage_api
#	ttn_storage_api.sensor_pull_storage(...) -- see docs for args
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
	   expression -- input expression where error occurred. This
		will include the values that were erroneous.
	   message -- explanation of the error. This is a constant
		string.
	"""
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message

def sensor_pull_storage(appname, accesskey, timestring, *,data_folder = None, ttn_version=3):
	"""
	Pull data from TTN via the TTN storage API.

	appname is the name of the TTN app

	accesskey is the full accesskey from ttn.  For TTN V3, this is is the
		secret that is output when a key is created. For TTN V2, this is
		the string from the console, starting with 'ttn-acount-v2.'

	timestring indicates amount of data needed, e.g. '100h'.

	ttn_version should be 2 or 3; 3 is default.

	If data_folder is supplied, it is a string or a Path; it is taken as a directory,
	and the name "sensors_lastperiod.json" is appended to form an output file name, and
	the data is written to the resulting file, replacing any previous contents.

	Otherwise, the data is returned as a Python array (for V3) or a string (for V2).
	We've not really tested V2 extensively.
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
		raise FetchError(f"ttn_version={ttn_version}", f"Illegal ttn_version (not 2 or 3)")


	# if the user supplied a data_folder, then we want to output to a file.
	if data_folder != None:
		args += [ "-o", str(pathlib.Path(data_folder, "sensors_lastperiod.json")) ]

	# run the curl command to get the data.
	result = subprocess.run( 
		args, shell=False, check=True, capture_output=True
		)

	sresult = result.stdout
	if ttn_version == 3:
		return list(map(json.loads, re.sub(r'\n+', '\n', sresult.decode()).splitlines()))
	else:
		return sresult
