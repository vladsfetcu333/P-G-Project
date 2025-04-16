from sqlalchemy import DateTime, Float, ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    capacity = Column(Integer)

    plant_products = relationship('PlantProduct', back_populates='plant')
    plant_materials = relationship('PlantMaterial', back_populates='plant')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    price = Column(Float)

    plant_products = relationship('PlantProduct', back_populates='product')
    storage_products = relationship('StorageProduct', back_populates='product')
    order_products = relationship('OrderProduct', back_populates='product')
    product_materials = relationship('ProductMaterial', back_populates='product')


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    unit = Column(String)
    cost = Column(Float)

    plant_materials = relationship('PlantMaterial', back_populates='material')
    storage_materials = relationship('StorageMaterial', back_populates='material')
    product_materials = relationship('ProductMaterial', back_populates='material')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime)
    customer_name = Column(String, unique=True, nullable=False)
    status = Column(String)

    order_products = relationship('OrderProduct', back_populates='order')


class PlantProduct(Base):
    __tablename__ = 'plant_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('plants.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    plant = relationship('Plant', back_populates='plant_products')
    product = relationship('Product', back_populates='plant_products')


class PlantMaterial(Base):
    __tablename__ = 'plant_materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('plants.id'))
    material_id = Column(Integer, ForeignKey('materials.id'))
    quantity = Column(Integer)

    plant = relationship('Plant', back_populates='plant_materials')
    material = relationship('Material', back_populates='plant_materials')


class ProductMaterial(Base):
    __tablename__ = 'product_materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    material_id = Column(Integer, ForeignKey('materials.id'))
    quantity = Column(Integer)

    product = relationship('Product', back_populates='product_materials')
    material = relationship('Material', back_populates='product_materials')


class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship('Order', back_populates='order_products')
    product = relationship('Product', back_populates='order_products')


class StorageProduct(Base):
    __tablename__ = 'storage_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    product = relationship('Product', back_populates='storage_products')


class StorageMaterial(Base):
    __tablename__ = 'storage_materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'))
    quantity = Column(Integer)

    material = relationship('Material', back_populates='storage_materials')


Base.metadata.create_all(engine)
