from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

'''class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
   			self.channel_name
		)
        self.accept()

        # self.send(text_data=json.dumps(
        #     {
        #         'type': 'connection_established',
        #         'message': 'You are now connected!'
        #     }
        # ))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print('Message:', message)

        async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message
			}
		)

        # self.send(text_data=json.dumps(
		# 	{
		# 		'type': 'chat',
		# 		'message': message
		# 	}
		# ))
    def chat_message(self, event):
       message = event['message']

       self.send(text_data=json.dumps(
			{
				'type': 'chat',
				'message': message
			}
		))
'''

import asyncio, datetime, time as tm
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Quiz, Question, IntervalQuiz

# from .tasks import update_quiz_interval

'''class TestConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            "type": "websocket.accept"
        })

        quiz_name  = self.scope['url_route']['kwargs']['quiz_name']
        quiz_name2 = self.scope['url_route']['kwargs']['quiz_name2']
        user       = self.scope['user']
        print(quiz_name, quiz_name2, user)

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({'key': "hello world"})
        })

    async def websocket_receive(self, event):
        print('receive', event)

        received = json.loads(event['text'])

        list_start = []
        list_end   = []
        for q in received['quizes']:
            qui = await self.get_quizes(q)
            print(qui.start_quiz.strftime("%d/%m/%Y, %H:%M:%S"))

            # await self.send(
            #     {
            #         "type": 'websocket.send',
            #         'text': str(qui)
            #     }
            # )

            list_start.append(str(qui.start_quiz.strftime("%d/%m/%Y, %H:%M:%S")))
            end = qui.start_quiz + datetime.timedelta(minutes=qui.time)
            list_end.append(end.strftime("%d/%m/%Y, %H:%M:%S"))


        await self.send(
            {
                "type": 'websocket.send',
                'text': json.dumps({'start': list_start, 'end': list_end})
            }
        )




    async def websocket_disconnect(self, event):
        print('disconnect', event)

    @database_sync_to_async
    def get_quizes(self, id):
        return Quiz.objects.get(id=id)
'''


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test_group'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({'quiz_start': self.get_quiz_start_time()}))

    def receive(self, text_data=None, bytes_data=None):

        if text_data:
            tm.sleep(1)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'tes',
                    'message': self.get_quiz_start_time()
                }
            )

    def tes(self, event):
        date_now = event['message']
        self.send(json.dumps({'quiz_start': date_now}))

    def disconnect(self, code):
        print(code)

    def here(self):
        for q in Quiz.objects.filter(is_answered=False):
            current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

            q_time = datetime.datetime.strptime(q.start_quiz.strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
            c_time = datetime.datetime.strptime(current_time.strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
            # print(q_time)
            # print(c_time)

            if not q_time >= c_time:
                if not IntervalQuiz.objects.filter(quiz=q).exists():
                    self.create_quiz_interval(q)
                else:
                    self.update_quiz_interval(q)

    def create_quiz_interval(self, q):
        hours, minutes = divmod(q.time, 60)
        quiz_interval = IntervalQuiz.objects.create(quiz=q, intervalTime=datetime.time(hour=hours, minute=minutes))

        q_end_in = quiz_interval.intervalTime

        q_endin = datetime.datetime.strptime(q_end_in.strftime("%H:%M:%S"), "%H:%M:%S")

        q_interval = datetime.datetime.strptime(datetime.time(second=1).strftime("%H:%M:%S"), "%H:%M:%S")

        IntervalQuiz.objects.filter(quiz=quiz_interval.quiz).update(
            intervalTime=str(q_endin - q_interval)
        )

    def update_quiz_interval(self, q):
        constant_time = datetime.time(hour=0, minute=0, second=0)

        get_current_interval = IntervalQuiz.objects.get(quiz=q)

        q_end_in = get_current_interval.intervalTime

        q_endin = datetime.datetime.strptime(q_end_in.strftime("%H:%M:%S"), "%H:%M:%S")

        q_interval = datetime.datetime.strptime(datetime.time(second=1).strftime("%H:%M:%S"), "%H:%M:%S")

        if not q_end_in == constant_time:
            IntervalQuiz.objects.filter(quiz=get_current_interval.quiz).update(
                intervalTime=str(q_endin - q_interval)
            )

    def get_quiz_start_time(self):
        constant_time = datetime.time(hour=0, minute=0, second=0)

        context = {}

        for q in Quiz.objects.filter(is_answered=False):
            current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

            q_time = datetime.datetime.strptime(q.start_quiz.strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
            c_time = datetime.datetime.strptime(current_time.strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")

            if q_time >= c_time:
                context[str(q.id)] = {'time_now': str(abs(q_time - c_time)), 'is_start': False}
            else:
                get_current_interval = IntervalQuiz.objects.get(quiz=q)

                q_end_in = get_current_interval.intervalTime

                if q_end_in == constant_time:

                    context[str(q.id)] = {'time_now': str(constant_time), 'is_start': 'ended'}

                    self.update_quiz_and_interval(q)

                else:
                    context[str(q.id)] = {'time_now': str(get_current_interval.intervalTime), 'is_start': True}

                '''if not IntervalQuiz.objects.filter(quiz=q).exists():
                    hours, minutes = divmod(q.time, 60)
                    quiz_interval = IntervalQuiz.objects.create(quiz=q, intervalTime=datetime.time(hour=hours, minute=minutes))

                    q_end_in = quiz_interval.intervalTime

                    q_endin = datetime.datetime.strptime(q_end_in.strftime("%H:%M:%S"), "%H:%M:%S")

                    q_interval = datetime.datetime.strptime(datetime.time(second=1).strftime("%H:%M:%S"), "%H:%M:%S")

                    IntervalQuiz.objects.filter(quiz=quiz_interval.quiz).update(
                        intervalTime=str(q_endin - q_interval)
                    )

                    get_current_interval = IntervalQuiz.objects.get(quiz=q)

                    context[str(q.id)] = {'time_now': str(get_current_interval.intervalTime), 'is_start': True}
                else:
                    get_current_interval = IntervalQuiz.objects.get(quiz=q)

                    q_end_in = get_current_interval.intervalTime

                    q_endin = datetime.datetime.strptime(q_end_in.strftime("%H:%M:%S"), "%H:%M:%S")

                    q_interval = datetime.datetime.strptime(datetime.time(second=1).strftime("%H:%M:%S"), "%H:%M:%S")


                    if not q_end_in == constant_time:
                        IntervalQuiz.objects.filter(quiz=get_current_interval.quiz).update(
                            intervalTime=str(q_endin - q_interval)
                        )

                        get_current_interval = IntervalQuiz.objects.get(quiz=q)

                        context[str(q.id)] = {'time_now': str(get_current_interval.intervalTime), 'is_start': True}

                    else:
                        context[str(q.id)] = {'time_now': str(constant_time), 'is_start': 'ended'}

                        self.update_quiz_and_interval(q)'''

        return context

    def update_quiz_and_interval(self, q):
        Quiz.objects.filter(name=q.name).update(
            is_answered=True
        )
        IntervalQuiz.objects.get(quiz=q).delete()
