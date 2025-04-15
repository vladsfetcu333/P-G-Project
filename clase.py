from sqlalchemy import DateTime, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import  Column, Integer, String
import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "project.db")
DATABASE_URL = "sqlite:///" + DATABASE_FILE
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

try:
    with engine.connect() as connection:
        print("Database connected successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")

Session = sessionmaker(bind=engine)
session = Session()

class Plant(Base):
    __tablename__ = 'plants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    capacity = Column(Integer)
    
    plant_products = relationship('PlantProduct', back_populates='plants')
    plant_materials = relationship('PlantMaterial', back_populates='plants')

    
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    price = Column(Float)

    plant_products = relationship('PlantProduct', back_populates='products')
    storage_products = relationship('StorageProducts', back_populates='products')
    order_products = relationship('OrderProducts', back_populates='products')
    product_materials = relationship('ProductMaterials', back_populates='products')


class Material(Base):
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    unit = Column(String)
    cost = Column(Float)

    plant_materials = relationship('PlantMaterial', back_populates='materials')
    storage_materials = relationship('StorageMaterials', back_populates='materials')
    product_materials = relationship('ProductMaterials', back_populates='materials')


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date=Column(DateTime)
    customer_name = Column(String, unique=True, nullable=False)
    status = Column(String)

    order_products = relationship('OrderProduct', back_populates='orders')

class PlantProduct(Base):
    __tablename__ = 'plant_products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('plants.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    plants = relationship('Plant', back_populates='plant_products')
    products = relationship('Product', back_populates='plant_products')


class ProductMaterial(Base):
    __tablename__ = 'product_materials'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    material_id = Column(Integer, ForeignKey('materials.id'))
    quantity = Column(Integer)

    products = relationship('Product', back_populates='product_materials')
    materials = relationship('Material', back_populates='product_materials')

class PlantMaterial(Base):
    __tablename__ = 'plant_materials'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('plants.id'))
    material_id = Column(Integer, ForeignKey('materials.id'))
    quantity = Column(Integer)   

    plants = relationship('Plant', back_populates='plant_materials')
    materials = relationship('Material', back_populates='plant_materials')
    

class OrderProduct(Base):
    __tablename__ = 'order_products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    orders = relationship('Order', back_populates='order_products')
    products = relationship('Product', back_populates='order_products')

class StorageProduct(Base):
    __tablename__ = 'storage_products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)  

    products = relationship('Product', back_populates='storage_products')

class StorageMaterial(Base):
    __tablename__ = 'storage_materials'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'))
    quantity = Column(Integer)

    materials = relationship('Material', back_populates='storage_materials')