from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt

from app.api import auth, monitorings, notifications
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.services.realtime import realtime_manager

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(auth.router)
app.include_router(monitorings.router)
app.include_router(notifications.router)


@app.on_event('startup')
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)) -> None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload.get('sub'))
    except (JWTError, TypeError, ValueError):
        await websocket.close(code=1008)
        return

    await realtime_manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        realtime_manager.disconnect(user_id, websocket)
