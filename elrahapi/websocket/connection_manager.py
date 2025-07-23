from fastapi import WebSocket,WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections:list[WebSocket]=[]

    async def connect(self,webSocket:WebSocket):
        await webSocket.accept()
        self.active_connections.append(webSocket)

    async def disconnect(self,webSocket:WebSocket):
        self.active_connections.remove(webSocket)

    async def send_message(self,sender_websocket:WebSocket,message:str):
        active_connections=[websocket for websocket in self.active_connections if websocket != sender_websocket]
        for connection in active_connections:
            try :
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)



    async def broadcast(self,message:str):
        for connection in self.active_connections:
            try :
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)
