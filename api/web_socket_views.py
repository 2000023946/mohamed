import json 
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accpet()
        print('accepted')
    
    def disconnect(self, code):
        self.close()
        print('disconnected')

    def receive(self, text_data):
        text_data = json.loads(text_data)
        text = text_data['text']
        self.send(text_data=json.dumps({
            'result':'Msg received'
        }))
