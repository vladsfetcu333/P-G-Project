from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from clase import SessionLocal, Plant 
from schemas import PlantCreate, PlantRead, PlantUpdate
from typing import List
from typing import Generator

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
    db_plant = Plant(**plant.dict())
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
    for field, value in updated.dict().items():
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

