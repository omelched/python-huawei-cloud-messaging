# Python Huawei Cloud Messaging

my fork of Wrapper of huawei cloud messaging [(Push Kit)](https://developer.huawei.com/consumer/en/hms/huawei-pushkit/) for sending push notification using python.

## Home page

https://pypi.org/project/pyhcm/ — original project

## Install
```pip install git+https://github.com/omelched/python-huawei-cloud-messaging```

## Example

### Send notification to device

```
CLIENT_ID = "00000000"
CLIENT_SECRET = "0000000000000000000000000000000000000000000000000000000000000000"
PROJECT_ID = "000000000000000000"

HCMNotification(CLIENT_ID, CLIENT_SECRET, PROJECT_ID).notify_single_device('token_xyz', 'test title', 'test body')
```

### Send notification to multiple devices

```
CLIENT_ID = "00000000"
CLIENT_SECRET = "0000000000000000000000000000000000000000000000000000000000000000"
PROJECT_ID = "000000000000000000"

HCMNotification(CLIENT_ID, CLIENT_SECRET, PROJECT_ID).notify_multiple_devices(['token_1', 'token_2'], 'test title', 'test body')
```