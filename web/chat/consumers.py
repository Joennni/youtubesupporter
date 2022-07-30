import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User as user_models
from django.db import models
from datetime import datetime
import time
import sqlite3





class ChatConsumer(WebsocketConsumer):
    
    
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):
        print('text_data : ',text_data)
        text_data_json = json.loads(text_data)
        print ('text_data_json', text_data_json)
        message = text_data_json['message']
        
        
        # ssm=User.objects.values()
        
        # print('ssm : ',ssm)
        # print('ssm print : ',ssm[3]['username'])
        # ssm=ssm[3]['username']
        
        # new_token = [word for word in okt.morphs(message) if not word in stopwords] 
        # new_sequences = tokenizer.texts_to_sequences([new_token])
        # new_pad = pad_sequences(new_sequences, maxlen = 80)
        # score = float(model.predict(new_pad))

        # if score > 0.5:
        #     result = (f'positive({score*100 :.2f})')
        #     print(result)
        # else : 
        #     result = (f'negative({(1-score)*100 :.2f})')
        #     print(result)


        # message = result
        
        # predict1=message
        
        
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # conn = sqlite3.connect("./db.sqlite3")
        # cursor = conn.cursor()

        # cursor.execute("INSERT INTO chat_hook2 VALUES (?,?,?,?,?)", ('0','아이디',message,current_time,'감정분석 전'))
        # conn.commit()
        # time.sleep(5)
        
        
        # cursor.execute("select message from chat_hook2 ORDER BY ROWID DESC LIMIT 1")
        # row = cursor.fetchone()
        # cursor.close
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO chat_hook2 VALUES (?,?,?,?,?)", ('0','아이디',"처리완료",current_time,'감정분석 전'))
        # conn.close()
        
        # colname = cursor.description
        # print('row : ',row)
        # message=row[0]
        # print('message : ',message)
        
        
        message = message.replace('씨발', '^_^')
        message = message.replace('개새끼', '****')
        message = message.replace('바보', '천재')
        message = message.replace('멍청이', '똑똑이')
        message = message.replace('안녕', '안녕은 개뿔')
        message = message.replace('아아아', '오아아오아ㅗ아와')
        
        print ('message : ', message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
    