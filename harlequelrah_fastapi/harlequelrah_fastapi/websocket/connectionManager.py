from fastapi import WebSocket,WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections:List[WebSocket]=[]

    async def connect(self,webSocket:WebSocket):
        await webSocket.accept()
        self.active_connections.append(WebSocket)

    async def disconnect(self,webSocket:WebSocket):
        self.active_connections.remove(webSocket)

    async def send_message(self,message:str):
        for connection in self.active_connections:
            await connection.send_text(message)
