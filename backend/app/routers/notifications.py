from asyncio import CancelledError
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from app.db.models import User
from app.db.schemas.notifications import Notification, NotificationCreate
from app.services.notifications import NotificationService, get_service
from app.routers.users import get_current_user


clients : dict[int, list[asyncio.Queue]] = {}

router = APIRouter(prefix="/notifications", tags=["Notifications"])

async def notify_user(user_id : int, notif : Notification):
    """ Notify user"""
    if user_id in clients:
        for client in clients[user_id]:
            await client.put(notif)


@router.get("/all")
def get_all(
    service : NotificationService = Depends(get_service),
    current_user : User = Depends(get_current_user)
):
  return service.list(current_user)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Notification)
async def add(
    notification : NotificationCreate,
    service : NotificationService = Depends(get_service),
    current_user : User = Depends(get_current_user) 
):
    if current_user.is_manager:
        notif : Notification =  service.create(notification)
        await notify_user(current_user.id, notif) # Send notification
        return notif
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized, not manager")

@router.put("/{id}", response_model=Notification)
def update(
    id : int,
    service : NotificationService = Depends(get_service),
    current_user : User = Depends(get_current_user) 
):
    return service.update(current_user, id)


@router.post("/stream")
async def notification_stream(
    request : Request,
    current_user : User = Depends(get_current_user)
):
    """Server-Sent Events (SSE) to stream notifications for a specific user."""
    async def event_notification():

        client_queue = asyncio.Queue() # Create a client queue

        if current_user.id not in clients: # Check if already exists if not create a list
            clients[current_user.id] = []
        
        clients[current_user.id].append(client_queue) # Add the new queue to the client

        try:
            while True:
                if await request.is_disconnected(): # if client closed cut connection
                    break
                
                notif : Notification = await client_queue.get()

                yield f"data: {notif.json()}\n\n"

        except CancelledError as e:
            print(f"Disconnected from client (via refresh/close) {current_user}")
            # Do any other cleanup, if any
            raise e
        finally:
            clients[current_user.id].remove(client_queue) # Remove client 
            if not clients[current_user.id]: # Check if queues exists in client if not delete it
                del clients[current_user.id] 

    return StreamingResponse(event_notification(), media_type="text/event-stream")