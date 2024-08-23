import json
from app.models import Stockdeatils
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import copy


class StockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, stockpicker):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in stockpicker:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.SECONDS)

            PeriodicTask.objects.create(
                interval=schedule,
                name='every-one-second',
                task="app.tasks.update_stocks_data",
                args=json.dumps([stockpicker]))

    @sync_to_async
    def addToStockDetail(self, stockpicker):
        user = self.scope["user"]
        for i in stockpicker:
            stock, _ = Stockdeatils.objects.get_or_create(symbol=i)
            stock.user.add(user)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("Web socket connected successfully")
        # Parse query_string
        query_params = parse_qs(self.scope["query_string"].decode())

        print(query_params)
        stockpicker = query_params['stockpicker']

        # add to celery beat
        await self.addToCeleryBeat(stockpicker)
        print("Arrived 1st function")
        # add user to stockdetail
        # await self.addToStockDetail(stockpicker)

        await self.accept()

    @sync_to_async
    def helper_func(self):
        user = self.scope["user"]
        stocks = Stockdeatils.objects.filter(user__id=user.id)
        task = PeriodicTask.objects.get(name="every-10-seconds")
        args = json.loads(task.args)
        args = args[0]
        for i in stocks:
            i.user.remove(user)
            if i.user.count() == 0:
                args.remove(i.stock)
                i.delete()
        if args == None:
            args = []

        if len(args) == 0:
            task.delete()
        else:
            task.args = json.dumps([args])
            task.save()

    async def disconnect(self, close_code):
        # await self.helper_func()
        print("Disconnected function")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Disconnected Successfully")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_stock_update',
                'message': message
            }
        )

    @sync_to_async
    def selectUserStocks(self):
        user = self.scope["user"]
        user_stocks = user.stockdetail_set.values_list('stock',
                                                       flat=True)
        return list(user_stocks)

    # Receive message from room group
    async def send_stock_update(self, event):
        message = event['message']
        # message = copy.copy(message)
        print("We are recieving messages")
        print(message, "Web socket message")
        # user_stocks = await self.selectUserStocks()

        # keys = message.keys()
        # for key in list(keys):
        #     if key not in user_stocks:
        #         del message[key]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
