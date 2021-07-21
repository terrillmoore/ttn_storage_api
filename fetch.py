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
#	fetch.sensor_pull_storage(...)
#
#	Or just cut/paste into your script.
#

import subprocess

def sensor_pull_storage(accesskey, timestring, appname, data_folder):
	"""
	Pull data from TTN via the storage API.

	accesskey is the full accesskey from ttn, starting with 'ttn-acount-v2.'
	timestring indicates amount of data needed, e.g. '1d'.
	appname is the name of the TTN app
	data_folder, if not None, says where to put the data.
	"""
	args = 	[ "curl",
		  "-X", "GET",
		  "--header", "Accept: application/json",
		  "--header", f"Authorization: key {accesskey}",
		  f"https://{appname}.data.thethingsnetwork.org/api/v2/query?last={timestring}"
		]

	# if the user supplied a data_folder, than tack on the args.
	# list1 += list2 syntax means "append each element of list2 to list 1"
	if data_folder != None:
		args += [ "-o", f"{data_folder}sensors_lastperiod.json"]

	return subprocess.run( 
		args, shell=False
		)
