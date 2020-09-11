from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from starlette.responses import HTMLResponse
from jinja2 import Template

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
layer = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# curl -X PUT http://127.0.0.1:8000/remove/9879780/

@app.post("/input/{user_id}/", response_model=schemas.Item, tags=["input"])
def enter_item(user_id: str, item: schemas.Incident, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# curl -d '{"id":"0000000009879780", "inc_type":"objeto", "inc_detail":"mar", "lat":41.358767876876, "lon":2.1878687687667, "url":"https://maps.google.com/maps?q=41.358767876876%2C2.1878687687667&z=14&hl=en", "pic":"https://drive.google.com/file/d/16udAHXF3QNouyb6bXUNgIQYW_bUzhSDp/preview"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/input/0034687978031/
# curl -d '{"id":"1000000009879787", "inc_type":"vertido", "inc_detail":"dársena", "lat":41.368767876876, "lon":2.1778687687667, "url":"https://maps.google.com/maps?q=41.368767876876%2C2.1778687687667&z=14&hl=en", "pic":"https://drive.google.com/file/d/16udAHXF3QNouyb6bXUNgIQYW_bUzhSDp/preview"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/input/0034687978022/
# curl -d '{"id":"2000000000987979", "inc_type":"vertido", "inc_detail":"calzada", "lat":41.348767876876, "lon":2.1978687687667, "url":"https://maps.google.com/maps?q=41.348767876876%2C2.1978687687667&z=14&hl=en", "pic":"https://drive.google.com/file/d/16udAHXF3QNouyb6bXUNgIQYW_bUzhSDp/preview"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/input/0034687978013/

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip)
    return items

# curl -X GET "http://127.0.0.1:8000/items/" -H  "accept: application/json"

@app.get("/dashboard/", tags=["dashboard"])
def dashboard(skip: int = 0, db: Session = Depends(get_db)):
    items = crud.get_items(db=db, skip=skip)
    tmpl = Template('''
    <table style="width:100%">
        <tr>
        <th>ID</th>
        <th>Fecha</th>
        <th>Incidencia</th>
        <th>Detalle</th>
        <th>Mapa</th>
        <th>Foto</th>
        <th>Usuario</th>
        </tr>
        {% for item in items %}
        <tr>
        <td>{{ item['id'] }}</td>
        <td>{{ item['timestamp'] }}</td>
        <td>{{ item['inc_type'] }}</td>
        <td>{{ item['inc_detail'] }}</td>
        <td><a href={{ item['url'] }}>{{ item['lat'] }}, {{ item['lon'] }}</a></td>
        <td><iframe src={{ item['pic'] }}></iframe></td>
        <td>{{ item['owner_id'] }}</td>
        </tr>
        {% endfor %}
    </table>

    <style>
        table {
            margin: 0 auto;
            font-size: medium;
            border: 1px solid black;
        }

        td {
            background-color: #ccffff;
            border: 1px solid black;
        }

        th,
        td {
            font-weight: bold;
            border: 1px solid black;
            padding: 10px;
            text-align: center;
            font-family: 'Helvetica';
        }

        td {
            font-weight: lighter;
        }
    </style>
    ''')

    return HTMLResponse(tmpl.render(items = items))
