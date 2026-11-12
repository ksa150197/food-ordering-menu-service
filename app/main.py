from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import MenuItem
from .schemas import MenuItemCreate, MenuItemOut, MenuItemUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Food Ordering - Menu Service", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"service": "menu-service", "status": "healthy"}

@app.post("/menu/items", response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
def create_item(payload: MenuItemCreate, db: Session = Depends(get_db)):
    item = MenuItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/menu/items", response_model=list[MenuItemOut])
def list_items(available_only: bool = False, db: Session = Depends(get_db)):
    query = select(MenuItem).order_by(MenuItem.id)
    if available_only:
        query = query.where(MenuItem.available.is_(True))
    return db.scalars(query).all()

@app.get("/menu/items/{item_id}", response_model=MenuItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(MenuItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@app.put("/menu/items/{item_id}", response_model=MenuItemOut)
def update_item(item_id: int, payload: MenuItemUpdate, db: Session = Depends(get_db)):
    item = db.get(MenuItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@app.patch("/menu/items/{item_id}/availability", response_model=MenuItemOut)
def set_availability(item_id: int, available: bool, db: Session = Depends(get_db)):
    item = db.get(MenuItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    item.available = available
    db.commit()
    db.refresh(item)
    return item

@app.delete("/menu/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(MenuItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
    return None
