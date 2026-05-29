

import logging

from fastapi import WebSocket


logger = logging.getLogger("app.core.websocket")

class ConnectionManager:

    def __init__(self) -> None:
        self.active_connections: set[WebSocket] = set()


    async def connect(self, websocket: WebSocket)-> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Nueva conexion KDS, total activas: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket)-> None:
        self.active_connections.discard(websocket)
        logger.info(f"Conexion KDS finalizada. TOtal de conexiones activas: {len(self.active_connections)}")

    async def broadcast(self, event_type: str, data: dict[str,any])->None:

        payload = {
            "event": event_type,
            "data": data
        }

        if not self.active_connections:
            logger.info(f"Evento {event_type} descartado(sin pantallas conectadas)")
            return
        
        logger.info(f"Broadcast {event_type} a {len(self.active_connections)} conexiones")

        for connection in list(self.active_connections):
            try:
                await connection.send_json(payload)
            except Exception as e:
                logger.warning(f"Error al enviar WebSocket. Removiendo conexion: {e}")
                self.active_connections.discard(connection)


manager = ConnectionManager()                

