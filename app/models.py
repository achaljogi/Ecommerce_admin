from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from fastapi import FastAPI, Depends, HTTPException, Query
from .database import Base


# ---------------- BRAND ----------------

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    logo_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="brand")


# ---------------- CATEGORY ----------------

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    subcategories = relationship(
        "SubCategory",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    products = relationship("Product", back_populates="category")


# ---------------- SUBCATEGORY ----------------

class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="subcategories"
    )

    products = relationship(
        "Product",
        back_populates="subcategory"
    )


# ---------------- PRODUCT ----------------

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    slug = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    sku = Column(String(100), unique=True, nullable=False)

    base_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    brand_id = Column(
        Integer,
        ForeignKey("brands.id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    subcategory_id = Column(
        Integer,
        ForeignKey("subcategories.id"),
        nullable=False
    )

    brand = relationship(
        "Brand",
        back_populates="products"
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    subcategory = relationship(
        "SubCategory",
        back_populates="products"
    )

    variants = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete-orphan"
    )


# ---------------- PRODUCT VARIANT ----------------

class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    sku = Column(String(100), unique=True, nullable=False)
    variant_name = Column(String(100), nullable=False)

    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    product = relationship(
        "Product",
        back_populates="variants"
    )