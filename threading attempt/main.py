from typing import List
from fastapi import Depends, FastAPI, HTTPException
from starlette.responses import HTMLResponse
import folium
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

map = folium.Map(
    location=[41.35, 2.18],
    zoom_start=13.2
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/populate/")
def populate(skip: int = 0, db: Session = Depends(get_db)):
    items = crud.get_items(db=db, skip=skip)
    for item in items:
        if item.is_active:
            folium.CircleMarker(
                location=[item.lat, item.lon],
                radius=5,
                tooltip=str(item.inc_type + ' ' + item.inc_detail + ' ' + str(item.timestamp.replace(microsecond=0))),
                fill=True,
                fill_color='#{:02x}{:02x}{:02x}'.format(249, 56, 34),
                stroke = False,
                fill_opacity=.5
                ).add_to(map)

# curl -X POST http://127.0.0.1:8000/populate/

@app.post("/users/{user_id}/", response_model=schemas.User, tags=["users"])
def create_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_users = crud.get_user(db=db, user_id=user.id)
    if db_users:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

# curl -d '{"id":9879780}' -H "content-Type: application/json" -X POST http://127.0.0.1:8000/users/

@app.post("/input/{user_id}/", response_model=schemas.Item, tags=["input"])
def enter_item(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    folium.CircleMarker(
        location=[item.lat, item.lon],
        radius=5,
        tooltip=str(item.inc_type + ' ' + item.inc_detail + ' ' + str(item.timestamp.replace(microsecond=0))),
        fill=True,
        fill_color='#{:02x}{:02x}{:02x}'.format(249, 56, 34),
        stroke = False,
        fill_opacity=.5
        ).add_to(map)
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# curl -d '{"id":9879780, "inc_type":"objeto", "inc_detail":"mar", "lat":41.35, "lon":2.18}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/input/

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip)
    return items

# curl -X GET "http://127.0.0.1:8000/items/" -H  "accept: application/json"

@app.get("/dashboard/", tags=["dashboard"])
def get_dashboard():
    return HTMLResponse(content=map._repr_html_())
