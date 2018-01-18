import time

import requests
from urllib import parse


class VK:
    def __init__(self, access_token, target_group, max_request_per_second=3):
        self.access_token = access_token
        self.target_group = target_group
        self.max_request_per_second = max_request_per_second
        self.request_timestamps = []

    def post(self, vk_post):
        vk_photo = self.upload_image(vk_post.img_file)
        message_param = parse.urlencode({'message': vk_post.text})
        url = 'https://api.vk.com/method/wall.post?owner_id=-{}&from_group=1&{}&attachments={}&access_token={}'
        url = url.format(self.target_group, message_param, vk_photo, self.access_token)
        response = self._execute_request(url)
        response = response.json()
        return response["response"]["post_id"]

    def upload_image(self, img_file):
        """Return vk photo object in string format: photo{owner_id}_{id}"""

        # Get upload server
        url = 'https://api.vk.com/method/photos.getWallUploadServer?group_id={}&access_token={}'
        url = url.format(self.target_group, self.access_token)
        response = self._execute_request(url)
        upload_url = response.json()["response"]["upload_url"]

        # Upload image
        with open(img_file, "rb") as file:
            response = requests.post(upload_url, files={"photo": file})
            response = response.json()
            server = response["server"]
            photo = response["photo"]
            hash_photo = response["hash"]

        # Save photo to vk
        url = 'https://api.vk.com/method/photos.saveWallPhoto?group_id={}&server={}&photo={}&hash={}&access_token={}'
        url = url.format(self.target_group, server, photo, hash_photo, self.access_token)
        response = self._execute_request(url)
        response = response.json()
        return response["response"][0]["id"]

    ########################

    def _ensure_request_limit(self):
        if len(self.request_timestamps) < self.max_request_per_second:
            return

        oldest = self.request_timestamps[-1]
        while (time.time() - oldest) < 1.0:
            time.sleep(0.1)

    def _register_request(self):
        self.request_timestamps.insert(0, time.time())
        if len(self.request_timestamps) > self.max_request_per_second:
            del self.request_timestamps[-1]

    def _execute_request(self, url):
        self._ensure_request_limit()
        response = requests.get(url, verify=False)
        self._register_request()
        return response
