import os
import requests
import json


def kirim_sms(telpon: str, pesan: str):
    url = os.getenv('ENDPOINT_SMS')
    device_id = os.getenv('DEVICE_ID')
    token = os.getenv("TOKEN_SMS")

    headers = {
        'Content-type': 'application/json',
        'Authorization' : token
    }

    data = [
            {
            "phone_number": telpon,
            "message": pesan,
            "device_id": device_id
        },
    ]

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)

    # print(url, device_id, token)

    print(response)