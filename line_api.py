import requests

class LINENotifyBot(object):
    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}
        self.API_URL = "https://notify-api.line.me/api/notify"

    def send(
        self,
        message,
        image=None,
        sticker_package_id=None,
        sticker_id=None,
    ):
        payload = {
            'message': message,
            'stickerPackageId': sticker_package_id,
            'stickerId': sticker_id,
        }

        files = None
        if image is not None:
            files = {'imageFile': open(image, 'rb')}

        r = requests.post(
            self.API_URL,
            headers=self.__headers,
            data=payload,
            files=files,
        )