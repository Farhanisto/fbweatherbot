import os
import json
import traceback
import requests
from flask import Flask, request
import sys

reload(sys)
sys.setdefaultencoding('utf-8')



token = 'EAAEVjnwxwgYBABkOOgALl0d2DcgAqHDcEBLungVXahZAZBmbO5ic2tAzUly2gWViIMPRIHhUpqPrqeCIQUDIfQJGzczYv5xTdZC8jStwBesWrClO8q08cZCa9D8UCZBeVBaJ7D3Sx0TEv3vsD1rDA5ftQCcYTjUXqL08NvE9dSAZDZD'
app = Flask(__name__)


def location_quick_reply(sender):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": "Share your location:",
            "quick_replies": [
                {
                    "content_type": "location",
                }
            ]
        }
    }
@app.route('/', methods=['GET', 'POST'])

def webhook():
    if request.method == 'POST':
        
        try:
            data = json.loads(request.data.decode())
            #text = data['entry'][0]['messaging'][0]['message']['text']
            message = data['entry'][0]['messaging'][0]['message']
            sender = data['entry'][0]['messaging'][0]['sender']['id']
            if 'attachments' in message:
                if 'payload' in message['attachments'][0]:
                    if 'coordinates' in message['attachments'][0]['payload']:
                        location = message['attachments'][0]['payload']['coordinates']
                        latitude = location['lat']
                        longitude = location['long']
                        api_key = 'e03156839ec6b2ad15552fa25847a24f'
                        url = 'http://api.openweathermap.org/data/2.5/weather?' \
                              'lat={}&lon={}&appid={}&units={}&lang={}'.format(latitude, longitude, api_key, 'metric',
                                                                               'pt')
                        r = requests.get(url)
                        description = r.json()['weather'][0]['description'].title()
                        icon = r.json()['weather'][0]['icon']
                        weather = r.json()['main']
                        text_res = '{}\n' \
                                   'Temperature: {}\n' \
                                   'Pressure: {}\n' \
                                   'Humidity: {}\n' \
                                   'Max: {}\n' \
                                   'Min: {}'.format(description, weather['temp'], weather['pressure'],
                                                    weather['humidity'], weather['temp_max'], weather['temp_min'])
                        payload = {'recipient': {'id': sender}, 'message': {'text': text_res}}
                        r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token,
                                          json=payload)
            else:
                text=message['text']
                payload = location_quick_reply(sender)#{'recipient': {'id': sender}, 'message': {'text': "Hello World"}}
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
        except Exception as e:
            print(traceback.format_exc())

    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == 'my_secret_key':
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"



if __name__ == '__main__':
    app.run(debug=True)