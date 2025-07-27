from fastapi.websockets import WebSocket
from typing import Any


class Room:
    def __init__(self,name:str):
        self.room_name = name
        self.active_connections:dict[WebSocket,Any]={}

    def is_user_connected(self,sub:Any):
        return sub in self.active_connections.values()

    def list_users(self):
        return self.active_connections.values()

    def add_user(self,sub:Any,websocket:WebSocket):
        self.active_connections[websocket]=sub

    def remove_user(self,websocket:WebSocket):
        sub = self.active_connections.pop(websocket, "Utilisateur inconnu")
        return sub

class ChatConnectionManager:
    def __init__(self):
        self.rooms:dict[str,Room]={}

    def list_rooms(self)->list[str]:
        return list(self.rooms.keys())

    def list_rooms_user(self,room_name:str):
        try :
            room =  self.get_room(room_name=room_name)
            return room.list_users()
        except ValueError:
            return []

    def create_room(self, room_name):
        try:
            existing_room=self.get_room(room_name)
        except ValueError:
            room = Room(name=room_name)
            self.rooms[room_name]=room

    async def send_private_message(self,room_name:str,to_sub:Any,message:str):
        room = self.get_room(room_name=room_name)
        for connection,sub in room.active_connections.items():
            if sub==to_sub:
                await connection.send_text(data=message)
                break

    async def connect(self,websocket:WebSocket,room_name:str,sub:Any):
        await websocket.accept()
        room=self.get_room(room_name=room_name)
        room.add_user(sub=sub,websocket=websocket)
        await self.broadcast(room_name=room_name,message=f"{sub} a rejoint le chat .")

    async def disconnect(self,websocket:WebSocket,room_name:str):
        room=self.get_room(room_name=room_name)
        sub=room.remove_user(websocket=websocket)
        await self.broadcast(
            room_name=room_name, message=f"{sub} vient de quitter le chat"
        )

    async def broadcast(self,room_name:str,message:str):
        room=self.get_room(room_name=room_name)
        for connection in room.active_connections:
            await connection.send_text(data=message)

    def get_room(self,room_name:str):
        if room_name in self.rooms:
            return self.rooms[room_name]
        else:
            raise ValueError(f"La salle '{room_name}' n'existe pas.")
