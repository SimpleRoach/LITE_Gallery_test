from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, s3_client

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.post("/images/", response_model=schemas.Image)
async def create_image(image: schemas.ImageCreate, db: Session = Depends(database.get_db)):
    db_project = crud.get_project(db, project_id=image.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_image = crud.create_image(db=db, image=image)
    upload_link = s3_client.create_presigned_url(bucket_name="your-bucket-name", object_name=image.filename)

    return {"image_id": db_image.id, "upload_link": upload_link}


@app.get("/projects/{id}/images", response_model=schemas.Project)
async def read_project_images(id: int, db: Session = Depends(database.get_db)):
    db_project = crud.get_project(db, project_id=id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
