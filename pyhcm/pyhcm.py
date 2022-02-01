from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
import json


class HCMNotification:

    def __init__(self, client_id: str, client_secret: str, project_id: str):
        self.url_auth = 'https://oauth-login.cloud.huawei.com/oauth2/v2/token'
        # self.url_push = f'https://push-api.cloud.huawei.com/v1/{client_id}/messages:send'
        self.url_push = f'https://push-api.cloud.huawei.com/v2/{project_id}/messages:send'
        self.access_token = self.get_access_token(client_id, client_secret)

    def get_access_token(self, client_id, client_secret):
        request = Request(
            self.url_auth,
            data=urlencode(
                {
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret
                }
            ).encode(),
            headers={"Content-type": "application/x-www-form-urlencoded"}
        )
        return json.loads(urlopen(request).read())['access_token']

    @staticmethod
    def _build_notification_payload(registration_ids=None, topic=None, message_title=None, message_body=None,
                                    data: dict = None):
        payload = dict()

        if registration_ids:
            payload['token'] = registration_ids
        else:
            payload['topic'] = topic

        payload['data'] = json.dumps(data) if data else None

        payload['android'] = {}
        payload['android']['notification'] = {}
        if message_title:
            payload['android']['notification']['title'] = message_title
        if message_body:
            payload['android']['notification']['body'] = message_body
        payload['android']['notification']['click_action'] = {
            'type': 3,
        }

        return {
            'message': payload,
        }

    def _send_notification_request(self, payload: object):
        request = Request(
            self.url_push,
            data=json.dumps(payload).encode(),
            headers={"Content-type": "application/json",
                     "Authorization": f'Bearer {self.access_token}'}
        )
        response = json.loads(urlopen(request).read())
        return response

    def notify_topic_subscribers(
            self, topic: str, message_title: str, message_body: str):
        payload = self._build_notification_payload(
            topic=topic,
            message_title=message_title,
            message_body=message_body
        )
        return self._send_notification_request(payload)

    def notify_single_device(self, registration_id: str, message_title: str = None, message_body: str = None,
                             data: dict = None):
        payload = self._build_notification_payload(
            registration_ids=[registration_id],
            message_title=message_title,
            message_body=message_body,
            data=data
        )
        return self._send_notification_request(payload)

    def notify_multiple_devices(self, registration_ids: list[str], message_title: str = None, message_body: str = None,
                               data: dict = None):
        payload = self._build_notification_payload(
            registration_ids=registration_ids,
            message_title=message_title,
            message_body=message_body,
            data=data
        )
        return self._send_notification_request(payload)
