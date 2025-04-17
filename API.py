from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from clase import SessionLocal, Plant 
from schemas import PlantCreate, PlantRead, PlantUpdate
from typing import List
from typing import Generator
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from clase import Order, OrderProduct, ProductMaterial, StorageProduct

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return {'message': 'Welcome!'}

@app.post("/plants/", response_model=PlantRead)
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = Plant(**plant.model_dump())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

@app.get("/plants/", response_model=List[PlantRead])
def read_all_plants(db: Session = Depends(get_db)):
    return db.query(Plant).all()

@app.get("/plants/{plant_id}", response_model=PlantRead)
def read_plant_by_id(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@app.put("/plants/{plant_id}", response_model=PlantRead)
def update_plant(plant_id: int, updated: PlantUpdate, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    for field, value in updated.model_dump().items():
        setattr(plant, field, value)
    
    db.commit()
    db.refresh(plant)
    return plant


@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"message": f"Plant with ID {plant_id} deleted successfully"}

@app.post("/orders/{order_id}/process")
def process_order(order_id : int, db : Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Comanda nu exista")
    
    order_products = db.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()

    for op in order_products:
       product_id = op.product_id
       quantity_ordered = op.quantity
       product_materials = db.query(ProductMaterial).filter(ProductMaterial.product_id == product_id).all()
       for pm in product_materials:
          material_id = pm.material_id
          quantity_needed = pm.quantity * quantity_ordered

          stock = db.query(StorageProduct).filter(StorageProduct.material_id == material_id).first()
          if not stock:
              raise HTTPException(status_code=404, detail=f"Materialul {material_id} nu exista in stoc")
          if stock.quantity < quantity_needed:
                raise HTTPException(status_code=400, detail=f"Stoc insuficient pentru materialul {material_id}")
          