from fastapi import FastAPI
import crud
import models
import schemas
import database
import s3_client

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Message text was: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/images/", response_model=schemas.Image)
async def create_image(image: schemas.ImageCreate, db: Session = Depends(database.get_db)):
    db_project = crud.get_project(db, project_id=image.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_image = crud.create_image(db=db, image=image)
    upload_link = await s3_client.create_presigned_url(bucket_name="test_1", object_name=image.filename)

    return {"image_id": db_image.id, "upload_link": upload_link}


@app.get("/projects/{id}/images", response_model=schemas.Project)
async def read_project_images(id: int, db: Session = Depends(database.get_db)):
    db_project = crud.get_project(db, project_id=id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
