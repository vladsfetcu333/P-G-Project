from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from clase import Order, OrderProduct, ProductMaterial, StorageProduct
from API import get_db


router = APIRouter()
@router.post("/orders/{order_id}/process")
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
          
          stock.quantity -= quantity_needed

    db.commit()
    
    return {"message": f"Comanda {order_id} a fost procesata si plasata cu succes"}