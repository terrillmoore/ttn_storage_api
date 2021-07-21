# ttn_storage_api

Simple (primitive) Python script to get data for a TTN Version 3 app from the [TTN storage application API](https://www.thethingsnetwork.org/docs/applications/storage/).

## Use

### TTN V3 Console Preparation

Set up your application on TTN V3.

Enable the "storage integration".

Create an API key for the application. Record the secret, because you'll need it to call the API.

### Python set up

Put `ttn_storage_api.py` in your current directory, or do the work to put it in your installed python module set. (We've not tested any of that; we just tested interactively in the same directory as this repo.)

```python
import ttn_storage_api
```

### `sensor_pull_storage`

```python
def sensor_pull_storage(appname, accesskey, timestring, *,data_folder = None, ttn_version=3):
```

Pull data from TTN via the TTN storage API.

- `appname` is the name of the TTN app, as a string.

- `accesskey` is the full access key from The Things Network Console. Meaning depends on whether you're using V2 or V3.  For TTN V3, this is must be set to the secret that is output when an API key is created. For TTN V2, this is the API key string from the console, starting with "`ttn-acount-v2`."

- `timestring` indicates amount of data needed, e.g. `'100h'`. For some reason, in TTN , the `d` suffix is not supported; please use `h`.

- `ttn_version` should be 2 or 3; 3 is default.

- If `data_folder` is supplied, it is a string or a `Path`. This is taken as a directory, and the name `"sensors_lastperiod.json"` is appended to form an output file name. The fetched data is written to the resulting file, replacing any previous contents.

   Otherwise, the data is returned as a Python array (for V3) or a string (for V2).

We've not really tested V2 extensively.

## Interactive Examples

```console
>>> import ttn_storage_api
>>>
>>> # set the access key
>>> key = "the secret output by TTN v3 console when you create an API key"
>>>
>>> # read 24 hours of data and display it
>>> ttn_storage_api.sensor_pull_storage("my-app-name", key, "24h")
[{'result': {'end_device_ids': {'device_id': 'device-1', 'application_ids': {}}, 'received_at': '2021-07-20T22:09:14.260657946Z', 'uplink_message': {'decoded_payload': {'humidity': 71, 'temperature': 21.8}, 'settings': {'data_rate': {}}, 'received_at': '2021-07-20T22:09:14.050246577Z'}}}, {'result': {'end_device_ids': {'device_id': 'device-2', 'application_ids': {}}, 'received_at': '2021-07-20T22:12:14.095320042Z', 'uplink_message': {'decoded_payload': {'humidity': 58, 'temperature': 26.8}, 'settings': {'data_rate': {}}, 'received_at': '2021-07-20T22:12:13.879292705Z'}}}, {'result': {'end_device_ids': {'device_id': 'device-3', 'application_ids': {}}, 'received_at': '2021-07-20T22:14:55.108253840Z', 'uplink_message': {'decoded_payload': {'humidity': 58, 'temperature': 25.4}, 'settings': {'data_rate': {}}, 'received_at': '2021-07-20T22:14:54.891246372Z'}
}]
>>>
>>> # put the data in an array
>>> r = ttn_storage_api.sensor_pull_storage("my-app-name", key, "24h")
>>>
>>> # size of the array
>>> len(r)
3
>>> # the first record
>>> r[0]['result']
{'end_device_ids': {'device_id': 'device-1', 'application_ids': {}}, 'received_at': '2021-07-20T22:09:14.260657946Z', 'uplink_message': {'decoded_payload': {'humidity': 71, 'temperature': 21.8}, 'settings': {'data_rate': {}}, 'received_at': '2021-07-20T22:09:14.050246577Z'}}
>>>
>>> # drill down
>>> r[0]['result']['uplink_message']
{'decoded_payload': {'humidity': 71, 'temperature': 21.8}, 'settings': {'data_rate': {}}, 'received_at': '2021-07-20T22:09:14.050246577Z'}
>>> r[0]['result']['uplink_message']['decoded_payload']
{'humidity': 71, 'temperature': 21.8}
>>> r[0]['result']['uplink_message']['decoded_payload']['humidity']
71
>>>
>>> # display the timestamp of the message
>>> r[0]['result']['uplink_message']['received_at']
'2021-07-20T22:09:14.050246577Z'
>>>
>>> # display the sending device's ID
>>> r[0]['result']['end_device_ids']['device_id']
'device-1'
>>>
```

## Meta

### Contributions

This code was written by Terry Moore, MCCI Corporation, with feedback and test assistance from Brian Vant-Hull.

### License

This repository is released under the MIT license.

### Support Open Source Hardware and Software

MCCI invests time and resources providing this open source code, please support MCCI and open-source hardware by purchasing products from MCCI\ and other open-source hardware/software vendors!

For information about MCCI's products, please visit [store.mcci.com](https://store.mcci.com/).
