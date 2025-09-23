import asyncio
from fastapi import WebSocket

from typing import List, Dict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        await websocket.accept()
        async with self.lock:
            self.active_connections[user_id].append(websocket)

        return

    async def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        async with self.lock:
            if websocket in self.active_connections.get(user_id, []):
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]

    async def notify_user(self, message: str, user_id: str):
        async with self.lock:
            for connection in self.active_connections.get(user_id, []):
                await connection.send_text(message)


manager = ConnectionManager()
