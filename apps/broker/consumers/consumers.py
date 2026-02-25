import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SignalInvalidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.group_name = "signal_invalid"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def signal_invalid_event(self, event: dict):
        await self.send(text_data=json.dumps(event["data"]))
