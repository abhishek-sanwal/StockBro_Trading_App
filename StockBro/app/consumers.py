
import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer


class StockConsumer(WebsocketConsumer):

    def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"stock_{self.room_name}"

        # Join room group

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_node):

        # Leave Room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "stock_update",
                "message": message
            }
        )

    # Receive message from room group

    def stock_update(self, event):

        message = event["message"]

        self.send(text_data=json.dumps(
            {
                "message": message
            }
        ))
